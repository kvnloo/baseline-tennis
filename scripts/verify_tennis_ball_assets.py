#!/usr/bin/env python3
"""Verify exact-grid tennis-ball masters and tracked runtime derivatives."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "artifacts" / "tennis-ball-8k"
TILE = 2048
MAPS = ("albedo", "normal", "roughness", "emissive-mask")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


results = {"accepted": True, "masterSize": [8192, 8192], "maps": {}, "derivatives": {}}
for name in MAPS:
    master_path = MASTER / f"tennis-ball-{name}-8192.png"
    master = Image.open(master_path)
    exact = master.size == (8192, 8192)
    tiles = []
    for row in range(4):
        for col in range(4):
            tile_path = MASTER / "tiles" / f"{name}-r{row+1}c{col+1}-2048.png"
            tile = Image.open(tile_path)
            crop = master.crop((col*TILE, row*TILE, (col+1)*TILE, (row+1)*TILE))
            same = tile.size == (TILE, TILE) and ImageChops.difference(tile, crop).getbbox() is None
            exact &= same
            tiles.append({"tile": tile_path.name, "exact": same, "sha256": sha(tile_path)})
    results["maps"][name] = {"dimensions": list(master.size), "sha256": sha(master_path), "allTilesExact": exact, "tiles": tiles}
    results["accepted"] &= exact

for path in sorted((ROOT / "public" / "tennis-ball").glob("*.webp")):
    image = Image.open(path)
    results["derivatives"][path.name] = {"dimensions": list(image.size), "sha256": sha(path), "bytes": path.stat().st_size}

out = ROOT / "assets" / "tennis-ball-8k-qa.json"
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps({"accepted": results["accepted"], "qa": str(out), "maps": len(results["maps"]), "derivatives": len(results["derivatives"])}))
raise SystemExit(0 if results["accepted"] else 1)
