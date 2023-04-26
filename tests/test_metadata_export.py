from __future__ import annotations

import toolz

import gdsfactory as gf


def test_metadata_export_partial() -> None:
    straight_wide = gf.partial(gf.pcells.straight, width=2)
    c = straight_wide()
    d = c.to_dict()
    assert d["settings"]["full"]["width"] == 2


def test_metadata_export_compose() -> None:
    straight_wide = toolz.compose(gf.pcells.extend_ports, gf.pcells.straight)
    c = straight_wide()
    d = c.to_dict()
    # assert d["settings"]["full"]["component"]["settings"]["function_name"] == "straight"
    assert d["settings"]["full"]["length"] == 5


if __name__ == "__main__":
    # test_metadata_export_partial()
    test_metadata_export_compose()

    # straight_wide = toolz.compose(gf.pcells.extend_ports, gf.pcells.straight)
    # c = straight_wide()
    # d = c.to_dict()
