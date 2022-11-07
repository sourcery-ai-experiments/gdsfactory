from pathlib import Path
from typing import Optional, Union

from omegaconf import OmegaConf

from gdsfactory.cell import cell as _cell
from gdsfactory.component import Component
from gdsfactory.component_layout import _rename_cell, layout
from gdsfactory.config import CONFIG, logger


@_cell
def import_gds(
    gdspath: Union[str, Path],
    cellname: Optional[str] = None,
    gdsdir: Optional[Union[str, Path]] = None,
    read_metadata: bool = True,
    hashed_name: bool = True,
    **kwargs,
) -> Component:
    """Returns a Componenent from a GDS file.

    if any cell names are found on the component CACHE we append a $ with a
    number to the name

    Args:
        gdspath: path of GDS file.
        cellname: cell of the name to import (None) imports top cell.
        gdsdir: optional GDS directory.
        read_metadata: loads metadata if it exists.
        kwargs: extra to add to component.info (polarization, wavelength ...).

    """
    gdspath = Path(gdsdir) / Path(gdspath) if gdsdir else Path(gdspath)

    if not gdspath.exists():
        raise FileNotFoundError(f"No file {gdspath!r} found")

    metadata_filepath = gdspath.with_suffix(".yml")
    gdspath = str(gdspath)

    # First we set all the cell names in this layout to "" (from zeropdk)
    # so that imported cells don't have name collisions
    cell_dict = {cell.name: cell for cell in layout.each_cell()}
    used_names = set(cell_dict.keys())

    for c in cell_dict.values():
        _rename_cell(c, "")

    # Then we load the new cells from the file and get their names
    layout.read(gdspath)

    imported_cell_dict = {
        cell.name: cell for cell in layout.each_cell() if cell.name != ""
    }

    # Find the top level cell from the
    top_level_cells = {
        cell.name: cell for cell in layout.top_cells() if cell.name != ""
    }

    # Correct any overlapping names by appending an integer to the end of the name
    for name, cell in imported_cell_dict.items():
        new_name = name
        n = 1
        while new_name in used_names:
            new_name = name + ("%0.1i" % n)
            n += 1
        _rename_cell(cell, new_name)
        used_names.add(new_name)

    # Rename all the old cells back to their original names
    for name, cell in cell_dict.items():
        _rename_cell(cell, name)

    # Verify that the topcell name specified exists or that there's only
    # one topcell.  If not, delete the imported cells and raise a ValueError
    if cellname is not None:
        if cellname not in imported_cell_dict:
            [
                layout.delete_cell(cell.cell_index())
                for cell in imported_cell_dict.values()
            ]
            raise ValueError(
                f"import_gds() The requested cell {cellname!r} not in {gdspath!r}"
            )
        top_cell = imported_cell_dict[cellname]
    elif cellname is None and len(top_level_cells) == 1:
        top_cell = list(top_level_cells.values())[0]
    elif cellname is None and len(top_level_cells) > 1:
        [layout.delete_cell(cell.cell_index()) for cell in imported_cell_dict.values()]
        raise ValueError(
            "import_gds() There are multiple top-level cells,"
            " you must specify `cellname` to select of one of them"
        )

    # Create a new Device, but delete the klayout cell that is created
    # and replace it with the imported cell
    component = Component("import_gds")
    layout.delete_cell(component._cell.cell_index())
    component._cell = top_cell

    if read_metadata and metadata_filepath.exists():
        logger.info(f"Read YAML metadata from {metadata_filepath}")
        metadata = OmegaConf.load(metadata_filepath)

        if "settings" in metadata:
            component.settings = OmegaConf.to_container(metadata.settings)

        if "ports" in metadata:
            for port_name, port in metadata.ports.items():
                if port_name not in component.ports:
                    component.add_port(
                        name=port_name,
                        center=port.center,
                        width=port.width,
                        orientation=port.orientation,
                        layer=tuple(port.layer),
                        port_type=port.port_type,
                    )

    component.info.update(**kwargs)
    component.imported_gds = True
    return component


if __name__ == "__main__":

    gdspath = CONFIG["gdsdir"] / "mzi2x2.gds"
    # c = import_gds(gdspath, flatten=True, name="TOP")
    # c.settings = {}
    # print(clean_value_name(c))
    c = import_gds(gdspath, flatten=False, polarization="te")
    # c = import_gds("/home/jmatres/gdsfactory/gdsfactory/gdsdiff/gds_diff_git.py")
    c.show()
