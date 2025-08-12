from torch import Tensor


def display_cloud_mapping(
    ax,
    x,
    color,
    x_i=0,
    y_i=1,
    v=None,
    color_mapping: str = "#5BBF3AAA",
    npoints=None,
    *args,
    **kwargs,
):
    if isinstance(x, Tensor):
        x = x.detach().cpu().numpy()

    if npoints is not None:
        x = x[: min(npoints, x.shape[0])]
        if v is not None:
            v = v[: min(npoints, v.shape[0])]
    ax.scatter(x[:, x_i], x[:, y_i], s=None, c=color, edgecolors="none", *args, **kwargs)

    if v is not None:
        if isinstance(v, Tensor):
            v = v.detach().cpu().numpy()
        ax.quiver(
            x[:, x_i],
            x[:, y_i],
            v[:, x_i],
            v[:, y_i],
            scale=1,
            scale_units="xy",
            # color="#5CBF3A",
            color=color_mapping,
            zorder=3,
            # width=1.0 / len(x_),
            width=2e-3,
        )
