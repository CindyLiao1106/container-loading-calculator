#!/usr/bin/env python3
"""Container loading calculator - how many units fit, and what limits the load.

No dependencies. Volume and payload are checked separately and the smaller of the
two wins; the tool reports which one binds. Missing inputs raise an error instead of
guessing a number.

Typical published container data is used (verify with the carrier before booking):

    container      internal L x W x H (mm)      payload (kg)
    20ft GP        5898 x 2352 x 2393           28200
    40ft HQ        12032 x 2352 x 2698          28600

Web version (same logic, in the browser): https://buildextechnology.com/tools/container-loading-calculator/
"""
import argparse
import json

CONTAINERS = {
    "20gp": {"label": "20ft general purpose", "L": 5898, "W": 2352, "H": 2393, "payload": 28200},
    "40hq": {"label": "40ft high cube", "L": 12032, "W": 2352, "H": 2698, "payload": 28600},
}


def plan(container, length, width, height, weight, max_layers=None, rotate=False):
    """Return the loading plan, or raise ValueError listing what is missing."""
    if container not in CONTAINERS:
        raise ValueError(f"unknown container {container!r}; choose from {sorted(CONTAINERS)}")
    missing = []
    if length <= 0:
        missing.append("packed length (mm)")
    if width <= 0:
        missing.append("packed width (mm)")
    if height <= 0:
        missing.append("packed height (mm)")
    if weight <= 0:
        missing.append("unit weight (kg)")
    if missing:
        raise ValueError("missing: " + ", ".join(missing) + " (this tool does not estimate)")

    box = CONTAINERS[container]
    # whole millimetres / kilograms - keep the arithmetic integral
    length, width, height, weight = int(length), int(width), int(height), int(weight)
    per_layer_straight = (box["L"] // length) * (box["W"] // width)
    per_layer_rotated = (box["L"] // width) * (box["W"] // length)
    per_layer = max(per_layer_straight, per_layer_rotated) if rotate else per_layer_straight
    used_rotation = bool(rotate and per_layer_rotated > per_layer_straight)

    layers = box["H"] // height
    limited_by_stack = False
    if max_layers and max_layers < layers:
        layers = int(max_layers)
        limited_by_stack = True

    units_volume = per_layer * layers
    units_weight = box["payload"] // weight
    units = min(units_volume, units_weight)
    limited_by = "weight" if units_weight < units_volume else "volume"
    volume_util = units * length * width * height / (box["L"] * box["W"] * box["H"]) * 100
    payload_util = units * weight / box["payload"] * 100

    return {
        "container": box["label"],
        "units_per_layer": per_layer,
        "rotated": used_rotation,
        "layers": layers,
        "capped_by_stacking_limit": limited_by_stack,
        "units_by_volume": units_volume,
        "units_by_payload": units_weight,
        "units": units,
        "limited_by": limited_by,
        "volume_utilisation_pct": round(volume_util, 1),
        "payload_utilisation_pct": round(payload_util, 1),
    }


def main():
    p = argparse.ArgumentParser(description="How many units fit in a container, and what limits the load.")
    p.add_argument("container", choices=sorted(CONTAINERS))
    p.add_argument("length", type=float, help="packed length of one unit, mm")
    p.add_argument("width", type=float, help="packed width of one unit, mm")
    p.add_argument("height", type=float, help="packed height of one unit, mm")
    p.add_argument("weight", type=float, help="weight of one unit, kg")
    p.add_argument("--max-layers", type=int, default=None, help="stacking limit, if the packing method sets one")
    p.add_argument("--rotate", action="store_true", help="allow rotating each unit 90 degrees")
    a = p.parse_args()
    try:
        result = plan(a.container, a.length, a.width, a.height, a.weight, a.max_layers, a.rotate)
    except ValueError as e:
        raise SystemExit(f"cannot calculate: {e}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
