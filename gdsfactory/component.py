"""Component is a canvas for geometry.

Adapted from PHIDL https://github.com/amccaugh/phidl/ by Adam McCaughan
"""

from __future__ import annotations

import datetime
import hashlib
import itertools
import math
import os
import pathlib
import uuid
import warnings
from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import gdstk
import numpy as np
import orjson
import yaml
from omegaconf import DictConfig

from gdsfactory import snap
from gdsfactory.component_layout import (
    CellSettings,
    ComponentSpec,
    Info,
    Label,
    _align,
    _distribute,
    _GeometryHelper,
    _parse_layer,
    get_polygons,
    pprint_ports,
)
from gdsfactory.component_reference import ComponentReference, SizeInfo
from gdsfactory.config import CONF, GDSDIR_TEMP, logger
from gdsfactory.name import get_name_short
from gdsfactory.polygon import Polygon
from gdsfactory.port import (
    Port,
    auto_rename_ports,
    auto_rename_ports_counter_clockwise,
    auto_rename_ports_layer_orientation,
    auto_rename_ports_orientation,
    map_ports_layer_to_orientation,
    map_ports_to_orientation_ccw,
    map_ports_to_orientation_cw,
    select_ports,
)
from gdsfactory.serialization import clean_dict
from gdsfactory.snap import snap_to_grid2x

if TYPE_CHECKING:
    from gdsfactory.technology import LayerStack, LayerViews
    from gdsfactory.typings import (
        Coordinate,
        CrossSection,
        CrossSectionSpec,
        Float2,
        Layer,
        Layers,
        LayerSpec,
        PathType,
        Tuple,
    )

valid_plotters = ["matplotlib", "klayout", "kweb"]
Axis = Literal["x", "y"]
os.environ["KWEB_FILESLOCATION"] = str(GDSDIR_TEMP)


class UncachedComponentWarning(UserWarning):
    pass


class UncachedComponentError(ValueError):
    pass


class MutabilityError(ValueError):
    pass


def _get_dependencies(component, references_set) -> None:
    for ref in component.references:
        references_set.add(ref.ref_cell)
        _get_dependencies(ref.ref_cell, references_set)


mutability_error_message = """
You cannot modify a Component after creation as it will affect all of its instances.

Create a new Component and add a reference to it.

For example:

# BAD
c = gf.components.bend_euler()
c.add_ref(gf.components.mzi())

# GOOD
c = gf.Component()
c.add_ref(gf.components.bend_euler())
c.add_ref(gf.components.mzi())
"""

move_error_message = """
You cannot move a Component. You can create a new Component, add a reference to the other Component and then move the reference.

For example:

# BAD
c = gf.components.straight()
c.xmin = 10

# GOOD
c = gf.Component()
ref = c.add_ref(gf.components.straight()) # or ref = c << gf.components.straight()
ref.xmin = 10
"""

_timestamp2019 = datetime.datetime.fromtimestamp(1572014192.8273)

# Global dictionary to hold counters for each name
name_counters = Counter()


valid_anchor_point_keywords = [
    "ce",
    "cw",
    "nc",
    "ne",
    "nw",
    "sc",
    "se",
    "sw",
    "center",
    "cc",
]
valid_anchor_value_keywords = [
    "south",
    "west",
    "east",
    "north",
]
# refer to a singular (x or y) value

valid_anchors = valid_anchor_point_keywords + valid_anchor_value_keywords
# full set of valid anchor keywords (either referring to points or values)


def _rnd(arr, precision=1e-4):
    arr = np.ascontiguousarray(arr)
    ndigits = round(-math.log10(precision))
    return np.ascontiguousarray(arr.round(ndigits) / precision, dtype=np.int64)


