from __future__ import annotations

import gdsfactory as gf


def test_add_settings_label() -> None:
    c = gf.components.mzi(delta_length=20, decorator=gf.functions.add_settings_label)
    assert c


if __name__ == "__main__":
    c = gf.components.mzi(delta_length=20, decorator=gf.functions.add_settings_label)
    c.show(show_ports=True)
