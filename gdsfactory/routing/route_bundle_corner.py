from __future__ import annotations

import numpy as np

from gdsfactory.component_layout import _rotate_points
from gdsfactory.port import Port
from gdsfactory.routing.manhattan import RouteError, generate_manhattan_waypoints
from gdsfactory.routing.path_length_matching import path_length_matched_points
from gdsfactory.routing.route_single import route_single
from gdsfactory.routing.validation import make_error_traces, validate_connections
from gdsfactory.typings import Route


def _groups(ports, cut, axis="X"):
    if axis == "Y":
        group1 = [p for p in ports if p.x <= cut]
        group2 = [p for p in ports if p.x > cut]
    else:
        group1 = [p for p in ports if p.y <= cut]
        group2 = [p for p in ports if p.y > cut]

    return group1, group2


def _transform_port(
    point, orientation, origin=(0, 0), rotation=None, x_reflection=False
):
    new_point = np.array(point)
    new_orientation = orientation

    if x_reflection:
        new_point[1] = -new_point[1]
        new_orientation = -orientation
    if rotation is not None:
        new_point = _rotate_points(new_point, angle=rotation, center=[0, 0])
        new_orientation += rotation
    if origin is not None:
        new_point = new_point + np.array(origin)
    new_orientation = new_orientation % 360

    return new_point, new_orientation


def _transform_ports(ports, rotation, origin=(0, 0), x_reflection=False):
    ports_transformed = []
    for p in ports:
        new_port = p.copy()
        new_center, new_orientation = _transform_port(
            p.center, p.orientation, origin, rotation, x_reflection
        )
        new_port.center = new_center
        new_port.new_orientation = new_orientation
        ports_transformed.append(new_port)

    return ports_transformed


def route_bundle_corner(
    ports1: list[Port],
    ports2: list[Port],
    separation: float = 5.0,
    path_length_match_loops: int | None = None,
    path_length_match_extra_length: float = 0.0,
    path_length_match_modify_segment_i: int = -2,
    enforce_port_ordering: bool = True,
    **kwargs,
) -> list[Route]:
    r"""Connect banks of ports with either 90Deg or 270Deg angle between them.

    Args:
        ports1: list of start ports.
        ports2: list of end ports.
        separation: in um.
        path_length_match_loops: optional number of loops for path length matching.
        path_length_match_extra_length: extra length (um) for path length matching.
        path_length_match_modify_segment_i: segment to increase length.
        enforce_port_ordering: If True, enforce that the ports are connected in the specific order.

    Returns:
        returns a list of elements which can be added to a component.
        e.g with default `route_single_from_waypoints`.


    ::

        Bend-types

        90 Deg bend
                   A1 A2      AN
                   | |  ...  |
                   | |      /
                  / /      /
                 / /      /
          B1 ----/ /    _/
          B2 -----/     /
                       /
            ...      _/
          BN --------/


        270 Deg bend
            /------------\
           /              \
          /  /-------\     \
         /  /         \     \
        |  /   /--\    |    |
        | /  /   |     | ...|
        | | /    B1    B2   BN
        | | |
        | \ \--- A1
        |  ----- A2
        |    ...
         \------ AN


    """
    _p1, _p2 = ports1, ports2
    if "straight" in kwargs:
        _ = kwargs.pop("straight")

    try:
        routes = _route_bundle_corner_waypoints(
            ports1,
            ports2,
            routing_func=generate_manhattan_waypoints,
            separation=separation,
            **kwargs,
        )
    except RouteError as e:
        return make_error_traces(ports1, ports2, str(e))
    if path_length_match_loops:
        routes = [np.array(route) for route in routes]
        routes = path_length_matched_points(
            routes,
            extra_length=path_length_match_extra_length,
            nb_loops=path_length_match_loops,
            modify_segment_i=path_length_match_modify_segment_i,
            **kwargs,
        )

    routes = [route_single(r, **kwargs) for r in routes]
    if enforce_port_ordering:
        routes = validate_connections(_p1, _p2, routes)
    return routes


