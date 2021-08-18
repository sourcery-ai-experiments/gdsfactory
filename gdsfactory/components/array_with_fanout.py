from typing import Optional

from gdsfactory.cell import cell
from gdsfactory.component import Component
from gdsfactory.components.array import array
from gdsfactory.components.bend_euler import bend_euler
from gdsfactory.components.pad import pad
from gdsfactory.components.straight import straight
from gdsfactory.cross_section import strip
from gdsfactory.port import auto_rename_ports
from gdsfactory.routing.sort_ports import sort_ports_x
from gdsfactory.types import (
    ComponentFactory,
    ComponentOrFactory,
    CrossSectionFactory,
    PortName,
)


@cell
def array_with_fanout(
    component: ComponentOrFactory = pad,
    n: int = 3,
    pitch: float = 150.0,
    waveguide_pitch: float = 10.0,
    start_straight: float = 5.0,
    end_straight: float = 40.0,
    radius: float = 5.0,
    component_port_name: PortName = 4,
    bend: ComponentFactory = bend_euler,
    bend_port_name1: Optional[PortName] = None,
    bend_port_name2: Optional[PortName] = None,
    cross_section: CrossSectionFactory = strip,
    **kwargs,
) -> Component:
    """Returns an array of components in X axis
    with fanout waveguides facing west

    Args:
        component: to replicate
        n: number of components
        pitch: float
        waveguide_pitch: for fanout
        start_straight: length of the start of the straight
        end_straight: lenght of the straight at the end
        radius: bend radius
        component_port_name:
        bend:
        bend_port_name1:
        bend_port_name2:
        cross_section: cross_section definition
        **kwargs: cross_section settings
    """
    c = Component()
    component = component() if callable(component) else component
    bend = bend(radius=radius, cross_section=cross_section, **kwargs)

    bend_ports = bend.get_ports_list()
    bend_ports = sort_ports_x(bend_ports)
    bend_ports.reverse()
    bend_port_name1 = bend_port_name1 or bend_ports[0].name
    bend_port_name2 = bend_port_name2 or bend_ports[1].name

    for col in range(n):
        ref = component.ref()
        ref.x = col * pitch
        c.add(ref)
        ylength = col * waveguide_pitch + start_straight
        xlength = col * pitch + end_straight
        straight_ref = c << straight(
            length=ylength, cross_section=cross_section, **kwargs
        )
        straight_ref.connect(2, ref.ports[component_port_name])

        bend_ref = c.add_ref(bend)
        bend_ref.connect(bend_port_name1, straight_ref.ports[1])
        straightx_ref = c << straight(
            length=xlength, cross_section=cross_section, **kwargs
        )
        straightx_ref.connect(2, bend_ref.ports[bend_port_name2])
        c.add_port(f"W_{col}", port=straightx_ref.ports[1])
    auto_rename_ports(c)
    return c


@cell
def array_with_fanout_2d(
    pitch: float = 150.0,
    pitch_x: Optional[float] = None,
    pitch_y: Optional[float] = None,
    cols: int = 3,
    rows: int = 2,
    **kwargs,
) -> Component:
    """Returns 2D array with fanout waveguides facing west.

    Args:
        pitch: 2D pitch
        pitch_x: defaults to pitch
        pitch_y: defaults to pitch
        cols:
        rows:
        kwargs:
            component: to replicate
            n: number of components
            pitch: float
            waveguide_pitch: for fanout
            start_straight: length of the start of the straight
            end_straight: lenght of the straight at the end
            radius: bend radius
            cross_section: cross_section factory
            component_port_name:
            bend_port_name1:
            bend_port_name2:
            **kwargs
    """
    pitch_y = pitch_y or pitch
    pitch_x = pitch_x or pitch
    row = array_with_fanout(n=cols, pitch=pitch_x, **kwargs)
    return array(component=row, n=rows, pitch=pitch_y, axis="y")


if __name__ == "__main__":

    # c1 = gf.components.pad()
    # c2 = array(component=c1, pitch=150, n=2)
    # print(c2.ports.keys())

    c2 = array_with_fanout(
        n=3,
        waveguide_pitch=20,
        # bend=gf.components.wire_corner,
        # layer=(2, 0),
        # width=10,
        # radius=11,
    )
    c2.show(show_ports=True)