class Component(_GeometryHelper):
    """A Component is an empty canvas where you add polygons, references and ports \
            (to connect to other components).

    - stores settings that you use to build the component
    - stores info that you want to use
    - can return ports by type (optical, electrical ...)
    - can return netlist for circuit simulation
    - can write to GDS, OASIS
    - can show in KLayout, matplotlib, 3D
    - can return copy, mirror, flattened (no references)

    Args:
        name: component_name. Use @cell decorator for auto-naming.
        with_uuid: adds unique identifier.

    Properties:
        info: dictionary that includes
            - derived properties
            - external metadata (test_protocol, docs, ...)
            - simulation_settings
            - function_name
            - name: for the component

        settings:
            full: full settings passed to the function to create component.
            changed: changed settings.
            default: default component settings.
            child: dict info from the children, if any.
    """

    def __init__(
        self,
        name: str = "Unnamed",
        with_uuid: bool = False,
        max_name_length: int | None = None,
    ) -> None:
        """Initialize the Component object.

        Args:
            name: component_name. Use @cell decorator for auto-naming.
            with_uuid: adds unique identifier.
            max_name_length: maximum number of characters for component name.
        """

        self.uid = str(uuid.uuid4())[:8]

        if with_uuid:
            warnings.warn("with_uuid is deprecated. Use @cell decorator instead.")
            name += f"_{self.uid}"

        if name == "Unnamed":
            name = f"Unnamed_{self.uid}"

        name_counters[name] += 1
        if name_counters[name] > 1:
            name = f"{name}${name_counters[name]-1}"

        self._cell = gdstk.Cell(name)
        self.rename(name, max_name_length=max_name_length)
        self.info: Info = Info()

        self.settings: CellSettings = CellSettings()
        self._locked = False
        self._get_child_name = False
        self._reference_names_counter = Counter()
        self._reference_names_used = set()
        self._named_references = {}
        self._references = []
        self.function_name = ""
        self.module = ""

        self.ports = {}

        self.child = None

    def simplify(self, tolerance: float = 1e-3):
        """Removes points from the polygon but does not change the polygon
        shape by more than `tolerance` from the original. Uses the
        Ramer-Douglas-Peucker algorithm.

        Args:
            tolerance: Tolerance value for the simplification algorithm.  All points that
                can be removed without changing the resulting polygon by more than
                the value listed here will be removed. Also known as `epsilon` here
                https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
        """
        c = Component(f"{self.name}_simplified_{tolerance:.0e}")
        polygons = self.get_polygons(by_spec=True, as_array=True)

        for layer, points in polygons.items():
            for p in points:
                c.add_polygon(points=_simplify(p, tolerance=tolerance), layer=layer)

        return c

    @property
    def references(self):
        return self._references

    @property
    def polygons(self) -> list[Polygon]:
        return self._cell.polygons

    def area(self, layer: LayerSpec | None = None) -> float:
        """Returns the area of the component.

        Args:
            layer: if None returns the area of the component.
                If layer is specified returns the area of the component in that layer.
        """
        if not layer:
            return self._cell.area(False)
        from gdsfactory.pdk import get_layer

        layer = get_layer(layer)
        layer_to_area = self._cell.area(True)
        return layer_to_area[layer]

    @property
    def labels(self) -> list[Label]:
        return self._cell.labels

    @property
    def paths(self):
        return self._cell.paths

    @property
    def name(self) -> str:
        return self._cell.name

    @name.setter
    def name(self, name) -> None:
        self.rename(name)

    def rename(self, name: str, cache: bool = True, max_name_length: int | None = None):
        from gdsfactory.cell import CACHE, remove_from_cache

        if max_name_length is None:
            max_name_length = CONF.max_name_length

        if len(name) > max_name_length:
            name_short = get_name_short(name, max_name_length=max_name_length)
            warnings.warn(
                f" {name} is too long. Max length is {max_name_length}. Renaming to {name_short}",
                stacklevel=2,
            )
            name = name_short

        if self.name != name:
            # if this component is registered under its old name in the cache, remove it
            old_name = self.name
            if CACHE.get(old_name) is self:
                remove_from_cache(self.name)

            # cache the new name and add to counter if specified
            if cache is True:
                name_counters[name] += 1
                if name_counters[name] > 1:
                    name = f"{name}${name_counters[name]-1}"
                CACHE[name] = self

        self._cell.name = name

    def __iter__(self):
        """You can iterate over polygons, paths, labels and references."""
        return itertools.chain(self.polygons, self.paths, self.labels, self.references)

    def get_polygon_enclosure(self) -> Polygon:
        """Returns Polygon enclosure."""
        import shapely

        points = self._cell.convex_hull()
        return shapely.Polygon(points)

    def get_polygon_bbox(
        self,
        default: float = 0.0,
        top: float | None = None,
        bottom: float | None = None,
        right: float | None = None,
        left: float | None = None,
    ) -> Polygon:
        """Returns shapely Polygon with bounding box.

        Args:
            default: default padding in um.
            top: north padding in um.
            bottom: south padding in um.
            right: east padding in um.
            left: west padding in um.
        """
        import shapely

        (xmin, ymin), (xmax, ymax) = self.bbox
        top = top if top is not None else default
        bottom = bottom if bottom is not None else default
        right = right if right is not None else default
        left = left if left is not None else default
        points = [
            [xmin - left, ymin - bottom],
            [xmax + right, ymin - bottom],
            [xmax + right, ymax + top],
            [xmin - left, ymax + top],
        ]
        return shapely.Polygon(points)

    def get_polygons(
        self,
        by_spec: bool | tuple[int, int] = False,
        depth: int | None = None,
        include_paths: bool = True,
        as_array: bool = True,
        as_shapely: bool = False,
        as_shapely_merged: bool = False,
    ) -> list[Polygon] | dict[tuple[int, int], list[Polygon]]:
        """Return a list of polygons in this cell.

        Args:
            by_spec: bool or layer
                If True, the return value is a dictionary with the
                polygons of each individual pair (layer, datatype), which
                are used as keys.  If set to a tuple of (layer, datatype),
                only polygons with that specification are returned.
            depth: integer or None
                If not None, defines from how many reference levels to
                retrieve polygons.  References below this level will result
                in a bounding box.  If `by_spec` is True the key will be the
                name of this cell.
            include_paths: If True, polygonal representation of paths are also included in the result.
            as_array: when as_array=false, return the Polygon objects instead.
                polygon objects have more information (especially when by_spec=False) and are faster to retrieve.
            as_shapely: returns shapely polygons.
            as_shapely_merged: returns a shapely polygonize.

        Returns
            out: list of array-like[N][2] or dictionary
                List containing the coordinates of the vertices of each
                polygon, or dictionary with with the list of polygons (if
                `by_spec` is True).

        Note:
            Instances of `FlexPath` and `RobustPath` are also included in
            the result by computing their polygonal boundary.
        """
        return get_polygons(
            instance=self,
            by_spec=by_spec,
            depth=depth,
            include_paths=include_paths,
            as_array=as_array,
            as_shapely=as_shapely,
            as_shapely_merged=as_shapely_merged,
        )

    def get_dependencies(self, recursive: bool = False) -> list[Component]:
        """Return a list of Components referenced by this Component.

        Args:
            recursive: If True returns dependencies recursively.

        """
        if not recursive:
            return list({ref.parent for ref in self.references})

        references_set = set()
        _get_dependencies(self, references_set=references_set)
        return list(references_set)

    def __getitem__(self, key: str | int) -> Port:
        """Access reference ports."""
        if isinstance(key, int):
            key = list(self.ports.keys())[key]

        if key not in self.ports:
            ports = list(self.ports.keys())
            raise ValueError(f"{key!r} not in {ports}")

        return self.ports[key]

    def __lshift__(self, element) -> ComponentReference:
        """Convenience operator equivalent to add_ref()."""
        return self.add_ref(element)

    def __setitem__(self, key, element):
        """Allow adding polygons and cell references.

        like D['arc3'] = pg.arc()

        Args:
            key: Alias name.
            element: Object that will be accessible by alias name.

        """
        if isinstance(element, ComponentReference | Polygon):
            self.named_references[key] = element
        else:
            raise ValueError(
                f"Tried to assign alias {key!r} in Component {self.name!r},"
                "but failed because the item was not a ComponentReference"
            )

    @classmethod
    def __get_validators__(cls):
        """Get validators for the Component object."""
        yield cls.validate

    @classmethod
    def validate(cls, v, _info):
        """Pydantic assumes component is valid if the following are true.

        - name characters < pdk.cell_decorator_settings.max_name_length
        - is not empty (has references or polygons)
        """
        from gdsfactory.pdk import get_active_pdk

        pdk = get_active_pdk()

        max_name_length = pdk.cell_decorator_settings.max_name_length
        assert isinstance(
            v, Component
        ), f"TypeError, Got {type(v)}, expecting Component"
        assert (
            len(v.name) <= max_name_length
        ), f"name `{v.name}` {len(v.name)} > {max_name_length} "
        return v

    @property
    def named_references(self):
        return self._named_references

    def add_label(
        self,
        text: str = "hello",
        position: tuple[float, float] = (0.0, 0.0),
        magnification: float = 1.0,
        rotation: float = 0,
        anchor: str = "o",
        layer: LayerSpec = "TEXT",
        x_reflection: bool = False,
    ) -> Label:
        """Adds Label to the Component.

        Args:
            text: Label text.
            position: x-, y-coordinates of the Label location.
            magnification: Magnification factor for the Label text.
            rotation: Angle rotation of the Label text.
            anchor: {'n', 'e', 's', 'w', 'o', 'ne', 'nw', ...}
                Position of the anchor relative to the text.
            layer: Specific layer(s) to put Label on.
            x_reflection: True reflects across the horizontal axis before rotation.
        """
        from gdsfactory.pdk import get_layer

        layer = get_layer(layer)

        gds_layer, gds_datatype = layer

        if not isinstance(text, str):
            text = text
        label = Label(
            text=text,
            origin=position,
            anchor=anchor,
            magnification=magnification,
            rotation=rotation,
            layer=gds_layer,
            texttype=gds_datatype,
            x_reflection=x_reflection,
        )
        self.add(label)
        return label

    @property
    def bbox(self):
        """Returns the bounding box of the ComponentReference."""
        bbox = self._cell.bounding_box()
        if bbox is None:
            bbox = ((0, 0), (0, 0))
        return np.array(bbox)

    @property
    def ports_layer(self) -> dict[str, str]:
        """Returns a mapping from layer0_layer1_E0: portName."""
        return map_ports_layer_to_orientation(self.ports)

    def port_by_orientation_cw(self, key: str, **kwargs):
        """Returns port by indexing them clockwise."""
        m = map_ports_to_orientation_cw(self.ports, **kwargs)
        if key not in m:
            raise KeyError(f"{key} not in {list(m.keys())}")
        key2 = m[key]
        return self.ports[key2]

    def port_by_orientation_ccw(self, key: str, **kwargs):
        """Returns port by indexing them clockwise."""
        m = map_ports_to_orientation_ccw(self.ports, **kwargs)
        if key not in m:
            raise KeyError(f"{key} not in {list(m.keys())}")
        key2 = m[key]
        return self.ports[key2]

    def get_ports_xsize(self, **kwargs) -> float:
        """Returns xdistance from east to west ports.

        Keyword Args:
            layer: port GDS layer.
            prefix: with in port name.
            orientation: in degrees.
            width: port width.
            layers_excluded: List of layers to exclude.
            port_type: optical, electrical, ...
        """
        ports_cw = self.get_ports_list(clockwise=True, **kwargs)
        ports_ccw = self.get_ports_list(clockwise=False, **kwargs)
        return ports_ccw[0].x - ports_cw[0].x

    def get_ports_ysize(self, **kwargs) -> float:
        """Returns ydistance from east to west ports.

        Keyword Args:
            layer: port GDS layer.
            prefix: with in port name.
            orientation: in degrees.
            width: port width (um).
            layers_excluded: List of layers to exclude.
            port_type: optical, electrical, ...
        """
        ports_cw = self.get_ports_list(clockwise=True, **kwargs)
        ports_ccw = self.get_ports_list(clockwise=False, **kwargs)
        return ports_ccw[0].y - ports_cw[0].y

    def plot_netlist(
        self, with_labels: bool = True, font_weight: str = "normal", **kwargs
    ):
        """Plots a netlist graph with networkx.

        Args:
            with_labels: add label to each node.
            font_weight: normal, bold.
            **kwargs: keyword arguments for the get_netlist function
        """
        import matplotlib.pyplot as plt
        import networkx as nx

        plt.figure()
        netlist = self.get_netlist(**kwargs)
        connections = netlist["connections"]
        placements = netlist["placements"]
        G = nx.Graph()
        G.add_edges_from(
            [
                (",".join(k.split(",")[:-1]), ",".join(v.split(",")[:-1]))
                for k, v in connections.items()
            ]
        )
        pos = {k: (v["x"], v["y"]) for k, v in placements.items()}
        labels = {k: ",".join(k.split(",")[:1]) for k in placements.keys()}
        nx.draw(
            G,
            with_labels=with_labels,
            font_weight=font_weight,
            labels=labels,
            pos=pos,
        )
        return G

    def plot_netlist_flat(
        self, with_labels: bool = True, font_weight: str = "normal", **kwargs
    ):
        """Plots a netlist graph with networkx.

        Args:
            flat: if true, will plot the flat netlist
            with_labels: add label to each node.
            font_weight: normal, bold.
            **kwargs: keyword arguments for the get_netlist function
        """
        import matplotlib.pyplot as plt
        import networkx as nx

        plt.figure()
        netlist = self.get_netlist_flat(**kwargs)
        connections = netlist["connections"]
        placements = netlist["placements"]
        connections_list = []
        for k, v_list in connections.items():
            connections_list.extend(
                (",".join(k.split(",")[:-1]), ",".join(v.split(",")[:-1]))
                for v in v_list
            )
        G = nx.Graph()
        G.add_edges_from(connections_list)
        pos = {k: (v["x"], v["y"]) for k, v in placements.items()}
        labels = {k: ",".join(k.split(",")[:1]) for k in placements.keys()}
        nx.draw(
            G,
            with_labels=with_labels,
            font_weight=font_weight,
            labels=labels,
            pos=pos,
        )
        return G

    def to_yaml(self, **kwargs) -> dict[str, Any]:
        from gdsfactory.get_netlist import get_netlist_yaml

        return get_netlist_yaml(self, **kwargs)

    def write_netlist(self, filepath: str) -> None:
        """Write netlist in YAML."""
        netlist = self.get_netlist()
        netlist = clean_dict(netlist)
        filepath = pathlib.Path(filepath)
        filepath.write_text(yaml.dump(netlist))

    def write_netlist_dot(self, filepath: str | None = None) -> None:
        """Write netlist graph in DOT format."""
        from networkx.drawing.nx_agraph import write_dot

        filepath = filepath or f"{self.name}.dot"

        G = self.plot_netlist()
        write_dot(G, filepath)

    def get_netlist(self, **kwargs) -> dict[str, Any]:
        """From Component returns instances, connections and placements dict.

        Keyword Args:
            component: to extract netlist.
            full_settings: True returns all, false changed settings.
            tolerance: tolerance in nm to consider two ports connected.
            exclude_port_types: optional list of port types to exclude from netlisting.
            get_instance_name: function to get instance name.
            allow_multiple: False to raise an error if more than two ports share the same connection.
                if True, will return key: [value] pairs with [value] a list of all connected instances.

        Returns:
            Netlist dict (instances, connections, placements, ports)
                instances: Dict of instance name and settings.
                connections: Dict of Instance1Name,portName: Instance2Name,portName.
                placements: Dict of instance names and placements (x, y, rotation).
                ports: Dict portName: ComponentName,port.
                name: name of component.
        """
        from gdsfactory.get_netlist import get_netlist

        return get_netlist(component=self, **kwargs)

    def get_netlist_recursive(self, **kwargs) -> dict[str, DictConfig]:
        """Returns recursive netlist for a component and subcomponents.

        Keyword Args:
            component: to extract netlist.
            component_suffix: suffix to append to each component name.
                useful if to save and reload a back-annotated netlist.
            get_netlist_func: function to extract individual netlists.
            full_settings: True returns all, false changed settings.
            tolerance: tolerance in nm to consider two ports connected.
            exclude_port_types: optional list of port types to exclude from netlisting.
            get_instance_name: function to get instance name.
            allow_multiple: False to raise an error if more than two ports share the same connection.
                if True, will return key: [value] pairs with [value] a list of all connected instances.

        Returns:
            Dictionary of netlists, keyed by the name of each component.
        """
        from gdsfactory.get_netlist import get_netlist_recursive

        return get_netlist_recursive(component=self, **kwargs)

    def get_netlist_flat(self, **kwargs) -> dict[str, DictConfig]:
        """Returns a netlist where all subinstances are exposed and independently named.

        Keyword Args:
            component: to extract netlist.
            component_suffix: suffix to append to each component name.
                useful if to save and reload a back-annotated netlist.
            get_netlist_func: function to extract individual netlists.
            full_settings: True returns all, false changed settings.
            tolerance: tolerance in nm to consider two ports connected.
            exclude_port_types: optional list of port types to exclude from netlisting.
            get_instance_name: function to get instance name.
            allow_multiple: False to raise an error if more than two ports share the same connection.
                if True, will return key: [value] pairs with [value] a list of all connected instances.

        Returns:
            Dictionary of netlists, keyed by the name of each component.
        """
        from gdsfactory.get_netlist_flat import get_netlist_flat

        return get_netlist_flat(component=self, **kwargs)

    def assert_ports_on_grid(
        self, grid_factor: int = 1, error_type: str = "error"
    ) -> None:
        """Asserts that all ports are on grid."""
        for port in self.ports.values():
            port.assert_on_grid(grid_factor=grid_factor, error_type=error_type)

    def assert_ports_manhattan(self, error_type: str = "error") -> None:
        """Asserts that all ports are on manhattan angles (0, 90, 180, 270)."""
        for port in self.ports.values():
            port.assert_manhattan(error_type=error_type)

    def get_ports(self, depth: int | None = 0):
        """Returns copies of all the ports of the Component, rotated and \
                translated so that they're in their top-level position.

        The Ports returned are copies of the originals, but each copy has the same
        ``uid`` as the original so that they can be traced back to the original if needed.

        Args:
            depth: If not None, defines from how many reference levels to retrieve Ports from.

        Returns:
            port_list : list of Port List of all Ports in the Component.
        """
        port_list = [p._copy() for p in self.ports.values()]

        if depth is None or depth > 0:
            for r in self.references:
                new_depth = None if depth is None else depth - 1
                ref_ports = r.parent.get_ports(depth=new_depth)

                # Transform ports that came from a reference
                ref_ports_transformed = []
                for rp in ref_ports:
                    new_port = rp._copy()
                    new_center, new_orientation = r._transform_port(
                        rp.center,
                        rp.orientation,
                        r.origin,
                        r.rotation,
                        r.x_reflection,
                    )
                    new_port.center = new_center
                    new_port.new_orientation = new_orientation
                    ref_ports_transformed.append(new_port)
                port_list += ref_ports_transformed

        return port_list

    def get_ports_dict(self, **kwargs) -> dict[str, Port]:
        """Returns a dict of ports.

        Keyword Args:
            layer: port GDS layer.
            prefix: select ports with prefix in port name.
            suffix: select ports with port name suffix.
            orientation: select ports with orientation in degrees.
            width: select ports with port width.
            layers_excluded: List of layers to exclude.
            port_type: select ports with port_type (optical, electrical, vertical_te).
            clockwise: if True, sort ports clockwise, False: counter-clockwise.
        """
        return select_ports(self.ports, **kwargs)

    def get_ports_list(self, **kwargs) -> list[Port]:
        """Returns list of ports.

        Keyword Args:
            layer: select ports with GDS layer.
            prefix: select ports with prefix in port name.
            suffix: select ports with port name suffix.
            orientation: select ports with orientation in degrees.
            orientation: select ports with orientation in degrees.
            width: select ports with port width.
            layers_excluded: List of layers to exclude.
            port_type: select ports with port_type (optical, electrical, vertical_te).
            clockwise: if True, sort ports clockwise, False: counter-clockwise.
        """
        return list(select_ports(self.ports, **kwargs).values())

    def get_ports_pandas(self):
        import pandas as pd

        col_spec = [
            "name",
            "width",
            "center",
            "orientation",
            "layer",
            "port_type",
            "shear_angle",
        ]

        return pd.DataFrame(
            [port.to_dict() for port in self.get_ports_list()], columns=col_spec
        )

    def get_ports_polars(self):
        import polars as pl

        col_spec = {
            "name": pl.Utf8,
            "width": pl.Float64,
            "center": pl.List(pl.Float64),
            "orientation": pl.Float64,
            "layer": pl.List(pl.UInt16),
            "port_type": pl.Utf8,
            "shear_angle": pl.Float64,
        }

        return pl.DataFrame(
            [port.to_dict() for port in self.get_ports_list()], schema=col_spec
        )

    def ref(
        self,
        position: Coordinate = (0, 0),
        port_id: str | None = None,
        rotation: float = 0,
        h_mirror: bool = False,
        v_mirror: bool = False,
    ) -> ComponentReference:
        """Returns Component reference.

        Args:
            position: x, y position.
            port_id: name of the port.
            rotation: in degrees.
            h_mirror: horizontal mirror using y axis (x, 1) (1, 0).
                This is the most common mirror.
            v_mirror: vertical mirror using x axis (1, y) (0, y).
        """
        _ref = ComponentReference(self)

        if port_id and port_id not in self.ports:
            raise ValueError(f"port {port_id} not in {self.ports.keys()}")

        origin = self.ports[port_id].center if port_id else (0, 0)
        if h_mirror:
            _ref.mirror_x(port_id)

        if v_mirror:
            _ref.mirror_y(port_id)

        if rotation != 0:
            _ref.rotate(rotation, origin)
        _ref.move(origin, position)

        return _ref

    def ref_center(self, position=(0, 0)):
        """Returns a reference of the component centered at (x=0, y=0)."""
        si = self.size_info
        yc = si.south + si.height / 2
        xc = si.west + si.width / 2
        center = (xc, yc)
        _ref = ComponentReference(self)
        _ref.move(center, position)
        return _ref

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return (
            f"{self.name}: uid {self.uid}, "
            f"ports {list(self.ports.keys())}, "
            f"references {list(self.named_references.keys())}, "
            f"{len(self.polygons)} polygons"
        )

    def pprint(self) -> None:
        """Prints component info."""
        try:
            from rich import pretty

            pretty.install()
            pretty.pprint(self.to_dict())
        except ImportError:
            print(yaml.dump(self.to_dict()))

    def pprint_ports(self, sort_by_name: bool = True, **kwargs) -> None:
        """Prints ports in a rich table.

        Keyword Args:
            layer: select ports with GDS layer.
            prefix: select ports with prefix in port name.
            suffix: select ports with port name suffix.
            orientation: select ports with orientation in degrees.
            orientation: select ports with orientation in degrees.
            width: select ports with port width.
            layers_excluded: List of layers to exclude.
            port_type: select ports with port_type (optical, electrical, vertical_te).
            clockwise: if True, sort ports clockwise, False: counter-clockwise.
        """

        pprint_ports(self.get_ports_list(sort_by_name=sort_by_name, **kwargs))

    def to_kfactory(self):
        """Converts the component to KLayout Component."""
        from gdsfactory.export.to_kfactory import to_kfactory

        return to_kfactory(self)

    def add_port(
        self,
        name: str | object | None = None,
        center: tuple[float, float] | None = None,
        width: float | None = None,
        orientation: float | None = None,
        port: Port | None = None,
        layer: LayerSpec | None = None,
        port_type: str | None = None,
        cross_section: CrossSectionSpec | None = None,
        shear_angle: float | None = None,
        info: Info | None = None,
    ) -> Port:
        """Add port to component.

        You can copy an existing port like add_port(port = existing_port) or
        create a new port add_port(myname, mycenter, mywidth, myorientation).
        You can also copy an existing port
        with a new name add_port(port = existing_port, name = new_name)

        Args:
            name: port name.
            center: x, y.
            width: in um.
            orientation: in deg.
            port: optional port.
            layer: port layer.
            port_type: optical, electrical, vertical_dc, vertical_te, vertical_tm. Defaults to optical.
            cross_section: port cross_section.
            shear_angle: an optional angle to shear port face in degrees.
            info: contains arbitrary information about the port.
        """
        from gdsfactory.pdk import get_cross_section, get_layer

        layer = get_layer(layer)

        if port:
            if not isinstance(port, Port):
                raise ValueError(f"add_port() needs a Port, got {type(port)}")
            p = port.copy()
            if name is not None:
                p.name = name
            if center is not None:
                p.center = center
            if width is not None:
                p.width = width
            if orientation is not None:
                p.orientation = orientation
            if port_type is not None:
                p.port_type = port_type
            if layer is not None:
                p.layer = layer
            if shear_angle is not None:
                p.shear_angle = shear_angle
            if cross_section is not None:
                p.cross_section = cross_section
            if info:
                for k, v in dict(info).items():
                    p.info[k] = v
            p.parent = self

        elif isinstance(name, Port):
            p = name.copy()
            p.parent = self
            name = p.name
        elif center is None:
            raise ValueError("Port needs center parameter (x, y) um.")

        else:
            p = Port(
                name=name,
                center=center,
                width=width,
                orientation=orientation,
                parent=self,
                layer=layer,
                port_type=port_type or "optical",
                cross_section=get_cross_section(cross_section)
                if cross_section
                else None,
                shear_angle=shear_angle,
            )
            p.parent = self
            if info is not None:
                for k, v in dict(info).items():
                    p.info[k] = v
        if name is not None:
            p.name = name
        if p.name in self.ports:
            raise ValueError(f"add_port() Port name {p.name!r} exists in {self.name!r}")

        self.ports[p.name] = p
        return p

    def add_ports(
        self,
        ports: Iterable[Port] | dict[str, Port],
        prefix: str = "",
        suffix: str = "",
        **kwargs,
    ) -> None:
        """Add a list or dict of ports.

        you can include a prefix to add to the new port names to avoid name conflicts.

        Args:
            ports: list or dict of ports.
            prefix: to prepend to each port name.
            suffix: to append to each port name.
        """
        if hasattr(ports, "values"):
            for port_name, port in ports.items():
                name = f"{prefix}{port_name}{suffix}"
                self.add_port(name=name, port=port, **kwargs)

        else:
            for port in ports:
                name = f"{prefix}{port.name}{suffix}"
                self.add_port(name=name, port=port, **kwargs)

    def snap_ports_to_grid(self, grid_factor: int = 1) -> None:
        for port in self.ports.values():
            port.snap_to_grid(grid_factor=grid_factor)

    def remove_layers(
        self,
        layers: list[LayerSpec],
        include_labels: bool = True,
        invert_selection: bool = False,
        recursive: bool = True,
    ) -> Component:
        """Remove a list of layers and returns the same Component.

        Args:
            layers: list of layers to remove.
            include_labels: remove labels on those layers.
            invert_selection: removes all layers except layers specified.
            recursive: operate on the cells included in this cell.
        """
        from gdsfactory import get_layer

        component = self.flatten() if recursive and self.references else self
        layers = [get_layer(layer) for layer in layers]

        should_remove = not invert_selection
        component._cell.filter(
            spec=layers,
            remove=should_remove,
            polygons=True,
            paths=True,
            labels=include_labels,
        )
        return component

    def extract(
        self,
        layers: list[LayerSpec],
        include_labels: bool = True,
        recursive: bool = True,
    ) -> Component:
        """Extract polygons from a Component and returns a new Component.

        Args:
            layers: list of layers to extract.
            include_labels: extract labels on those layers.
            recursive: operate on the cells included in this cell.
        """
        c = self.copy()

        return c.remove_layers(
            layers,
            invert_selection=True,
            recursive=recursive,
            include_labels=include_labels,
        )

    def add_polygon(
        self,
        points,
        layer: str | int | tuple[int, int] | np.nan = np.nan,
        snap_to_grid: bool = False,
    ) -> Polygon:
        """Adds a Polygon to the Component.

        Args:
            points: Coordinates of the vertices of the Polygon.
            layer: layer spec to add polygon on.
            snap_to_grid: snap points to grid.
        """
        from gdsfactory.pdk import get_layer

        if layer is None:
            return None
        elif isinstance(layer, set):
            polygons = [self.add_polygon(points, ly) for ly in layer]
            return polygons[0]

        layer = get_layer(layer)
        if isinstance(points, gdstk.Polygon):
            # if layer is unspecified or matches original polygon, just add it as-is
            polygon = points
            if layer is np.nan or (
                isinstance(layer, tuple) and (polygon.layer, polygon.datatype) == layer
            ):
                polygon = Polygon(polygon.points, (polygon.layer, polygon.datatype))
            else:
                layer, datatype = _parse_layer(layer)
                polygon = Polygon(polygon.points, (layer, datatype))

            if hasattr(points, "properties"):
                polygon.properties = deepcopy(points.properties)

            if polygon.area() > 0:
                self._add_polygons(polygon)
            return polygon

        elif hasattr(points, "geoms"):
            for geom in points.geoms:
                polygon = self.add_polygon(geom, layer=layer)
            return polygon
        elif hasattr(points, "exterior"):  # points is a shapely Polygon
            return self._add_polygon_shapely(layer, points)

        points = np.asarray(points)
        if points.ndim == 1:
            return [self.add_polygon(poly, layer=layer) for poly in points]
        if layer is np.nan:
            layer = 0

        if points.ndim == 2:
            # add single polygon from points
            if len(points[0]) > 2:
                # Convert to form [[1,2],[3,4],[5,6]]
                points = np.column_stack(points)

            points = snap.snap_to_grid2x(points) if snap_to_grid else points
            layer, datatype = _parse_layer(layer)
            polygon = Polygon(points, (layer, datatype))
            if polygon.area() > 0:
                self._add_polygons(polygon)
            return polygon
        elif points.ndim == 3:
            layer, datatype = _parse_layer(layer)

            polygons = []
            for polygon_points in points:
                polygon = Polygon(polygon_points, (layer, datatype))
                if polygon.area() > 0:
                    polygons.append(polygon)

            self._add_polygons(*polygons)
            return polygons
        else:
            raise ValueError(f"Unable to add {points.ndim}-dimensional points object")

    def _add_polygon_shapely(self, layer, points, snap_to_grid=False):
        layer, datatype = _parse_layer(layer)
        points_exterior = points.exterior.coords
        if snap_to_grid:
            points_exterior = snap_to_grid2x(points_exterior)
        polygon = Polygon(points_exterior, (layer, datatype))

        if points.interiors:
            return self._add_polygon_shapely_with_holes(
                points, layer, datatype, polygon
            )
        self._add_polygons(polygon)
        return polygon

    def _add_polygon_shapely_with_holes(
        self, points, layer, datatype, polygon, snap_to_grid=False
    ):
        from shapely import get_coordinates

        points = get_coordinates(points.interiors)

        if snap_to_grid:
            points = np.round(points, 3)

        polygon_interior = Polygon(points, (layer, datatype))
        polygons = gdstk.boolean(
            polygon,
            polygon_interior,
            operation="not",
            layer=layer,
            datatype=datatype,
        )
        for polygon in polygons:
            if polygon.area() > 0:
                self._add_polygons(polygon)
        return polygon

    def _add_polygons(self, *polygons: list[Polygon]) -> None:
        self.is_unlocked()
        self._cell.add(*polygons)

    def copy(self, name: str | None = None) -> Component:
        c = copy(self)
        if name:
            c.rename(name)
        return c

    def add_ref_container(self, component: Component) -> ComponentReference:
        """Add reference, ports and copy_child_info."""
        ref = self << component
        self.add_ports(ref.ports)
        self.copy_child_info(component)
        return ref

    def copy_child_info(self, component: Component) -> None:
        """Copy and settings info from child component into parent.

        Parent components can access child cells settings.
        """
        if not isinstance(component, Component | ComponentReference):
            raise ValueError(
                f"{type(component)}" "is not a Component or ComponentReference"
            )

        self.child = component
        for k, v in dict(component.info).items():
            if k not in self.info:
                self.info[k] = v

    @property
    def size_info(self) -> SizeInfo:
        """Size info of the component."""
        return SizeInfo(self.bbox)

    def is_unlocked(self) -> None:
        """Raises warning if Component is locked."""
        if self._locked:
            message = (
                f"Component {self.name!r} is dangerous to modify as it's already "
                "on cache and will change all of its references. "
                + mutability_error_message
            )
            if CONF.raise_error_on_mutation:
                raise MutabilityError(message)
            else:
                warnings.warn(message)

    def _add(self, element) -> None:
        """Add a new element or list of elements to this Component.

        Args:
            element: Polygon, ComponentReference or iterable
                The element or iterable of elements to be inserted in this cell.

        Raises:
            MutabilityError: if component is locked.
        """
        self.is_unlocked()
        if isinstance(element, ComponentReference):
            self._cell.add(element._reference)
            self._references.append(element)
        else:
            self._cell.add(element)

    def add(self, element) -> None:
        """Add a new element or list of elements to this Component.

        Args:
            element: Polygon, ComponentReference or iterable
                The element or iterable of elements to be inserted in this cell.

        Raises:
            MutabilityError: if component is locked.
        """
        if isinstance(element, ComponentReference):
            self._register_reference(element)
            self._add(element)
        elif isinstance(element, Iterable):
            for subelement in element:
                self.add(subelement)
        else:
            self._add(element)

    def add_array(
        self,
        component: Component,
        columns: int = 2,
        rows: int = 2,
        spacing: tuple[float, float] = (100, 100),
        alias: str | None = None,
    ) -> ComponentReference:
        """Creates a ComponentReference reference to a Component.

        Args:
            component: The referenced component.
            columns: Number of columns in the array.
            rows: Number of rows in the array.
            spacing: array-like[2] of int or float.
                Distance between adjacent columns and adjacent rows.
            alias: str or None. Alias of the referenced Component.

        Returns
            a: ComponentReference containing references to the Component.
        """
        if not isinstance(component, Component):
            raise TypeError("add_array() needs a Component object.")
        ref = ComponentReference(
            component=component,
            columns=int(round(columns)),
            rows=int(round(rows)),
            spacing=spacing,
        )
        ref.name = None
        self._add(ref)
        self._register_reference(reference=ref, alias=alias)
        return ref

    def distribute(
        self,
        elements: str = "all",
        direction: str = "x",
        spacing: float = 100.0,
        separation: bool = True,
        edge: str = "center",
    ) -> Component:
        """Distributes the specified elements in the Component.

        Args:
            elements: array-like of objects or 'all'. Elements to distribute.
            direction: {'x', 'y'} Direction of distribution; either a line in the x-direction or y-direction.
            spacing  int or float. Distance between elements.
            separation: bool. If True, guarantees elements are separated with a fixed spacing
                between; if  False, elements are spaced evenly along a grid.
            edge: {'x', 'xmin', 'xmax', 'y', 'ymin', 'ymax'}
                Which edge to perform the distribution along (unused if separation == True)

        """
        if elements == "all":
            elements = self.polygons + self.references
        _distribute(
            elements=elements,
            direction=direction,
            spacing=spacing,
            separation=separation,
            edge=edge,
        )
        return self

    def align(self, elements="all", alignment: str = "ymax") -> Component:
        """Align elements in the Component.

        Args:
            elements : array-like of objects, or 'all'
                Elements in the Component to align.
            alignment : {'x', 'y', 'xmin', 'xmax', 'ymin', 'ymax'}
                Which edge to align along (e.g. 'ymax' will move the elements such
                that all of their topmost points are aligned).
        """
        if elements == "all":
            elements = self.polygons + self.references
        _align(elements, alignment=alignment)
        return self

    def flatten(self, single_layer: LayerSpec | None = None) -> Component:
        """Returns a flattened copy of the component.

        Flattens the hierarchy of the Component such that there are no longer
        any references to other Components. All polygons and labels from
        underlying references are copied and placed in the top-level Component.
        If single_layer is specified, all polygons are moved to that layer.

        Args:
            single_layer: move all polygons are moved to the specified (optional).
        """
        component_flat = Component()

        _cell = self._cell.copy(name=component_flat.name)
        _cell = _cell.flatten()
        component_flat._cell = _cell
        if single_layer is not None:
            warnings.warn("flatten on single layer is deprecated")

        component_flat.copy_child_info(self)
        component_flat.add_ports(self.ports)
        return component_flat

    def flatten_reference(self, ref: ComponentReference) -> None:
        """From existing cell replaces reference with a flatten reference \
        which has the transformations already applied.

        Transformed reference keeps the original name.

        Args:
            ref: the reference to flatten into a new cell.

        """
        from gdsfactory.functions import transformed

        self.remove(ref)
        new_component = transformed(ref)
        self.add_ref(new_component, alias=ref.name)

    def flatten_invalid_refs(self, *args, **kwargs) -> Component:
        """Flatten all invalid references."""
        warnings.warn(
            "flatten_invalid_refs is deprecated, use flatten_offgrid_references",
            DeprecationWarning,
        )
        return self.flatten_offgrid_references(*args, **kwargs)

    def flatten_offgrid_references(
        self,
        grid_size: float | None = None,
        updated_components=None,
        traversed_components=None,
        keep_names: bool = False,
    ) -> Component:
        """Returns new component with flattened references so that they snap to grid.

        Args:
            grid_size: snap to grid size.
            updated_components: set of updated components.
            traversed_components: set of traversed components.
            keep_names: True for writing to GDS, False for internal use.
        """
        return flatten_offgrid_references_recursive(
            self,
            grid_size=grid_size,
            updated_components=updated_components,
            traversed_components=traversed_components,
            keep_names=keep_names,
        )

    def add_ref(
        self, component: Component, alias: str | None = None, **kwargs
    ) -> ComponentReference:
        """Add ComponentReference to the current Component.

        Args:
            component: Component.
            alias: named_references.

        Keyword Args:
            columns: Number of columns in the array.
            rows: Number of rows in the array.
            spacing: Distances between adjacent columns and adjacent rows.
            origin: array-like[2] of int or float
                Position where the cell is inserted.
            rotation : int or float
                Angle of rotation of the reference (in `degrees`).
            magnification : int or float
                Magnification factor for the reference.
            x_reflection : bool
                If True, the reference is reflected parallel to the x direction
                before being rotated.
            name : str (optional)
                A name for the reference (if provided).

        """
        if not isinstance(component, Component):
            raise TypeError(f"type = {type(component)} needs to be a Component.")
        ref = ComponentReference(component, **kwargs)
        self._add(ref)
        self._register_reference(reference=ref, alias=alias)
        return ref

    def _register_reference(
        self, reference: ComponentReference, alias: str | None = None
    ) -> None:
        component = reference.parent
        reference.owner = self

        if alias is None:
            if reference.name is not None:
                alias = reference.name
            else:
                prefix = (
                    component.function_name
                    if component.function_name
                    else component.name
                )
                self._reference_names_counter.update({prefix: 1})
                alias = f"{prefix}_{self._reference_names_counter[prefix]}"

                while alias in self._named_references:
                    self._reference_names_counter.update({prefix: 1})
                    alias = f"{prefix}_{self._reference_names_counter[prefix]}"

        reference.name = alias
        self._named_references[alias] = reference

    @property
    def layers(self) -> set[tuple[int, int]]:
        """Returns a set of the Layers in the Component."""
        return self.get_layers()

    def get_layers(self) -> set[tuple[int, int]]:
        """Return a set of (layer, datatype).

        .. code ::

            import gdsfactory as gf
            gf.components.straight().get_layers() == {(1, 0), (111, 0)}
        """
        polygons = self._cell.get_polygons(depth=None)
        return {(polygon.layer, polygon.datatype) for polygon in polygons}

    def get_layer_names(self) -> list[tuple[int, int]]:
        """Return layer names used in the design.

        .. code ::

            import gdsfactory as gf
            gf.components.straight().get_names() == ['WG']
        """
        import gdsfactory as gf

        PDK = gf.get_active_pdk()
        LAYERS = PDK.layers
        name_to_layer = dict(LAYERS)
        layer_to_name = {v: k for k, v in name_to_layer.items()}
        layer_names = []

        for layer in self.layers:
            if layer not in layer_to_name:
                warnings.warn(f"{layer} not in LayerMap.", stacklevel=3)
            else:
                layer_names.append(layer_to_name[layer])
        return layer_names

    def _repr_html_(self):
        """Show geometry in KLayout and in matplotlib for Jupyter Notebooks."""
        self.show()
        fig = self.plot()
        if fig and hasattr(fig, "_repr_html_"):
            return fig._repr_html_()

    def add_pins_triangle(
        self,
        port_marker_layer: Layer = (1, 10),
        layer_label: Layer = (1, 10),
        make_copy: bool = True,
    ) -> Component:
        """Returns component with triangular pins."""
        from gdsfactory.add_pins import add_pins_triangle

        if make_copy:
            component = self.copy()
        else:
            component = self
        add_pins_triangle(
            component=component, layer=port_marker_layer, layer_label=layer_label
        )
        return component

    def plot_klayout(
        self,
        show_ports: bool = True,
        port_marker_layer: Layer = (1, 10),
        show_labels: bool = False,
        show_ruler: bool = True,
    ):
        """Returns klayout image.

        If it fails to import klayout defaults to matplotlib.

        Args:
            show_ports: shows component with port markers and labels.
            port_marker_layer: for the ports.
            show_labels: shows labels.
            show_ruler: shows ruler.
        """

        if show_ports:
            name = self.name
            component = self.add_pins_triangle(port_marker_layer=port_marker_layer)
            component.rename(name, cache=False)

        else:
            component = self

        try:
            from io import BytesIO

            import klayout.db as db  # noqa: F401
            import klayout.lay as lay
            import matplotlib.pyplot as plt

            from gdsfactory.pdk import get_layer_views

            gdspath = component.write_gds(logging=False)
            lyp_path = gdspath.with_suffix(".lyp")

            layer_views = get_layer_views()
            layer_views.to_lyp(filepath=lyp_path)

            layout_view = lay.LayoutView()
            layout_view.load_layout(str(gdspath.absolute()))
            layout_view.max_hier()
            layout_view.load_layer_props(str(lyp_path))

            layout_view.set_config("text-visible", "true" if show_labels else "false")
            layout_view.set_config("grid-show-ruler", "true" if show_ruler else "false")

            pixel_buffer = layout_view.get_pixels_with_options(800, 600)
            png_data = pixel_buffer.to_png_data()

            # Convert PNG data to NumPy array and display with matplotlib
            with BytesIO(png_data) as f:
                img_array = plt.imread(f)

            # Compute the figure dimensions based on the image size and desired DPI
            dpi = 80
            fig_width = img_array.shape[1] / dpi
            fig_height = img_array.shape[0] / dpi

            fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

            # Remove margins and display the image
            ax.imshow(img_array)
            ax.axis("off")  # Hide axes
            ax.set_position([0, 0, 1, 1])  # Set axes to occupy the full figure space

            plt.subplots_adjust(
                left=0, right=1, top=1, bottom=0, wspace=0, hspace=0
            )  # Remove any padding
            plt.tight_layout(pad=0)  # Ensure no space is wasted
            return fig

        except ImportError:
            component.plot(plotter="matplotlib")

    def plot_kweb(self):
        """Shows current gds in kweb."""
        warnings.warn(
            "Component.plot_kweb() is deprecated and will be removed in future versions of gdsfactory. "
            "Use Component.plot() instead"
        )

        try:
            import kweb.server_jupyter as kj
        except Exception:
            print("You need to install kweb with `pip install 'gdsfactory[cad]'`")
            return self.plot_klayout()

        from html import escape

        from IPython.display import IFrame

        from gdsfactory.pdk import get_layer_views

        gdspath = self.write_gds(gdsdir=GDSDIR_TEMP, logging=False)
        lyp_path = GDSDIR_TEMP / "layers.lyp"

        layer_props = get_layer_views()
        layer_props.to_lyp(filepath=lyp_path)
        host = os.getenv("KWEB_HOST", "localhost")

        port = (
            kj.port
            if hasattr(kj, "port") and kj.port
            else int(os.getenv("KWEB_PORT", 8000))
        )
        src = f"http://{host}:{port}/gds/{escape(gdspath.stem+gdspath.suffix)}?layer_props={escape(str(lyp_path))}"

        os.environ["KWEB_PORT"] = str(os.getenv("KWEB_PORT", port))

        if not kj.jupyter_server:
            port = port
            while kj.is_port_in_use(port=port, host=host):
                port += 1

            os.environ["KWEB_PORT"] = str(port)
            logger.debug(src)
            kj.start()

        if kj.jupyter_server:
            return IFrame(
                src=src,
                width=1400,
                height=600,
            )
        else:
            return self.plot_klayout()

    def plot_matplotlib(self, **kwargs) -> None:
        """Plot component using matplotlib.

        Keyword Args:
            show_ports: Sets whether ports are drawn.
            show_subports: Sets whether subports (ports that belong to references) are drawn.
            label_aliases: Sets whether aliases are labeled with a text name.
            new_window: If True, each call to quickplot() will generate a separate window.
            blocking: If True, calling quickplot() will pause execution of ("block") the
                remainder of the python code until the quickplot() window is closed.
                If False, the window will be opened and code will continue to run.
            zoom_factor: Sets the scaling factor when zooming the quickplot window with the
                mousewheel/trackpad.
            interactive_zoom: Enables using mousewheel/trackpad to zoom.
            fontsize: for labels.
            layers_excluded: list of layers to exclude.
            layer_views: layer_views colors loaded from Klayout.
            min_aspect: minimum aspect ratio.
        """
        from gdsfactory.quickplotter import quickplot

        warnings.warn(
            "Component.plot_matplotlib() is deprecated and will be removed in future versions of gdsfactory. "
            "Use Component.plot() instead"
        )

        quickplot(self, **kwargs)

    def plot(self, plotter: str | None = None, **kwargs):
        """Returns component plot using klayout, matplotlib, or kweb.

        We recommend using klayout or kweb.
        Klayout is good for images and kweb for responsive interactive plots.
        Matplotlib is slow for rendering big layouts and is deprecated.

        Args:
            plotter: plot backends ('klayout').
        """
        plotter = plotter or CONF.display_type

        if plotter not in valid_plotters:
            raise ValueError(f"{plotter!r} not in {valid_plotters}")

        if plotter == "klayout":
            self.plot_klayout(**kwargs)
            return
        elif plotter == "kweb":
            return self.plot_kweb()

        elif plotter == "matplotlib":
            from gdsfactory.quickplotter import quickplot

            quickplot(self, **kwargs)
            return

    def show(
        self,
        show_ports: bool = False,
        show_subports: bool = False,
        port_marker_layer: Layer = (1, 10),
        **kwargs,
    ) -> None:
        """Show component in KLayout.

        returns a copy of the Component, so the original component remains intact.
        with pins markers on each port show_ports = True, and optionally also
        the ports from the references (show_subports=True)

        Args:
            show_ports: shows component with port markers and labels.
            show_subports: add ports markers and labels to references.
            port_marker_layer: for the ports.

        Keyword Args:
            gdspath: GDS file path to write to.
            gdsdir: directory for the GDS file. Defaults to /tmp/.
            unit: unit size for objects in library. 1um by default.
            precision: for object dimensions in the library (m). 1nm by default.
            timestamp: Defaults to 2019-10-25. If None uses current time.
        """
        from gdsfactory.add_pins import add_pins_triangle
        from gdsfactory.show import show

        component = (
            self.add_pins_triangle(
                port_marker_layer=port_marker_layer,
                layer_label=port_marker_layer,
                make_copy=True,
            )
            if show_ports
            else self
        )

        if show_subports:
            component = component.copy()
            for reference in component.references:
                if isinstance(component, ComponentReference):
                    add_pins_triangle(
                        component=component,
                        reference=reference,
                        layer=port_marker_layer,
                        layer_label=port_marker_layer,
                    )

        component.rename(self.name, cache=False)
        show(component, **kwargs)

    def _write_library(
        self,
        gdspath: PathType | None = None,
        gdsdir: PathType | None = None,
        timestamp: datetime.datetime | None = _timestamp2019,
        logging: bool = True,
        with_oasis: bool = False,
        with_metadata: bool = False,
        with_metadata_json: bool = False,
        with_netlist: bool = False,
        netlist_function: Callable | None = None,
        **kwargs,
    ) -> Path:
        """Write component to GDS or OASIS and returns gdspath.

        Args:
            gdspath: GDS file path to write to.
            gdsdir: directory for the GDS file. Defaults to /tmp/randomFile/gdsfactory.
            timestamp: Defaults to 2019-10-25 for consistent hash.
                If None uses current time.
            logging: disable GDS path logging, for example for showing it in KLayout.
            with_oasis: If True, file will be written to OASIS. Otherwise, file will be written to GDS.
            with_metadata: writes metadata in YAML format.
            with_metadata_json: writes metadata in JSON format.
            with_netlist: writes netlist in JSON format.
            netlist_function: The netlist function to use. You can compose a partial function with the `get_netlist` function for example with your parameters.

        Keyword Args:
            Keyword arguments will override the active PDK's default GdsWriteSettings and OasisWriteSettings.

            Gds settings:
                unit: unit size for objects in library. 1um by default.
                precision: for dimensions in the library (m). 1nm by default.
                on_duplicate_cell: specify how to resolve duplicate-named cells. Choose one of the following:
                    "warn" (default): overwrite all duplicate cells with one of the duplicates (arbitrarily).
                    "error": throw a ValueError when attempting to write a gds with duplicate cells.
                    "overwrite": overwrite all duplicate cells with one of the duplicates, without warning.
                    None: do not try to resolve (at your own risk!)
                flatten_offgrid_references: flattens component references which have invalid transformations.
                max_points: Maximal number of vertices per polygon. Polygons with more vertices that this are automatically fractured.

            Oasis settings:
                compression_level: Level of compression for cells (between 0 and 9).
                    Setting to 0 will disable cell compression, 1 gives the best speed and 9, the best compression.
                detect_rectangles: Store rectangles in compressed format.
                detect_trapezoids: Store trapezoids in compressed format.
                circle_tolerance: Tolerance for detecting circles. If less or equal to 0, no detection is performed. Circles are stored in compressed format.
                validation ("crc32", "checksum32", None): type of validation to include in the saved file.
                standard_properties: Store standard OASIS properties in the file.

        """
        from gdsfactory.decorators import has_valid_transformations
        from gdsfactory.pdk import get_active_pdk

        if gdspath and gdsdir:
            warnings.warn(
                "gdspath and gdsdir have both been specified. gdspath will take precedence and gdsdir will be ignored.",
                stacklevel=3,
            )

        default_settings = get_active_pdk().gds_write_settings
        default_oasis_settings = get_active_pdk().oasis_settings

        explicit_gds_settings = {
            k: v
            for k, v in kwargs.items()
            if v is not None and k in default_settings.model_dump()
        }
        explicit_oas_settings = {
            k: v
            for k, v in kwargs.items()
            if v is not None and k in default_oasis_settings.model_dump()
        }
        # update the write settings with any settings explicitly passed
        write_settings = default_settings.model_copy(update=explicit_gds_settings)
        oasis_settings = default_oasis_settings.model_copy(update=explicit_oas_settings)

        _check_uncached_components(
            component=self, mode=write_settings.on_uncached_component
        )

        if write_settings.flatten_offgrid_references:
            top_cell = flatten_offgrid_references_recursive(self, keep_names=True)
        else:
            top_cell = self
            if not has_valid_transformations(self):
                warnings.warn(
                    f"Component {self.name} has invalid transformations. "
                    "Try component.flatten_offgrid_references() first."
                )

        gdsdir = gdsdir or GDSDIR_TEMP
        gdsdir = pathlib.Path(gdsdir)
        if with_oasis:
            gdspath = gdspath or gdsdir / f"{top_cell.name}.oas"
        else:
            gdspath = gdspath or gdsdir / f"{top_cell.name}.gds"
        gdspath = pathlib.Path(gdspath)
        gdsdir = gdspath.parent
        gdsdir.mkdir(exist_ok=True, parents=True)

        cells = top_cell.get_dependencies(recursive=True)
        cell_names = [cell.name for cell in list(cells)]
        cell_names_unique = set(cell_names)

        if len(cell_names) != len(set(cell_names)):
            for cell_name in cell_names_unique:
                cell_names.remove(cell_name)

            if write_settings.on_duplicate_cell == "error":
                raise ValueError(
                    f"Duplicated cell names in {top_cell.name!r}: {cell_names!r}"
                )
            elif write_settings.on_duplicate_cell in {"warn", "overwrite"}:
                if write_settings.on_duplicate_cell == "warn":
                    warnings.warn(
                        f"Duplicated cell names in {top_cell.name!r}:  {cell_names}",
                        stacklevel=3,
                    )
                cells_dict = {cell.name: cell._cell for cell in cells}
                cells = cells_dict.values()
            elif write_settings.on_duplicate_cell is not None:
                raise ValueError(
                    f"on_duplicate_cell: {write_settings.on_duplicate_cell!r} not in (None, warn, error, overwrite)"
                )

        all_cells = [top_cell._cell] + sorted(cells, key=lambda cc: cc.name)

        no_name_cells = [
            cell.name for cell in all_cells if cell.name.startswith("Unnamed")
        ]

        if no_name_cells:
            warnings.warn(
                f"Unnamed cells, {len(no_name_cells)} in {top_cell.name!r}",
                stacklevel=3,
            )

        # for cell in all_cells:
        #     print(cell.name, type(cell))

        lib = gdstk.Library(
            name=write_settings.lib_name,
            unit=write_settings.unit,
            precision=write_settings.precision,
        )
        lib.add(top_cell._cell)
        lib.add(*top_cell._cell.dependencies(True))

        if with_oasis:
            lib.write_oas(gdspath, **oasis_settings.dict())
        else:
            lib.write_gds(
                gdspath, timestamp=timestamp, max_points=write_settings.max_points
            )
        if logging:
            logger.info(f"Wrote to {str(gdspath)!r}")
        if with_metadata:
            metadata = gdspath.with_suffix(".yml")
            metadata.write_text(self.to_dict_yaml(with_cells=True, with_ports=True))
            logger.info(f"Write YAML metadata to {str(metadata)!r}")
        if with_metadata_json:
            metadata = gdspath.with_suffix(".json")
            metadata.write_bytes(
                orjson.dumps(self.to_dict(with_cells=True, with_ports=True))
            )
            logger.info(f"Write JSON metadata to {str(metadata)!r}")

        if with_netlist:
            """
            Saves the netlist_function output to a json file.
            """
            import json

            if netlist_function is None:
                from gdsfactory.get_netlist import get_netlist

                netlist_function = get_netlist

            netlist_path = gdspath.with_suffix(".json")
            netlist_dictionary = netlist_function(component=self, **kwargs)
            netlist_path.write_text(json.dumps(netlist_dictionary, indent=2))

        CONF.last_saved_files.append(gdspath)
        return gdspath

    def write_gds(
        self,
        gdspath: PathType | None = None,
        gdsdir: PathType | None = None,
        **kwargs,
    ) -> Path:
        """Write component to GDS and returns gdspath.

        Args:
            gdspath: GDS file path to write to.
            gdsdir: directory for the GDS file. Defaults to /tmp/randomFile/gdsfactory.

        Keyword Args:
            unit: unit size for objects in library. 1um by default.
            precision: for dimensions in the library (m). 1nm by default.
            logging: disable GDS path logging, for example for showing it in KLayout.
            on_duplicate_cell: specify how to resolve duplicate-named cells. Choose one of the following:
                "warn" (default): overwrite all duplicate cells with one of the duplicates (arbitrarily).
                "error": throw a ValueError when attempting to write a gds with duplicate cells.
                "overwrite": overwrite all duplicate cells with one of the duplicates, without warning.
            on_uncached_component: Literal["warn", "error"] = "warn"
            flatten_offgrid_references: flattens component references which have invalid transformations.
            max_points: Maximal number of vertices per polygon.
                Polygons with more vertices that this are automatically fractured.
            with_metadata: writes metadata in YAML format.
            with_netlist: writes a netlist in JSON format.
            netlist_function: function to generate the netlist.
        """

        return self._write_library(
            gdspath=gdspath, gdsdir=gdsdir, with_oasis=False, **kwargs
        )

    def write_oas(
        self,
        gdspath: PathType | None = None,
        gdsdir: PathType | None = None,
        **kwargs,
    ) -> Path:
        """Write component to GDS and returns gdspath.

        Args:
            gdspath: GDS file path to write to.
            gdsdir: directory for the GDS file. Defaults to /tmp/randomFile/gdsfactory.

        Keyword Args:
            unit: unit size for objects in library. 1um by default.
            precision: for dimensions in the library (m). 1nm by default.
            logging: disable GDS path logging, for example for showing it in KLayout.
            on_duplicate_cell: specify how to resolve duplicate-named cells. Choose one of the following:
                "warn" (default): overwrite all duplicate cells with one of the duplicates (arbitrarily).
                "error": throw a ValueError when attempting to write a gds with duplicate cells.
                "overwrite": overwrite all duplicate cells with one of the duplicates, without warning.
                None: do not try to resolve (at your own risk!)
            on_uncached_component: Literal["warn", "error"] = "warn"
            flatten_offgrid_references: flattens component references which have invalid transformations.
            compression_level: Level of compression for cells (between 0 and 9).
                Setting to 0 will disable cell compression, 1 gives the best speed and 9, the best compression.
            detect_rectangles: Store rectangles in compressed format.
            detect_trapezoids: Store trapezoids in compressed format.
            circle_tolerance: Tolerance for detecting circles. If less or equal to 0, no detection is performed.
                Circles are stored in compressed format.
            validation ("crc32", "checksum32", None) – type of validation to include in the saved file.
            standard_properties: Store standard OASIS properties in the file.
        """
        return self._write_library(
            gdspath=gdspath,
            gdsdir=gdsdir,
            with_oasis=True,
            **kwargs,
        )

    def to_dict(
        self,
        ignore_components_prefix: list[str] | None = None,
        ignore_functions_prefix: list[str] | None = None,
        with_cells: bool = False,
        with_ports: bool = False,
    ) -> dict[str, Any]:
        """Returns Dict representation of a component.

        Args:
            ignore_components_prefix: for components to ignore when exporting.
            ignore_functions_prefix: for functions to ignore when exporting.
            with_cells: write cell info recursively.
            with_ports: write ports.
        """
        d = self.get_component_spec().model_dump()
        if with_ports:
            ports = {port.name: port.to_dict() for port in self.get_ports_list()}
            d["ports"] = ports

        if with_cells:
            cells = recurse_structures(
                self,
                ignore_functions_prefix=ignore_functions_prefix,
                ignore_components_prefix=ignore_components_prefix,
            )
            d["cells"] = clean_dict(cells)

        d["name"] = self.name
        d["info"] = self.info.model_dump()
        return d

    def to_dict_yaml(self, **kwargs) -> str:
        """Write Dict representation of a component in YAML format.

        Args:
            ignore_components_prefix: for components to ignore when exporting.
            ignore_functions_prefix: for functions to ignore when exporting.
            with_cells: write cells recursively.
            with_ports: write port information.
        """
        return yaml.dump(clean_dict(self.to_dict(**kwargs)))

    def auto_rename_ports(self, **kwargs) -> None:
        """Rename ports by orientation NSEW (north, south, east, west).

        Keyword Args:
            function: to rename ports.
            select_ports_optical: to select optical ports.
            select_ports_electrical: to select electrical ports.
            prefix_optical: prefix.
            prefix_electrical: prefix.

        .. code::

                  3  4
                 _|__|_
             2 -|      |- 5
                |      |
             1 -|______|- 6
                  |  |
                  8  7
        """
        auto_rename_ports(self, **kwargs)

    def auto_rename_ports_counter_clockwise(self, **kwargs) -> None:
        auto_rename_ports_counter_clockwise(self, **kwargs)

    def auto_rename_ports_layer_orientation(self, **kwargs) -> None:
        auto_rename_ports_layer_orientation(self, **kwargs)

    def auto_rename_ports_orientation(self, **kwargs) -> None:
        """Rename ports by orientation NSEW (north, south, east, west).

        Keyword Args:
            function: to rename ports.
            select_ports_optical: to select ports.
            select_ports_electrical:
            prefix_optical:
            prefix_electrical:

        .. code::

                 N0  N1
                 |___|_
            W1 -|      |- E1
                |      |
            W0 -|______|- E0
                 |   |
                S0   S1
        """
        auto_rename_ports_orientation(self, **kwargs)

    def move(self, *args, **kwargs) -> Component:
        """Make a reference instead"""
        raise ValueError(move_error_message)

    def mirror(self, p1: Float2 = (0, 1), p2: Float2 = (0, 0), **kwargs) -> Component:
        """Returns new Component with a mirrored reference.

        Args:
            p1: first point to define mirror axis.
            p2: second point to define mirror axis.
        """
        from gdsfactory.functions import mirror

        return mirror(component=self, p1=p1, p2=p2, **kwargs)

    def rotate(self, angle: float = 90, **kwargs) -> Component:
        """Returns new component with a rotated reference to the original.

        Args:
            angle: in degrees.
        """
        from gdsfactory.functions import rotate

        return rotate(component=self, angle=angle, **kwargs)

    def add_padding(self, **kwargs) -> Component:
        """Returns same component with padding.

        Keyword Args:
            component: for padding.
            layers: list of layers.
            suffix for name.
            default: default padding (50um).
            top: north padding.
            bottom: south padding.
            right: east padding.
            left: west padding.
        """
        from gdsfactory.add_padding import add_padding

        return add_padding(component=self, **kwargs)

    def absorb(self, reference) -> Component:
        """Absorbs polygons from ComponentReference into Component.

        Destroys the reference in the process but keeping the polygon geometry.

        Args:
            reference: ComponentReference to be absorbed into the Component.
        """
        if reference not in self.references:
            raise ValueError(
                "The reference you asked to absorb does not exist in this Component."
            )
        ref_polygons = reference.get_polygons(
            by_spec=False, include_paths=False, as_array=False
        )
        self._add_polygons(*ref_polygons)

        self.add(reference.get_labels())
        self.add(reference.get_paths())
        self.remove(reference)
        return self

    def remove(self, items):
        """Removes items from a Component, which can include Ports, PolygonSets \
        CellReferences, ComponentReferences and Labels.

        Args:
            items: list of Items to be removed from the Component.
        """
        if not hasattr(items, "__iter__"):
            items = [items]
        for item in items:
            if isinstance(item, Port):
                self.ports = {k: v for k, v in self.ports.items() if v != item}
            elif isinstance(item, gdstk.Reference):
                self._cell.remove(item)
                item.owner = None
            elif isinstance(item, ComponentReference):
                self.references.remove(item)
                self._cell.remove(item._reference)
                item.owner = None
                self._named_references.pop(item.name)
            else:
                self._cell.remove(item)

        self._bb_valid = False
        return self

    def hash_geometry(self, precision: float = 1e-4) -> str:
        """Returns an SHA1 hash of the geometry in the Component.

        For each layer, each polygon is individually hashed and then the polygon hashes
        are sorted, to ensure the hash stays constant regardless of the ordering
        the polygons.  Similarly, the layers are sorted by (layer, datatype).

        Args:
            precision: Rounding precision for the the objects in the Component.
                For instance, a precision of 1e-2 will round a point at
                (0.124, 1.748) to (0.12, 1.75).

        """
        polygons_by_spec = self.get_polygons(by_spec=True, as_array=False)
        layers = np.array(list(polygons_by_spec.keys()))

        final_hash = hashlib.sha1()
        for layer in layers:
            layer_hash = hashlib.sha1(layer.astype(np.int64)).digest()
            polygons = polygons_by_spec[tuple(layer)]
            polygons = [_rnd(p.points, precision) for p in polygons]
            polygon_hashes = np.sort([hashlib.sha1(p).digest() for p in polygons])
            final_hash.update(layer_hash)
            for ph in polygon_hashes:
                final_hash.update(ph)

        return final_hash.hexdigest()

    def get_labels(
        self, apply_repetitions=True, depth: int | None = None, layer=None
    ) -> list[Label]:
        """Return labels.

        Args:
            apply_repetitions:.
            depth: None returns all labels and 0 top level.
            layer: layerspec.
        """
        from gdsfactory.pdk import get_layer

        if layer:
            layer, texttype = get_layer(layer)
        else:
            texttype = None
        return self._cell.get_labels(
            apply_repetitions=apply_repetitions,
            depth=depth,
            layer=layer,
            texttype=texttype,
        )

    def remove_labels(self) -> None:
        """Remove labels."""
        self._cell.remove(*self.labels)

    def remap_layers(self, layermap, **kwargs) -> Component:
        """Returns a copy of the component with remapped layers.

        Args:
            layermap: Dictionary of values in format {layer_from: layer_to}.
        """
        if kwargs:
            warnings.warn("{kwargs.keys} is deprecated.", DeprecationWarning)

        component = self.copy()
        layermap = {_parse_layer(k): _parse_layer(v) for k, v in layermap.items()}

        cells = list(component.get_dependencies(True))
        cells.append(component)
        for cell in cells:
            cell._cell.remap(layermap)
        return component

    def to_3d(
        self,
        layer_views: LayerViews | None = None,
        layer_stack: LayerStack | None = None,
        exclude_layers: tuple[Layer, ...] | None = None,
    ):
        """Return Component 3D trimesh Scene.

        Args:
            component: to extrude in 3D.
            layer_views: layer colors from Klayout Layer Properties file.
                Defaults to active PDK.layer_views.
            layer_stack: contains thickness and zmin for each layer.
                Defaults to active PDK.layer_stack.
            exclude_layers: layers to exclude.

        """
        from gdsfactory.export.to_3d import to_3d

        return to_3d(
            self,
            layer_views=layer_views,
            layer_stack=layer_stack,
            exclude_layers=exclude_layers,
        )

    def to_np(
        self,
        nm_per_pixel: int = 20,
        layers: Layers = ((1, 0),),
        values: tuple[float, ...] | None = None,
        pad_width: int = 1,
    ) -> np.ndarray:
        """Returns a pixelated numpy array from Component polygons.

        Args:
            component: Component.
            nm_per_pixel: you can go from 20 (coarse) to 4 (fine).
            layers: to convert. Order matters (latter overwrite former).
            values: associated to each layer (defaults to 1).
            pad_width: padding pixels around the image.

        """
        from gdsfactory.export.to_np import to_np

        return to_np(
            self,
            nm_per_pixel=nm_per_pixel,
            layers=layers,
            values=values,
            pad_width=pad_width,
        )

    def write_stl(
        self,
        filepath: str,
        layer_stack: LayerStack | None = None,
        exclude_layers: tuple[Layer, ...] | None = None,
        use_layer_name: bool = False,
        hull_invalid_polygons: bool = True,
        scale: float | None = None,
    ) -> None:
        """Write a Component to STL for 3D printing.

        Args:
            filepath: to write STL to.
            layer_stack: contains thickness and zmin for each layer.
            exclude_layers: layers to exclude.
            use_layer_name: If True, uses LayerLevel names in output filenames rather than gds_layer and gds_datatype.
            hull_invalid_polygons: If True, replaces invalid polygons (determined by shapely.Polygon.is_valid) with its convex hull.
            scale: Optional factor by which to scale meshes before writing.

        """
        from gdsfactory.export.to_stl import to_stl

        to_stl(
            self,
            filepath=filepath,
            layer_stack=layer_stack,
            exclude_layers=exclude_layers,
            use_layer_name=use_layer_name,
            hull_invalid_polygons=hull_invalid_polygons,
            scale=scale,
        )

    def write_gerber(self, dirpath, layermap_to_gerber_layer, options) -> None:
        """
        Args:
            dirpath: directory to write gerber files to.
            layermap_to_gerber_layer: dictionary of layermap to gerber layer.
            options: dictionary of options for gerber export.
                header: List[str] | None = None
                mode: Literal["mm", "in"] = "mm"
                resolution: float = 1e-6
                int_size: int = 4
        """
        from gdsfactory.export.to_gerber import to_gerber

        to_gerber(
            self,
            dirpath=dirpath,
            layermap_to_gerber_layer=layermap_to_gerber_layer,
            options=options,
        )

    def to_gmsh(self, *args, **kwargs) -> None:
        """Deprecated. instead of.

        mesh = component.to_gmsh(arguments)

        Use:

        from gplugins.gmsh.get_mesh import get_mesh

        """

        raise ValueError(
            """component.to_gmsh() has been deprecated. Instead of:

        mesh = component.to_gmsh(arguments)

        Use:

        from gplugins.gmsh.get_mesh import get_mesh

        mesh = get_mesh(component, arguments)
        """
        )

    def offset(
        self,
        distance: float = 0.1,
        use_union: bool = True,
        precision: float = 1e-4,
        join: str = "miter",
        tolerance: int = 2,
        layer: LayerSpec = "WG",
    ) -> Component:
        """Returns new Component with polygons eroded or dilated by an offset.

        Args:
        distance: Distance to offset polygons. Positive values expand, negative shrink.
        use_union: If True, use union of all polygons to offset. If False, offset
        precision: Desired precision for rounding vertex coordinates.
        join: {'miter', 'bevel', 'round'} Type of join used to create polygon offset
        tolerance: For miter joints, this number must be at least 2 represents the
          maximal distance in multiples of offset between new vertices and their
          original position before beveling to avoid spikes at acute joints. For
          round joints, it indicates the curvature resolution in number of
          points per full circle.
        layer: Specific layer to put polygon geometry on.

        """
        from gdsfactory.geometry.offset import offset

        return offset(
            self,
            distance=distance,
            use_union=use_union,
            precision=precision,
            join=join,
            tolerance=tolerance,
            layer=layer,
        )

    def add_route_info(
        self,
        cross_section: CrossSection | str,
        length: float,
        length_eff: float | None = None,
        taper: bool = False,
        **kwargs,
    ) -> None:
        """Adds route information to a component.

        Args:
            cross_section: CrossSection or name of the cross_section.
            length: length of the route.
            length_eff: effective length of the route.
            taper: if True adds taper information.
            **kwargs: extra information to add to the component.
        """
        from gdsfactory.pdk import get_active_pdk

        pdk = get_active_pdk()

        length_eff = length_eff or length
        length_eff = float(length_eff)
        xs_name = (
            cross_section
            if isinstance(cross_section, str)
            else pdk.get_cross_section_name(cross_section)
        )

        info = self.info
        if taper:
            info[f"route_info_{xs_name}_taper_length"] = length

        info["route_info_type"] = xs_name
        info["route_info_length"] = length_eff
        info["route_info_weight"] = length_eff
        info[f"route_info_{xs_name}_length"] = length_eff
        for key, value in kwargs.items():
            info[f"route_info_{key}"] = value

    def get_component_spec(self) -> ComponentSpec:
        return ComponentSpec(
            function=self.function_name,
            module=self.module,
            settings=self.settings,
        )

    # Deprecated
    @property
    def metadata_child(self) -> dict:
        """Returns metadata from child if any, Otherwise returns component own.
        metadata can access the children metadata at the bottom of the hierarchy.
        """
        warnings.warn(
            "metadata_child is deprecated and will be removed in future versions of gdsfactory"
        )
        settings = dict(self.settings)

        while settings.get("child"):
            settings = settings.get("child")

        return dict(settings)

    def get_info(self):
        """Gathers the .info dictionaries from every sub-Component and returns them in a list.

        Args:
            depth: int or None
                If not None, defines from how many reference levels to
                retrieve Ports from.

        Returns:
            list of dictionaries
                List of the ".info" property dictionaries from all sub-Components
        """
        warnings.warn(
            "get_info is deprecated and will be removed in future versions of gdsfactory"
        )
        D_list = self.get_dependencies(recursive=True)
        return [D.info.model_copy() for D in D_list]

    def get_netlist_yaml(self, **kwargs) -> dict[str, Any]:
        from gdsfactory.get_netlist import get_netlist_yaml

        warnings.warn(
            "get_netlist_yaml is deprecated and will be removed in future versions of gdsfactory"
            "Use to_yaml instead"
        )

        return get_netlist_yaml(self, **kwargs)

    def get_setting(self, setting: str) -> str | int | float:
        warnings.warn(
            "get_setting is deprecated and will be removed in future versions of gdsfactory"
        )
        return (
            self.info.get(setting)
            or self.settings.get(setting)
            or self.metadata_child.get(setting)
        )

    def unlock(self) -> None:
        """Only do this if you know what you are doing."""
        warnings.warn("we will remove unlock to discourage use")
        self._locked = False

    def lock(self) -> None:
        """Makes sure components can't add new elements or move existing ones.

        Components lock automatically when going into the CACHE to
        ensure one component does not change others
        """
        warnings.warn(
            f"we will remove lock to discourage use. Using it in {self.name!r}"
        )
        self._locked = True

    @property
    def metadata(self) -> dict:
        warnings.warn(
            "metadata is deprecated and will be removed in future versions of gdsfactory. "
            "Use component.settings for accessing component settings or component.info for component info."
        )
        return dict(self.settings)

    def __reduce__(self):
        """Gdstk Cells cannot be directly pickled. This method overrides binary serialization with GDS serialization."""
        return deserialize_gds, serialize_gds(self)