def _route_bundle_corner_waypoints(
    ports1,
    ports2,
    routing_func=generate_manhattan_waypoints,
    separation: float = 5.0,
    **kwargs,
):
    ports1 = ports1.copy()
    ports2 = ports2.copy()
    nb_ports = len(ports1)
    connections = []

    for p in ports1:
        p.orientation = p.orientation % 360

    for p in ports2:
        p.orientation = p.orientation % 360

    port_angles1 = {p.orientation for p in ports1}
    port_angles2 = {p.orientation for p in ports2}

    assert len(ports2) == nb_ports, f"ports1 = {len(ports1)} must match {len(ports2)}"
    assert (
        len(port_angles1) <= 1
    ), f"ports1 should have the same angle. Got {port_angles1}"
    assert (
        len(port_angles2) <= 1
    ), f"ports2 should have the same angle. Got {port_angles2}"

    a_start = ports1[0].orientation
    a_end = ports2[0].orientation

    da = a_end - a_start
    assert (da) % 180 == 90, (
        "corner_bundle can  only route port banks between orthogonal axes."
        f"Got angles of {a_start} and {a_end}"
    )

    # Rotate all ports to be in the configuration where start_angle = 0

    origin = ports1[0].center
    ports1_transformed = _transform_ports(ports1, rotation=-a_start, origin=origin)
    ports2_transformed = _transform_ports(ports2, rotation=-a_start, origin=origin)

    # a_end_tr = ports2_transformed[0].orientation % 360

    ys = [p.y for p in ports1_transformed]
    ye = [p.y for p in ports2_transformed]

    xs = [p.x for p in ports1_transformed]
    xe = [p.x for p in ports2_transformed]

    are_above = max(ys) < min(ye)
    are_below = min(ys) > max(ye)

    are_right = max(xs) < min(xe)
    are_left = min(xs) > max(xe)

    assert are_above or are_below, "corner_bundle - ports should be below or above"
    assert are_right or are_left, "corner_bundle - ports should be left or right"

    start_sort_type = ["Y", "-X", "-Y", "X"]

    da = da % 360

    if da == 270:
        da = -90

    is_routable_270 = ((are_below and are_left) or (are_above and are_right)) and (
        da == -90
    )
    is_routable_90 = ((are_below and are_right) or (are_above and are_left)) and (
        da == 90
    )
    if not (is_routable_270 or is_routable_90):
        message = (
            f"Ports not routable with corner_bundle: da={da}; are_below={are_below};"
            f"are_above={are_above}; are_left={are_left}; are_right={are_right}. "
            "Consider applying a U turn first and then to to the 90Deg or 270Deg connection"
        )
        raise RouteError(message)

    end_sort_type = ["Y", "-X", "-Y", "X"] if da > 0 else ["-Y", "X", "Y", "-X"]
    start_angle_sort_index = a_start // 90
    end_angle_sort_index = a_end // 90

    # flip sort for a few specific cases:
    if are_above and are_left and da == 90:
        start_angle_sort_index = start_angle_sort_index + 2
        start_angle_sort_index = start_angle_sort_index % 4

    if are_below and are_right and da == 90:
        end_angle_sort_index = end_angle_sort_index + 2
        end_angle_sort_index = end_angle_sort_index % 4

    start_angle_sort_type = start_sort_type[int(start_angle_sort_index)]
    end_angle_sort_type = end_sort_type[int(end_angle_sort_index)]

    type2key = {
        "X": lambda p: p.x,
        "Y": lambda p: p.y,
        "-X": lambda p: -p.x,
        "-Y": lambda p: -p.y,
    }

    # print(a_start, a_end, start_angle_sort_type, end_angle_sort_type)
    ports1.sort(key=type2key[start_angle_sort_type])
    ports2.sort(key=type2key[end_angle_sort_type])

    kwargs.pop("start_straight_length", "")
    kwargs.pop("end_straight_length", "")
    for i, (p1, p2) in enumerate(zip(ports1, ports2)):
        conn = routing_func(
            p1,
            p2,
            start_straight_length=i * separation,
            end_straight_length=i * separation,
            **kwargs,
        )
        connections += [conn]
    return connections


if __name__ == "__main__":
    import gdsfactory as gf

    dy = -200
    orientation = 0
    layer = (1, 0)
    xs1 = [-100, -90, -80, -55, -35] + [200, 210, 240]
    axis = "X" if orientation in [0, 180] else "Y"
    pitch = 10.0
    N = len(xs1)
    xs2 = [50 + i * pitch for i in range(N)]

    a1 = orientation
    a2 = a1 + 180

    if axis == "X":
        ports1 = [
            Port(f"top_{i}", center=(0, xs1[i]), width=0.5, orientation=a1, layer=layer)
            for i in range(N)
        ]

        ports2 = [
            Port(
                f"bot_{i}",
                center=(dy, xs2[i]),
                width=0.5,
                orientation=a2,
                layer=layer,
            )
            for i in range(N)
        ]

    else:
        ports1 = [
            Port(f"top_{i}", center=(xs1[i], 0), width=0.5, orientation=a1, layer=layer)
            for i in range(N)
        ]

        ports2 = [
            Port(
                f"bot_{i}",
                center=(xs2[i], dy),
                width=0.5,
                orientation=a2,
                layer=layer,
            )
            for i in range(N)
        ]

    c = gf.Component()
    routes = gf.routing.route_bundle(
        c,
        ports1,
        ports2,
        bend=gf.components.bend_euler,
        radius=5,
        enforce_port_ordering=False,
    )