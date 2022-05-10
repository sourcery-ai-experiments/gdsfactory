import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.components.bend_s import bend_s
from gdsfactory.components.straight import straight as straight_function
from gdsfactory.types import ComponentSpec


@gf.cell
def delay_snake_sbend(
    length: float = 100.0,
    length1: float = 0.0,
    length4: float = 0.0,
    radius: float = 5.0,
    waveguide_spacing: float = 5.0,
    bend: ComponentSpec = bend_euler,
    sbend: ComponentSpec = bend_s,
    sbend_xsize: float = 100.0,
    straight: ComponentSpec = straight_function,
    **kwargs,
) -> Component:
    r"""Return compact Snake with sbend in the middle.
    Input port faces west and output port faces east.

    Args:
        length: total length.
        length1: first straight section length.
        length3: third straight section length.
        radius: u bend radius.
        waveguide_spacing: waveguide pitch.
        bend: bend spec.
        sbend: sbend spec.
        sbend_size: sbend size.
        straight: straight spec.
        kwargs: cross_section settings

    .. code::

                         length1
         <----------------------------
               length2    spacing    |
                _______              |
               |        \            |
               |          \          | bend1 radius
               |            \sbend   |
          bend2|              \      |
               |                \    |
               |                  \__|
               |
               ---------------------->----------->
                   length3              length4

        We adjust length2 and length3
    """

    c = Component()

    bend180_radius = (radius + waveguide_spacing) / 2
    bend = gf.get_component(bend, radius=bend180_radius, angle=180, **kwargs)
    sbend = gf.get_component(sbend, size=(sbend_xsize, radius), **kwargs)

    b1 = c << bend
    b2 = c << bend
    bs = c << sbend
    bs.mirror()

    length23 = (
        length - (2 * bend.info["length"] - bs.info["length"]) - length1 - length4
    )
    length2 = length23 / 2
    length3 = length23 / 2

    if length2 < 0:
        raise ValueError(
            f"length2 = {length2} < 0. You need to reduce length1 = {length1} "
            f"or length3 = {length3} or increase length = {length}"
        )

    straight1 = gf.get_component(straight, length=length1, **kwargs)
    straight2 = gf.get_component(straight, length=length2, **kwargs)
    straight3 = gf.get_component(straight, length=length3, **kwargs)
    straight4 = gf.get_component(straight, length=length4, **kwargs)

    s1 = c << straight1
    s2 = c << straight2
    s3 = c << straight3
    s4 = c << straight4

    b1.connect("o2", s1.ports["o2"])
    bs.connect("o2", b1.ports["o1"])

    s2.connect("o2", bs.ports["o1"])

    b2.connect("o1", s2.ports["o1"])
    s3.connect("o1", b2.ports["o2"])
    s4.connect("o1", s3.ports["o2"])

    c.add_port("o1", port=s1.ports["o1"])
    c.add_port("o2", port=s4.ports["o2"])

    c.info["min_bend_radius"] = sbend.info["min_bend_radius"]
    c.info["bend180_radius"] = bend180_radius
    return c


if __name__ == "__main__":
    c = gf.grid(
        [
            delay_snake_sbend(length=length, print_min_bend_radius=True)
            for length in [500, 3000]
        ]
    )
    c.show()
