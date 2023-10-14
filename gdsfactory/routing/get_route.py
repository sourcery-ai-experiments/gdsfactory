"""`get_route` returns a Manhattan route between two ports.

`get_route` only works for an individual routes. For routing groups of ports you need to use `get_bundle` instead

To make a route, you need to supply:

 - input port
 - output port
 - bend
 - straight
 - taper to taper to wider straights and reduce straight loss (Optional)


To generate a straight route:

 1. Generate the backbone of the route.
 This is a list of manhattan coordinates that the route would pass through
 if it used only sharp bends (right angles)

 2. Replace the corners by bend references
 (with rotation and position computed from the manhattan backbone)

 3. Add tapers if needed and if space permits

 4. generate straight portions in between tapers or bends


 A `Route` is a dataclass with:

- references: list of references for tapers, bends and straight waveguides
- ports: a dict of port name to Port, usually two ports "input" and "output"
- length: a float with the length of the route

"""
from __future__ import annotations

import warnings
from collections.abc import Callable
from functools import partial

import numpy as np
from kfactory.routing.optical import route

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.components.straight import straight as straight_function
from gdsfactory.components.taper import taper as taper_function
from gdsfactory.components.via_corner import via_corner
from gdsfactory.components.wire import wire_corner
from gdsfactory.cross_section import metal2, metal3
from gdsfactory.port import Port
from gdsfactory.routing.manhattan import round_corners
from gdsfactory.typings import (
    ComponentSpec,
    Coordinates,
    CrossSectionSpec,
    MultiCrossSectionAngleSpec,
    Route,
)


def get_route() -> None:
    raise ValueError("get_route is deprecated. Use place_route instead")


def place_route(
    component: Component,
    input_port: Port,
    output_port: Port,
    bend: ComponentSpec = bend_euler,
    with_sbend: bool = False,
    straight: ComponentSpec = straight_function,
    taper: ComponentSpec | None = None,
    start_straight_length: float = 0.0,
    end_straight_length: float = 0.0,
    cross_section: CrossSectionSpec | MultiCrossSectionAngleSpec = "xs_sc",
    **kwargs,
) -> None:
    """Returns a Manhattan Route between 2 ports.

    The references are straights, bends and tapers.
    `get_route` is an automatic version of `get_route_from_steps`.

    Args:
        component: to place the route into.
        input_port: start port.
        output_port: end port.
        bend: bend spec.
        with_sbend: add sbend in case there are routing errors.
        straight: straight spec.
        taper: taper spec.
        start_straight_length: length of starting straight.
        end_straight_length: length of end straight.
        min_straight_length: min length of straight for any intermediate segment.
        cross_section: spec.
        kwargs: cross_section settings.


    .. plot::
        :include-source:

        import gdsfactory as gf

        c = gf.Component('sample_connect')
        mmi1 = c << gf.components.mmi1x2()
        mmi2 = c << gf.components.mmi1x2()
        mmi2.move((40, 20))
        gf.routing.place_route(c, mmi1.ports["o2"], mmi2.ports["o1"], radius=5)
        c.plot()
    """
    with_sbend = kwargs.pop("min_straight_length", None)
    min_straight_length = kwargs.pop("min_straight_length", None)

    if with_sbend:
        warnings.warn("with_sbend is not implemented yet")

    if min_straight_length:
        warnings.warn("minimum straight length not implemented yet")

    xs = gf.get_cross_section(cross_section, **kwargs)
    width = xs.width
    straight = partial(straight, width=width)
    bend90 = gf.get_component(bend_euler)
    taper_cell = gf.get_component(taper) if taper else None

    def straight_dbu(length: int, width: int = width) -> Component:
        return straight(
            length=round(length * component.kcl.dbu),
            width=round(width * component.kcl.dbu),
            cross_section=cross_section,
            **kwargs,
        )

    end_straight = round(end_straight_length / component.kcl.dbu)
    start_straight = round(start_straight_length / component.kcl.dbu)

    route(
        component,
        p1=input_port,
        p2=output_port,
        straight_factory=straight_dbu,
        bend90_cell=bend90,
        taper_cell=taper_cell,
        start_straight=start_straight,
        end_straight=end_straight,
    )