# Component functions
def serialize_gds(component: Component) -> Tuple[PathType]:
    """Saves Component as GDS + YAML metadata in temporary files with unique name."""
    gds_filepath = GDSDIR_TEMP / component.name
    gds_filepath = gds_filepath.with_suffix(".gds")
    component.write_gds(gds_filepath, with_metadata=True)
    return (gds_filepath,)


def _line_distances(points, start, end):
    if np.all(start == end):
        return np.linalg.norm(points - start, axis=1)

    vec = end - start
    cross = np.cross(vec, start - points)
    return np.divide(abs(cross), np.linalg.norm(vec))


def _simplify(points, tolerance=0):
    """Ramer–Douglas–Peucker algorithm for line simplification. Takes an
    array of points of shape (N,2) and removes excess points in the line. The
    remaining points form a identical line to within `tolerance` from the
    original
    """
    # From https://github.com/fhirschmann/rdp/issues/7
    # originally written by Kirill Konevets https://github.com/kkonevets

    M = np.asarray(points)
    start, end = M[0], M[-1]
    dists = _line_distances(M, start, end)

    index = np.argmax(dists)
    dmax = dists[index]

    if dmax > tolerance:
        result1 = _simplify(M[: index + 1], tolerance)
        result2 = _simplify(M[index:], tolerance)

        result = np.vstack((result1[:-1], result2))
    else:
        result = np.array([start, end])

    return result


