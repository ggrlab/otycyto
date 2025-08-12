import datetime
from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from geomloss import SamplesLoss
from torch.autograd import grad

from otcyto.plot.figure_clouds import figure_clouds

# from otcyto.plot.figure_umap import figure_umap


class OTDPairwise:
    def __init__(
        self,
        sources: list[torch.tensor],
        targets: list[torch.tensor],
        sources_names: list[str] | None = None,
        targets_names: list[str] | None = None,
        loss: SamplesLoss = SamplesLoss(loss="sinkhorn", p=2, blur=0.05, scaling=0.8),
        verbose: bool = False,
        intermediate_file: Path | str = None,
        skipping_fun: Callable[[int, int], bool] = lambda i, j: False,
        # return_time: bool = False,
        # brenier_map: bool = False,
        output_type: str | None = "torch",
    ):
        """Initialize the OTDPairwise class with the given parameters.

        Args:
            sources (List): List of data elements which should be "transported" to the targets
            targets (List): List of data elements which the sources should be "transported" to
            sources_names (Optional[List[str]], optional): List of names for elements in sources. Defaults to None, becomes sample_[i] in list order.
            targets_names (Optional[List[str]], optional): List of names for elements in targets. Defaults to None, becomes sample_[i] in list order.
            loss (SamplesLoss, optional): Loss function to compute the OTD. Defaults to SamplesLoss(loss="sinkhorn", p=2, blur=0.05, scaling=0.8).
            verbose (bool, optional): If True, print progress information. Defaults to False.
            intermediate_file (Optional[str], optional): Path to file for saving intermediate results. Defaults to None.
            skipping_fun (Callable[[int, int], bool], optional): Function to determine if a pair should be skipped. Defaults to lambda i, j: False.
            return_time (bool, optional): If True, return computation times. Defaults to False.
            brenier_map (bool, optional): If True, compute the Brenier map. Defaults to False.
        """
        self.sources = sources
        # For the Brenier map calculation, we need to keep track of the gradients of the sources
        for x in self.sources:
            x.requires_grad = True

        self.targets = targets
        self.sources_names = (
            sources_names
            if sources_names is not None
            else [f"sample_{i}" for i in range(len(sources))]
        )
        self.targets_names = (
            targets_names
            if targets_names is not None
            else [f"sample_{i}" for i in range(len(targets))]
        )
        if len(sources) != len(self.sources_names):
            raise ValueError("The number of sources and sources_names must be equal.")
        if len(targets) != len(self.targets_names):
            raise ValueError("The number of targets and targets_names must be equal.")
        self.loss: Callable = loss
        self.verbose = verbose
        self._intermediate_file = intermediate_file
        self._skipping_fun = skipping_fun
        self.output_type = output_type

        self._time_calculation = torch.zeros(
            (len(self.sources), len(self.targets)), dtype=torch.float32
        )
        self._otd = torch.zeros((len(self.sources), len(self.targets)), dtype=torch.float32)
        self._otd_calculated = False

        self._brenier_maps: list[list[torch.tensor]] = None
        self._brenier_maps_all_computed = False

    @property
    def brenier_maps(
        self,
        source_i: int | None = None,
        target_j: int | None = None,
    ) -> torch.Tensor | list[list[torch.Tensor]]:
        """
        Getter for brenier_maps.

        Args:
            source_i (Union[int, None], optional): Index of the source sample. If None, returns all Brenier maps. Defaults to None.
            target_j (Union[int, None], optional): Index of the target sample. If None, returns all Brenier maps. Defaults to None.

        Returns:
            Union[torch.Tensor, List[List[torch.Tensor]]]: The Brenier map for the specified source and target indices, or all Brenier maps if indices are not provided.
        """
        if self._brenier_maps is None:
            # Initialize the Brenier maps as a list of lists of None
            self._brenier_maps = [
                [None for _ in range(len(self.targets))] for i in range(len(self.sources))
            ]
        if source_i is not None and target_j is not None:
            # Compute the Brenier map for the specified source and target indices if not already computed
            if self._brenier_maps[source_i][target_j] is None:
                self.compute_brenier_map(source_i, target_j)
            return self._brenier_maps[source_i][target_j]
        else:
            # Compute all Brenier maps if not already computed
            if not self._brenier_maps_all_computed:
                self.compute_all_brenier_maps()
            return self._brenier_maps

    def compute_all_brenier_maps(self):
        """Compute all Brenier maps."""
        for source_i in range(len(self.sources)):
            for target_j in range(len(self.targets)):
                self.compute_brenier_map(source_i, target_j)
                self._brenier_maps[source_i][target_j] = self._brenier_maps[source_i][
                    target_j
                ].cpu()
        self._brenier_maps_all_computed = True

    def compute_brenier_map(self, source_i: int, target_j: int):
        """Compute the Brenier map for the given source and target."""
        if not self._otd_calculated:
            raise ValueError(
                "OTD must be calculated before Brenier map can be computed. (Call .compute() first.)"
            )

        # https://www.kernel-operations.io/geomloss/_auto_examples/sinkhorn_multiscale/plot_kernel_truncation.html#sphx-glr-auto-examples-sinkhorn-multiscale-plot-kernel-truncation-py
        #  The generalized "Brenier map" is (minus) the gradient of the Sinkhorn loss
        # with respect to the Wasserstein metric:
        [dx_i] = grad(
            self._otd[source_i, target_j],
            [self.sources[source_i]],
            retain_graph=True,
        )
        brenier_map = -dx_i
        # Given each point has the same weight, we need to multiply the Brenier map by the number of points in the source
        self._brenier_maps[source_i][target_j] = brenier_map * len(self.sources[source_i])

    @property
    def time_calculation(self) -> torch.Tensor:
        """Getter for time_calculation."""
        return pd.DataFrame(
            self._time_calculation.cpu().numpy(),
            index=self.sources_names,
            columns=self.targets_names,
        )

    @property
    def otd_torch(self) -> torch.Tensor:
        return self._otd.detach().cpu()

    @property
    def otd_numpy(self) -> np.ndarray:
        return self.otd_torch.numpy()

    @property
    def otd_df(self) -> pd.DataFrame:
        return pd.DataFrame(
            self.otd_numpy,
            index=self.sources_names,
            columns=self.targets_names,
        )

    def save_intermediate(self, filename: Path | str):
        """Save intermediate results to a file."""
        self.otd_df.to_csv(filename)
        print(f"    Wrote {filename}")

    def compute(
        self,
    ) -> None:
        """Compute the pairwise OTD between each element of the two lists of data.

        Returns:
            Tuple[pd.DataFrame, Optional[List[List[torch.Tensor]]], Optional[pd.DataFrame]]: Pairwise distances, Brenier maps, and optionally computation times.
        """
        for source_i in range(len(self.sources)):
            for target_j in range(len(self.targets)):
                # Skip the pair if skipping_fun returns True
                if self._skipping_fun(source_i, target_j):
                    if self.verbose:
                        print(
                            f"Skipping {self.sources_names[source_i]} -> {self.targets_names[target_j]}"
                        )
                    continue
                if self.verbose:
                    print(
                        "Compute OTD from",
                        self.sources_names[source_i],
                        "to",
                        self.targets_names[target_j],
                        end=" ",
                        flush=True,
                    )

                # Get the source and target samples
                x_i = self.sources[source_i]
                y_j = self.targets[target_j]

                # Record the start time of the computation
                start = datetime.datetime.now()

                # Compute the optimal transport distance (OTD) using the provided loss function
                self._otd[source_i, target_j] = self.loss(x_i, y_j)

                # Record the end time of the computation
                end = datetime.datetime.now()

                # Calculate and store the time taken for the computation
                self._time_calculation[source_i, target_j] = (end - start).total_seconds()

                # If verbose mode is enabled, print the time taken and the computed distance
                if self.verbose:
                    print(
                        f"(t={end - start})   ",
                        self._otd[source_i, target_j].detach().numpy(),
                        end="",
                    )

                # Save the intermediate results to a file if an intermediate file path is provided
                if self._intermediate_file is not None:
                    self.save_intermediate(self._intermediate_file)
                else:
                    # Print a newline if no intermediate file path is provided
                    print()  # make a newline
        self._otd_calculated = True

    def plot(self, source_i: int = 0, target_j: int = 0, npoints: int = 10000):
        """Plot the points of  given source and target."""
        fig = figure_clouds(
            self.sources[source_i].detach().cpu(),
            self.targets[target_j].cpu(),
            npoints=npoints,
        )
        return fig

    def plot_brenier(
        self,
        source_i: int = 0,
        target_j: int = 0,
        x_i: int = 0,
        y_i: int = 1,
        color_mapping: str = "#5BBF3AAA",
        npoints: int = 10000,
    ):
        """Plot the points of  given source and target."""
        fig = figure_clouds(
            self.sources[source_i].detach().cpu(),
            self.targets[target_j].cpu(),
            x_i=x_i,
            y_i=y_i,
            map_source_to_target=self.brenier_maps[source_i][target_j],
            color_mapping=color_mapping,
            npoints=npoints,
        )
        return fig

    def plot_umap(self, source_i: int = 0, target_j: int = 0):
        raise NotImplementedError
        """Plot the points of  given source and target."""
        fig = figure_umap(
            self.sources[source_i].detach().cpu(),
            self.targets[target_j].cpu(),
            map_source_to_target=self.brenier_maps[source_i][target_j],
        )
        return fig
