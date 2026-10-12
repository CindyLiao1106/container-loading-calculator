# Container loading calculator

How many flat-pack units — or panels, or crates — fit in a 20ft or 40HQ container, and **what limits the load**:
volume or payload. No dependencies, one file.

```
python3 container_loading.py 40hq 2900 2200 600 900
```

```json
{
  "container": "40ft high cube",
  "units_per_layer": 4,
  "layers": 4,
  "units_by_volume": 16,
  "units_by_payload": 31,
  "units": 16,
  "limited_by": "volume",
  "volume_utilisation_pct": 80.2,
  "payload_utilisation_pct": 50.3
}
```

The same unit in a 20ft, with a heavier unit, is **weight-limited** instead:

```
python3 container_loading.py 20gp 1000 1000 500 5000
# units_by_volume 40 · units_by_payload 5 · units 5 · limited_by "weight"
```

## Options

| flag | what it does |
|---|---|
| `--max-layers N` | caps the number of layers when the packing method limits stacking |
| `--rotate` | tries rotating each unit 90° and uses whichever fits more per layer |

## Why it refuses to calculate

If the packed length, width, height or the unit weight is missing, the tool raises an error listing exactly what is missing
instead of returning a number. A guessed loading plan is how deposits get lost — the packed height and the unit weight are
the two inputs that move the answer most, and both come from the factory packing method.

## Container data used

Typical published internal dimensions and payloads. **Confirm against the carrier's own data and the actual packing list
before booking.**

| container | internal L × W × H (mm) | payload (kg) |
|---|---|---|
| 20ft GP | 5898 × 2352 × 2393 | 28,200 |
| 40ft HQ | 12032 × 2352 × 2698 | 28,600 |

Volume utilisation is calculated on the packed envelope (length × width × height of one unit), not on the net product volume.

## Web version

Same logic, in the browser, no install: **[container loading calculator](https://buildextechnology.com/tools/container-loading-calculator/)** —
the tool we use ourselves when quoting flat-pack buildings and aluminium ceiling systems.

## Tests

```
python3 tests/test_loading.py
```

## License

MIT