def deserialize_gds(gds_filepath: PathType) -> Component:
    """Loads Component as GDS + YAML metadata from temporary files, and deletes them."""
    from gdsfactory.read import import_gds

    c = import_gds(gds_filepath, read_metadata=True)
    metadata_filepath = gds_filepath.with_suffix(".yml")
    metadata_filepath.unlink()
    gds_filepath.unlink()
    return c


def copy(
    D: Component,
    references=None,
    ports=None,
    polygons=None,
    paths=None,
    name=None,
    labels=None,
) -> Component:
    """Returns a Component copy.

    Args:
        D: component to copy.
        references: references to copy.
        ports: ports to copy.
        polygons: polygons to copy.
        paths: paths to copy.
        name: name of the new component.
        labels: labels to copy.
    """
    c = Component()
    c.settings = D.settings.model_copy()
    c.info = D.info.model_copy()
    c.child = D.child
    c.function_name = D.function_name
    c.module = D.module

    for ref in references if references is not None else D.references:
        c.add(copy_reference(ref))
    for port in (ports if ports is not None else D.ports).values():
        c.add_port(port=port)
    for poly in polygons if polygons is not None else D.polygons:
        c.add_polygon(poly)
    for path in paths if paths is not None else D.paths:
        c.add(path)
    for label in labels if labels is not None else D.labels:
        c.add_label(
            text=label.text,
            position=label.origin,
            layer=(label.layer, label.texttype),
        )

    if name is not None:
        c.name = name

    return c


