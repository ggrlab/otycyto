# from otcyto.plot.display_cloud_mapping import display_cloud_mapping
import torch
from matplotlib import pyplot as plt

from otcyto.plot.display_cloud import display_cloud
from otcyto.plot.display_cloud_mapping import display_cloud_mapping


def figure_clouds(
    source_pointcloud,
    target_pointcloud,
    x_i: int = 0,
    y_i: int = 1,
    map_source_to_target: torch.Tensor = None,
    color_mapping: str = "#5BBF3AAA",
    label_source="Source",
    label_target="Target",
    color_source="#0000ffa0",
    color_target="#ff0000a0",
    npoints=1000,
) -> plt.Figure:
    """Create a figure displaying two point clouds.

    Args:
        pointcloud_a (torch.Tensor): The first point cloud.
        pointcloud_b (torch.Tensor): The second point cloud.
        axes (List[int], optional): The columns to use for the x and y coordinates. Defaults to [0, 1].

    Returns:
        plt.Figure: The created matplotlib figure.
    """
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1)
    display_cloud_mapping(
        ax,
        source_pointcloud,
        color_source,
        x_i=x_i,
        y_i=y_i,
        v=map_source_to_target,
        color_mapping=color_mapping,
        label=label_source,
        npoints=npoints,
    )
    display_cloud(
        ax,
        target_pointcloud,
        color_target,
        x_i=x_i,
        y_i=y_i,
        label=label_target,
        npoints=npoints,
    )
    # ax.set_title(
    #     "Low resolution dataset:\n"
    #     + "Source (N={:,}) and target (M={:,}) point clouds".format(
    #         len(pointcloud_a[0]), len(pointcloud_b[0])
    #     )
    # )
    plt.legend(loc="upper left")
    plt.tight_layout()
    return fig
