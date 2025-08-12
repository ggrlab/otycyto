from torch import Tensor


def display_cloud(ax, measure, color, x_i: int = 0, y_i: int = 1, npoints=None, *args, **kwargs):
    """Display a point cloud on a given matplotlib axis.

    Args:
        ax (matplotlib.axes.Axes): The axis to plot on.
        measure (torch.Tensor): The point cloud data.
        color (str): The color of the points.
        columns (List[int], optional): The columns to use for the x and y coordinates. Defaults to [0, 1].
    """
    if isinstance(measure, Tensor):
        measure = measure.cpu().numpy()
    ax.set_aspect("equal")
    if npoints is not None:
        measure = measure[: min(npoints, measure.shape[0])]

    ax.scatter(measure[:, x_i], measure[:, y_i], c=color, *args, **kwargs)