def copy_reference(
    ref,
    parent=None,
    columns=None,
    rows=None,
    spacing=None,
    origin=None,
    rotation=None,
    magnification=None,
    x_reflection=None,
    name=None,
    v1=None,
    v2=None,
) -> ComponentReference:
    return ComponentReference(
        component=parent or ref.parent,
        columns=columns or ref.columns,
        rows=rows or ref.rows,
        spacing=spacing or ref.spacing,
        origin=origin or ref.origin,
        rotation=rotation or ref.rotation,
        magnification=magnification or ref.magnification,
        x_reflection=x_reflection or ref.x_reflection,
        name=name or ref.name,
        v1=v1 or ref.v1,
        v2=v2 or ref.v2,
    )


def _filter_polys(polygons, layers_excl):
    return [
        polygon
        for polygon, layer, datatype in zip(
            polygons.polygons, polygons.layers, polygons.datatypes
        )
        if (layer, datatype) not in layers_excl
    ]


def recurse_structures(
    component: Component,
    ignore_components_prefix: list[str] | None = None,
    ignore_functions_prefix: list[str] | None = None,
) -> dict[str, Any]:
    """Recurse component and components references recursively.

    Args:
        component: component to recurse.
        ignore_components_prefix: list of prefix to ignore.
        ignore_functions_prefix: list of prefix to ignore.
    """
    ignore_functions_prefix = ignore_functions_prefix or []
    ignore_components_prefix = ignore_components_prefix or []

    if component.function_name and component.function_name in ignore_functions_prefix:
        return {}

    if hasattr(component, "name") and any(
        component.name.startswith(i) for i in ignore_components_prefix
    ):
        return {}

    output = {component.name: dict(component.settings)}
    for reference in component.references:
        if (
            isinstance(reference, ComponentReference)
            and reference.ref_cell.name not in output
        ):
            output.update(recurse_structures(reference.ref_cell))

    return output