get_route_electrical = partial(
    get_route,
    bend=wire_corner,
    cross_section="xs_metal_routing",
    taper=None,
)

get_route_electrical_m2 = partial(
    get_route,
    bend=wire_corner,
    cross_section=metal2,
    taper=None,
)

get_route_electrical_multilayer = partial(
    get_route_electrical,
    bend=via_corner,
    cross_section=[(metal2, (0, 180)), (metal3, (90, 270))],
)


def get_route_from_waypoints(
    waypoints: Coordinates,
    bend: Callable = bend_euler,
    straight: Callable = straight_function,
    taper: Callable | None = taper_function,
    cross_section: CrossSectionSpec = "xs_sc",
    **kwargs,
) -> Route:
    """Returns a route formed by the given waypoints with bends instead of \
    corners and optionally tapers in straight sections. Tapering to wider \
    straights reduces the optical loss. `get_route_from_waypoints` is a manual \
    version of `get_route` `get_route_from_steps` is a  more concise and \
    convenient version of `get_route_from_waypoints` also available in \
    gf.routing.

    Args:
        waypoints: Coordinates that define the route.
        bend: function that returns bends.
        straight: function that returns straight waveguides.
        taper: function that returns tapers.
        cross_section: spec.
        kwargs: cross_section settings.

    .. plot::
        :include-source:

        import gdsfactory as gf

        c = gf.Component("waypoints_sample")

        w = gf.components.straight()
        left = c << w
        right = c << w
        right.move((100, 80))

        obstacle = gf.components.rectangle(size=(100, 10))
        obstacle1 = c << obstacle
        obstacle2 = c << obstacle
        obstacle1.ymin = 40
        obstacle2.xmin = 25


        p0x, p0y = left.ports["o2"].center
        p1x, p1y = right.ports["o2"].center
        o = 10  # vertical offset to overcome bottom obstacle
        ytop = 20


        routes = gf.routing.get_route_from_waypoints(
            [
                (p0x, p0y),
                (p0x + o, p0y),
                (p0x + o, ytop),
                (p1x + o, ytop),
                (p1x + o, p1y),
                (p1x, p1y),
            ],
        )
        c.add(routes.references)
        c.plot()

    """
    if isinstance(cross_section, list | tuple):
        xs_list = []
        for element in cross_section:
            xs, angles = element
            xs = gf.get_cross_section(xs)
            xs = xs.copy(**kwargs)  # Shallow copy
            xs_list.append((xs, angles))
        x = cross_section = xs_list

    else:
        cross_section = gf.get_cross_section(cross_section)
        x = cross_section = cross_section.copy(**kwargs)

    if isinstance(cross_section, list):
        taper = None
    elif taper:
        x = gf.get_cross_section(cross_section, **kwargs)
        auto_widen = x.auto_widen
        width1 = x.width
        width2 = x.width_wide if auto_widen else width1
        taper_length = x.taper_length
        if auto_widen:
            taper = (
                taper(
                    length=taper_length,
                    width1=width1,
                    width2=width2,
                    cross_section=x,
                )
                if callable(taper)
                else taper
            )
        else:
            taper = None
    waypoints = np.array(waypoints)
    kwargs.pop("route_filter", "")

    return round_corners(
        points=waypoints,
        bend=bend,
        straight=straight,
        taper=taper,
        cross_section=x,
    )


get_route_from_waypoints_electrical = partial(
    get_route_from_waypoints, bend=wire_corner, cross_section="xs_metal_routing"
)

get_route_from_waypoints_electrical_m2 = partial(
    get_route_from_waypoints, bend=wire_corner, cross_section=metal2
)

get_route_from_waypoints_electrical_multilayer = partial(
    get_route_from_waypoints,
    bend=via_corner,
    cross_section=[(metal2, (0, 180)), (metal3, (90, 270))],
)


if __name__ == "__main__":
    c = gf.Component("demo")
    s = gf.c.straight()
    pt = c << s
    pb = c << s
    pt.d.move((50, 50))
    gf.routing.place_route(
        c,
        pb.ports["o2"],
        pt.ports["o1"],
        cross_section="xs_sc_auto_widen",
    )
    c.show()
