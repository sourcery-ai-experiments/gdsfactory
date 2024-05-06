from __future__ import annotations

import jsondiff
import numpy as np

import gdsfactory as gf


def test_waveguide_setting() -> None:
    x = gf.cross_section.cross_section(width=2)
    assert x.width == 2


def test_settings_different() -> None:
    strip1 = gf.cross_section.strip()
    strip2 = gf.cross_section.strip(layer=(2, 0))
    assert strip1 != strip2


def test_transition_names() -> None:
    layer = (1, 0)
    s1 = gf.Section(width=5, layer=layer, port_names=("o1", "o2"))
    s2 = gf.Section(width=50, layer=layer, port_names=("o1", "o2"))

    xs1 = gf.CrossSection(sections=(s1,))
    xs2 = gf.CrossSection(sections=(s2,))

    trans12 = gf.path.transition(
        cross_section1=xs1, cross_section2=xs2, width_type="linear"
    )
    trans21 = gf.path.transition(
        cross_section1=xs2, cross_section2=xs1, width_type="linear"
    )

    WG4Path = gf.Path()
    WG4Path.append(gf.path.straight(length=100, npoints=2))
    c1 = gf.path.extrude_transition(WG4Path, trans12)
    c2 = gf.path.extrude_transition(WG4Path, trans21)
    assert c1.name != c2.name


def test_copy() -> None:
    s = gf.Section(width=0.5, offset=0, layer=(3, 0), port_names=("in", "out"))
    x1 = gf.CrossSection(sections=(s,))
    x2 = x1.copy()
    d = jsondiff.diff(x1.model_dump(), x2.model_dump())
    assert len(d) == 0, d


def multi_layer_cs(width: float = 1):
    width1 = width
    width2 = width + 2
    s2 = gf.Section(width=width2, layer=(5, 21))
    cs = gf.cross_section.cross_section(width=width1, layer=(2, 21), sections=[s2])
    return cs


def many_sections_per_layer_cs(width: float = 1):
    width1 = width
    width2 = width + 2
    s2 = gf.Section(width=width2, layer=(5, 21))
    s3 = gf.Section(width=1, offset=width2 / 2 + 1, layer=(6, 21), name="l3_upper")
    s4 = gf.Section(width=1, offset=-(width2 / 2 + 1), layer=(6, 21), name="l3_lower")
    cs = gf.cross_section.cross_section(
        width=width1, layer=(2, 21), sections=[s2, s3, s4]
    )
    return cs


def other_many_sections_per_layer_cs(width: float = 1):
    width1 = width
    s3 = gf.Section(width=1, offset=width1 / 2 + 1, layer=(6, 21), name="l3_upper")
    s4 = gf.Section(width=1, offset=-(width1 / 2 + 1), layer=(6, 21), name="l3_lower")
    cs = gf.cross_section.cross_section(width=width1, layer=(2, 21), sections=[s3, s4])
    return cs


def test_get_cross_section_modified_width():
    pdk = gf.get_active_pdk()
    # register our test cross section
    pdk.register_cross_sections(test_multi_layer_cs=multi_layer_cs)
    cs_spec = {"cross_section": "test_multi_layer_cs", "settings": {"width": 4}}

    c = gf.get_component("straight", cross_section=cs_spec, length=10)
    layer1_area = c.extract([(2, 21)]).area()
    layer2_area = c.extract([(5, 21)]).area()

    assert layer1_area == 4 * 10
    assert layer2_area == 6 * 10

    # teardown: remove the test cross section
    pdk.cross_sections.pop("test_multi_layer_cs")


def test_extrude_transition_multi_section():
    cs1 = many_sections_per_layer_cs(width=1)
    cs2 = other_many_sections_per_layer_cs(width=5)
    transition = gf.cross_section.Transition(cross_section1=cs1, cross_section2=cs2)
    p = gf.path.straight(10)

    c = gf.path.extrude_transition(transition=transition, p=p)

    layer1_area = c.extract([(2, 21)]).area()
    layer2_area = c.extract([(5, 21)]).area()
    layer3_area = c.extract([(6, 21)]).area()

    assert layer1_area == (1 + 5) / 2 * 10
    assert layer2_area == 0
    assert np.isclose(layer3_area, 1 * 10 * 2)


def test_get_cross_sections_empty_input() -> None:
    xs = gf.get_cross_sections([])
    assert isinstance(xs, dict)
    assert len(xs) == 0


def test_cross_section_mirror() -> None:
    xs_pn = gf.cross_section.xs_pn
    xs_np = xs_pn.mirror()

    for s1, s2 in zip(xs_pn.sections, xs_np.sections):
        assert s1.offset == -s2.offset, f"{s1.offset} != {s2.offset}"


def test_extrude_transition_component():
    w1 = 1
    w2 = 5
    x1 = gf.get_cross_section("xs_sc", width=w1)
    x2 = gf.get_cross_section("xs_sc", width=w2)
    trans = gf.path.transition(x1, x2)
    c = gf.components.bend_euler(radius=10, cross_section=trans)
    assert c["o1"].width == w1
    assert c["o2"].width == w2


def test_cross_section_variable_width_section():
    """Make sure serialization for Section with variable width is different for different width functions.
    This will fail if @gf.cell is reusing the first Component."""
    import numpy as np

    def get_custom_width_func(n: int = 1):
        def _width_func(t):
            return 3 + np.cos(2 * np.pi * t * n)

        return _width_func

    P = gf.path.straight(length=40, npoints=100)

    s1 = gf.Section(
        width=0, width_function=get_custom_width_func(n=1), offset=0, layer=(1, 0)
    )
    s2 = gf.Section(
        width=0, width_function=get_custom_width_func(n=5), offset=0, layer=(1, 0)
    )

    X1 = gf.CrossSection(sections=(s1,))
    X2 = gf.CrossSection(sections=(s2,))

    p1 = gf.path.extrude(P, cross_section=X1)
    p2 = gf.path.extrude(P, cross_section=X2)

    assert p1 is not p2