def get_base_components(
    component: gf.Component, allow_empty: bool = True
) -> Iterator[gf.Component]:
    """Generator function that yields base components of a given component.

    Parameters:
        component (gf.Component): The component whose base components are to be found.
        allow_empty (bool): If True, allows yielding of components without polygons.

    Yields:
        gf.Component: The base components of the given component.
    """
    if not component.references and (component.polygons or allow_empty):
        yield component
    for ref in component.references:
        yield from get_base_components(ref.parent, allow_empty)


def flatten_offgrid_references_recursive(
    component: Component,
    grid_size: float | None = None,
    updated_components=None,
    traversed_components=None,
    keep_names: bool = False,
) -> Component:
    """Recursively flattens component references which have invalid transformations
    (i.e. non-90 deg rotations or sub-grid translations)
    returns a copy if any subcells have been modified.

    WARNING: this function will produce same-name copies of cells.
    It is strictly meant to be used on write of the GDS file and
    should not be mixed with other cells,
    or you will likely experience issues with duplicate cells

    Args:
        component: the component to fix (in place).
        grid_size: the GDS grid size, in um, defaults to active PDK.get_grid_size()
            any translations with higher resolution than this are considered invalid.
        updated_components: dict of components transformed.
            Should always be None, except for recursive.
        traversed_components: the set of component names which have been traversed.
            Should always be None, except for recursive invocations.
        keep_names: True for writing to GDS, False for internal use.
    """
    from gdsfactory.decorators import is_invalid_ref

    invalid_refs = []
    refs = component.references
    subcell_modified = False
    updated_components = updated_components or {}
    traversed_components = traversed_components or set()

    for ref in refs:
        # mark any invalid refs for flattening
        # otherwise, check if there are any modified cells beneath (we need not do this if the ref will be flattened anyways)
        if is_invalid_ref(ref, grid_size):
            invalid_refs.append(ref.name)
        else:
            # otherwise, recursively flatten refs if the subcell has not already been traversed
            if ref.parent.name not in traversed_components:
                flatten_offgrid_references_recursive(
                    ref.parent,
                    grid_size=grid_size,
                    updated_components=updated_components,
                    traversed_components=traversed_components,
                )
            # now, if the ref's cell been modified, mark it as such
            if ref.parent.name in updated_components:
                subcell_modified = True
    if invalid_refs or subcell_modified:
        # if the cell or subcells need to have references flattened, create an uncached copy of this cell for export
        new_component = component.copy()
        if keep_names:
            new_component.rename(component.name, cache=False)
        else:
            new_component.rename(component.name + "_offgrid")

        # make sure all modified cells have their references updated
        new_refs = new_component.references.copy()
        for ref in new_refs:
            if ref.name in invalid_refs:
                new_component.flatten_reference(ref)
            elif (
                ref.parent.name in updated_components
                and ref.parent is not updated_components[ref.parent.name]
            ):
                ref.parent = updated_components[ref.parent.name]
        component = new_component
        updated_components[component.name] = new_component
    traversed_components.add(component.name)
    return component


