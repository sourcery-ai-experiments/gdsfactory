from __future__ import annotations

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components import bend_euler, straight
from gdsfactory.components.taper_cross_section import taper_cross_section_linear
from gdsfactory.cross_section import strip
from gdsfactory.typings import (
    ComponentFactory,
    ComponentSpec,
    CrossSectionSpec,
    Floats,
    LayerSpec,
)


@gf.cell
def straight_heater_meander(
    length: float = 300.0,
    spacing: float = 2.0,
    cross_section: CrossSectionSpec = strip,
    heater_width: float = 2.5,
    extension_length: float = 15.0,
    layer_heater: LayerSpec | None = "HEATER",
    radius: float | None = None,
    via_stack: ComponentSpec | None = "via_stack_heater_mtop",
    port_orientation1: int | None = None,
    port_orientation2: int | None = None,
    heater_taper_length: float | None = 10.0,
    straight_widths: Floats | None = (0.8, 0.9, 0.8),
    taper_length: float = 10,
    n: int | None = None,
    straight: ComponentFactory = straight,
    bend: ComponentFactory = bend_euler,
    taper: ComponentFactory = taper_cross_section_linear,
) -> Component:
    """Returns a meander based heater.

    based on SungWon Chung, Makoto Nakai, and Hossein Hashemi,
    Low-power thermo-optic silicon modulator for large-scale photonic integrated systems
    Opt. Express 27, 13430-13459 (2019)
    https://www.osapublishing.org/oe/abstract.cfm?URI=oe-27-9-13430

    Args:
        length: total length of the optical path.
        spacing: waveguide spacing (center to center).
        cross_section: for waveguide.
        heater_width: for heater.
        extension_length: of input and output optical ports.
        layer_heater: for top heater, if None, it does not add a heater.
        radius: for the meander bends.
        via_stack: for the heater to via_stack metal.
        port_orientation1: in degrees. None adds all orientations.
        port_orientation2: in degrees. None adds all orientations.
        heater_taper_length: minimizes current concentrations from heater to via_stack.
        straight_widths: widths of the straight sections.
        taper_length: from the cross_section.
        n: Optional number of passes. If None, it is calculated from the straight_widths.
        straight: ComponentFactory for the straight sections.
        bend: ComponentFactory for the bend sections.
        taper: ComponentFactory for the photonic taper sections.
    """
    if n and straight_widths:
        raise ValueError("n and straight_widths are mutually exclusive")

    rows = n or len(straight_widths)
    c = gf.Component()
    x = gf.get_cross_section(cross_section)

    radius = radius or x.radius

    if n and not straight_widths:
        if n % 2 == 0:
            raise ValueError(f"n={n} should be odd")
        straight_widths = [x.width] * n

    p1 = gf.Port(
        name="p1",
        center=(0, 0),
        orientation=0,
        cross_section=x,
        layer=x.layer,
        width=x.width,
    )
    p2 = gf.Port(
        name="p2",
        center=(0, spacing),
        orientation=0,
        cross_section=x,
        layer=x.layer,
        width=x.width,
    )
    route = gf.routing.get_route(
        p1, p2, radius=radius, cross_section=x, straight=straight, bend=bend
    )

    cross_section2 = cross_section

    straight_length = gf.snap.snap_to_grid(
        (length - (rows - 1) * route.length) / rows, grid_factor=2
    )
    ports = {}

    ##############
    # Straights
    ##############
    for row, straight_width in enumerate(straight_widths):
        cross_section1 = gf.get_cross_section(cross_section, width=straight_width)
        straight_i = gf.get_component(
            straight,
            length=straight_length - 2 * taper_length,
            cross_section=cross_section1,
        )

        taper_lin = partial(
            taper,
            cross_section1=cross_section1,
            cross_section2=cross_section2,
            length=taper_length,
        )

        straight_with_tapers = gf.c.extend_ports(straight_i, extension=taper_lin)

        straight_ref = c << straight_with_tapers
        straight_ref.y = row * spacing
        ports[f"o1_{row+1}"] = straight_ref.ports["o1"]
        ports[f"o2_{row+1}"] = straight_ref.ports["o2"]

    ##############
    # loopbacks
    ##############
    for row in range(1, rows, 2):
        extra_length = 3 * (rows - row - 1) / 2 * radius
        straight_extra_length = gf.get_component(
            straight, length=extra_length, cross_section=cross_section
        )
        extra_straight1 = c << straight_extra_length
        extra_straight2 = c << straight_extra_length
        extra_straight1.connect("o1", ports[f"o1_{row+1}"])
        extra_straight2.connect("o1", ports[f"o1_{row+2}"])

        route = gf.routing.get_route(
            extra_straight1.ports["o2"],
            extra_straight2.ports["o2"],
            radius=radius,
            cross_section=cross_section,
            straight=straight,
            bend=bend,
        )
        c.add(route.references)

        extra_length = 3 * (row - 1) / 2 * radius
        straight_extra_length = gf.get_component(
            straight, length=extra_length, cross_section=cross_section
        )

        extra_straight1 = c << straight_extra_length
        extra_straight2 = c << straight_extra_length
        extra_straight1.connect("o1", ports[f"o2_{row+1}"])
        extra_straight2.connect("o1", ports[f"o2_{row}"])

        route = gf.routing.get_route(
            extra_straight1.ports["o2"],
            extra_straight2.ports["o2"],
            radius=radius,
            cross_section=cross_section,
            straight=straight,
            bend=bend,
        )
        c.add(route.references)

    straight_extension = gf.get_component(
        straight, length=extension_length, cross_section=cross_section
    )
    straight1 = c << straight_extension
    straight2 = c << straight_extension
    straight1.connect("o2", ports["o1_1"])
    straight2.connect("o1", ports[f"o2_{rows}"])

    c.add_port("o1", port=straight1.ports["o1"])
    c.add_port("o2", port=straight2.ports["o2"])

    if layer_heater:
        heater_cross_section = partial(
            gf.cross_section.cross_section, width=heater_width, layer=layer_heater
        )

        heater = c << gf.c.straight(
            length=straight_length,
            cross_section=heater_cross_section,
        )
        heater.movey(spacing * (rows // 2))

    if layer_heater and via_stack:
        via = via_stacke = via_stackw = gf.get_component(via_stack)
        dx = via_stackw.get_ports_xsize() / 2 + heater_taper_length or 0
        via_stack_west_center = heater.size_info.cw - (dx, 0)
        via_stack_east_center = heater.size_info.ce + (dx, 0)

        via_stack_west = c << via_stackw
        via_stack_east = c << via_stacke
        via_stack_west.move(via_stack_west_center)
        via_stack_east.move(via_stack_east_center)

        valid_orientations = {p.orientation for p in via.ports.values()}
        p1 = via_stack_west.get_ports_list(orientation=port_orientation1)
        p2 = via_stack_east.get_ports_list(orientation=port_orientation2)

        if not p1:
            raise ValueError(
                f"No ports for port_orientation1 {port_orientation1} in {valid_orientations}"
            )
        if not p2:
            raise ValueError(
                f"No ports for port_orientation2 {port_orientation2} in {valid_orientations}"
            )

        c.add_ports(p1, prefix="l_")
        c.add_ports(p2, prefix="r_")

        if heater_taper_length:
            taper = gf.c.taper(
                cross_section=heater_cross_section,
                width1=via_stackw.ports["e1"].width,
                width2=heater_width,
                length=heater_taper_length,
                port_types=("electrical", "electrical"),
            )
            taper1 = c << taper
            taper2 = c << taper

            taper1.connect("o2", heater.ports["o1"], allow_type_mismatch=True)
            taper2.connect("o2", heater.ports["o2"], allow_type_mismatch=True)

            via_stack_west.connect(
                "e3",
                taper1.ports["o1"],
                allow_layer_mismatch=True,
                allow_type_mismatch=True,
            )
            via_stack_east.connect(
                "e1",
                taper2.ports["o1"],
                allow_layer_mismatch=True,
                allow_type_mismatch=True,
            )

    return c


if __name__ == "__main__":
    # c = straight_heater_meander(
    #     straight_widths=(0.5, 0.5, 0.5),
    #     n=3,
    #     taper_length=10,
    #     # taper_length=10,
    #     length=10000,
    #     layer_heater=None,
    #     # taper=gf.c.taper_cross_section_linear
    #     # taper=None,
    #     # port_orientation1=0
    #     # cross_section=partial(gf.cross_section.strip, width=0.8),
    # )
    c = straight_heater_meander()
    c.show(show_ports=True)
