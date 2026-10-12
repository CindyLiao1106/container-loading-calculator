"""Tests for the loading calculator. Run: python3 -m pytest -q  (or python3 tests/test_loading.py)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from container_loading import plan  # noqa: E402


def test_volume_limited():
    r = plan("40hq", 2900, 2200, 600, 900)
    assert r["units_per_layer"] == 4
    assert r["layers"] == 4
    assert r["units"] == 16
    assert r["limited_by"] == "volume"
    assert r["volume_utilisation_pct"] == 80.2
    assert r["payload_utilisation_pct"] == 50.3


def test_weight_limited():
    r = plan("20gp", 1000, 1000, 500, 5000)
    assert r["units_by_payload"] == 5
    assert r["units"] == 5
    assert r["limited_by"] == "weight"


def test_stacking_limit_caps_layers():
    r = plan("40hq", 2900, 2200, 600, 900, max_layers=2)
    assert r["layers"] == 2
    assert r["capped_by_stacking_limit"] is True
    assert r["units"] == 8


def test_missing_inputs_are_refused():
    for kwargs in ({"height": 0}, {"weight": 0}, {"length": 0}, {"width": 0}):
        args = dict(length=1000, width=1000, height=500, weight=100)
        args.update(kwargs)
        try:
            plan("20gp", **args)
        except ValueError as e:
            assert "missing" in str(e)
        else:
            raise AssertionError("should have refused to calculate")


def test_rotation_helps_when_it_fits_better():
    straight = plan("40hq", 2400, 1150, 600, 900)
    rotated = plan("40hq", 2400, 1150, 600, 900, rotate=True)
    assert rotated["units_per_layer"] >= straight["units_per_layer"]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