def _check_uncached_components(component, mode):
    valid_modes = ["warn", "error", "ignore"]

    if mode == "ignore":
        return
    elif mode not in valid_modes:
        raise ValueError(
            f"{mode} is not a valid value for on_uncached_component. Try one of these: {valid_modes}."
        )

    for sub_component in component.get_dependencies(recursive=True):
        if not sub_component._locked:
            message = (
                f"Component {sub_component.name!r} was NOT properly locked. "
                "You need to write it into a function that has the @cell decorator."
            )
            if mode == "warn":
                warnings.warn(message, UncachedComponentWarning, stacklevel=3)

            elif mode == "error":
                raise UncachedComponentError(message)


if __name__ == "__main__":
    # from functools import partial
    import gdsfactory as gf

    c = gf.c.mzi()
    c = c.simplify(200e-3)
    c.show()

    # c1 = gf.Component()
    # c2 = gf.Component()
    # print(c1.name)
    # print(c2.name)

    # c = gf.components.straight(length=1)
    # cc = gf.routing.add_fiber_array(c)
    # print(c.hash_geometry())
    # c2 = c.flatten()

    # c = gf.routing.add_fiber_single(c)
    # c = gf.components.mzi(info=dict(hi=3))
    # print(type(c.info))
    # yaml_netlist = c.to_yaml()
    # c2 = gf.read.from_yaml(yaml_netlist)
    # c2.show()

    # c = gf.Component()
    # wg1 = c << gf.components.straight(width=0.5, layer=(1, 0))
    # wg2 = c << gf.components.straight(width=0.5, layer=(2, 0))
    # wg2.connect("o1", wg1.ports["o2"])
    # custom_padding = partial(gf.add_padding, layers=("WG",))
    # c = gf.c.mzi(decorator=custom_padding)

    # c = c.copy()
    # c = c.remap_layers({(1, 0): (3, 0)})

    # c._cell.remap({(1, 0): (3, 0)})
    # lib = gdstk.Library()
    # lib.add(c._cell)
    # lib.remap({(1, 0): (2, 0)})
    # c2 = lib[c.name]
    # c._cell = c2
    # c.show()

    # gf.config.enable_offgrid_ports()

    # c = gf.Component("bend")
    # b = c << gf.components.bend_circular(angle=30)
    # s = c << gf.components.straight(length=5)
    # s.connect("o1", b.ports["o2"])
    # p_shapely = c.get_polygons(as_shapely_merged=True)
    # c2 = gf.Component("bend_fixed")
    # c2.add_polygon(p_shapely, layer=(1, 0))
    # c2.plot()

    # c = gf.c.mzi(flatten=True, decorator=gf.routing.add_fiber_single)
    # # print(c.name)
    # c.show()

    # c = gf.c.mzi()
    # fig = c.plot_klayout()
    # fig.savefig("mzi.png")
    # c.pprint_ports()

    # c = gf.Component("hi" * 200)
    # print(c.name)

    # c = gf.Component("hi" * 200)
    # print(c.name)
    # p = c.add_polygon(
    #     [(-8, 6, 7, 9), (-6, 8, 17, 5)], layer=(1, 0)
    # )  # GDS layers are tuples of ints (but if we use only one number it assumes the other number is 0)
    # c.write_gds("hi.gds")
    # c.show()
    # print(CONF.last_saved_files)
