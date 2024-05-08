from __future__ import annotations

from gdsfactory.components.bend_s import bend_s
from gdsfactory.port import Port
from gdsfactory.routing.sort_ports import sort_ports as sort_ports_function
from gdsfactory.typings import Route


def get_bundle_sbend(
    ports1: Port,
    ports2: Port,
    sort_ports: bool = True,
    enforce_port_ordering: bool = True,
    axis: str = "X",
    **kwargs,
) -> list[Route]:
    """Returns a list of routes from ports1 to ports2.

    Args:
        ports1: start ports.
        ports2: end ports.
        sort_ports: sort ports.
        enforce_port_ordering: enforces port ordering.
        axis: axis to bend. X or Y.
        kwargs: cross_section settings.

    Returns:
        list of routes.

    """
    if sort_ports:
        ports1, ports2 = sort_ports_function(
            ports1, ports2, enforce_port_ordering=enforce_port_ordering
        )

    routes = []

    for p1, p2 in zip(ports1, ports2):
        ysize = p2.center[1] - p1.center[1]
        xsize = p2.center[0] - p1.center[0]
        if axis == "X":
            bend = bend_s(size=(xsize, ysize), **kwargs)
        elif axis == "Y":
            bend = bend_s(size=(ysize, -xsize), **kwargs)
        else:
            raise ValueError("axis must be 'X' or 'Y'")
        sbend = bend.ref()
        port_in = sbend.get_ports_list()[0]
        sbend.connect(port_in, p1)
        routes.append(
            Route(
                references=[sbend],
                ports=tuple(sbend.get_ports_list()),
                length=bend.info["length"],
            )
        )
    return routes


if __name__ == "__main__":
    import gdsfactory as gf

    c = gf.Component("test_get_route_sbend")
    pitch = 2.0
    ys_left = [0, 10, 20]
    N = len(ys_left)
    y0 = -10
    ys_right = [(i - N / 2) * pitch + y0 for i in range(N)]

    layer = (1, 0)
    right_ports = [
        gf.Port(
            f"R_{i}", center=(0, ys_right[i]), width=0.5, orientation=180, layer=layer
        )
        for i in range(N)
    ]
    left_ports = [
        gf.Port(
            f"L_{i}", center=(-50, ys_left[i]), width=0.5, orientation=0, layer=layer
        )
        for i in range(N)
    ]
    left_ports.reverse()

    routes = gf.routing.get_bundle(right_ports, left_ports, with_sbend=False)
    for route in routes:
        c.add(route.references)
    c.show(show_ports=True)
