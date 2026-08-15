#!/usr/bin/env python3
"""Author archived procedural PBR masters and approved photoreal web sprites.

The 8192 px PBR maps preserve the earlier exact-grid experiment, but they are
not the visible identity source. Runtime sprites derive from the reviewed local
FLUX.2 Klein plate in ``assets/tennis-ball/source``; no native-8K claim is made
for that plate.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "artifacts" / "tennis-ball-8k"
WEB = ROOT / "public" / "tennis-ball"
PHOTO_SOURCE = ROOT / "assets" / "tennis-ball" / "source" / "photoreal-source-seed-4101.png"
SIZE = 8192
TILE = 2048
SEED = 1987


def field(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Continuous multi-frequency felt field in global pixel coordinates."""
    x = x.astype(np.float32)
    y = y.astype(np.float32)
    return (
        np.sin(x * .118 + np.sin(y * .017) * 2.2) * .34
        + np.sin(y * .151 + np.cos(x * .013) * 1.7) * .26
        + np.sin((x + y) * .287) * .18
        + np.sin((x * .73 - y * .61) + SEED) * .12
        + np.sin((x * 1.91 + y * 1.37) + SEED * .17) * .07
    )


def tile_arrays(row: int, col: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # One-pixel guard band ensures normal derivatives remain continuous at exact tile joins.
    yy, xx = np.mgrid[row*TILE-1:(row+1)*TILE+1, col*TILE-1:(col+1)*TILE+1]
    h = field(xx, yy)
    gy, gx = np.gradient(h)
    h = h[1:-1, 1:-1]
    gx = gx[1:-1, 1:-1]
    gy = gy[1:-1, 1:-1]

    base = np.array([196, 236, 43], dtype=np.float32)
    shade = np.clip(1 + h[..., None] * .075, .82, 1.15)
    albedo = np.clip(base * shade, 0, 255).astype(np.uint8)

    strength = 2.7
    nx, ny = -gx * strength, -gy * strength
    nz = np.ones_like(nx)
    norm = np.sqrt(nx*nx + ny*ny + nz*nz)
    normal = np.stack(((nx/norm*.5+.5)*255, (ny/norm*.5+.5)*255, (nz/norm*.5+.5)*255), axis=-1).astype(np.uint8)
    roughness = np.clip(210 + h * 22, 150, 245).astype(np.uint8)
    emissive = np.clip(120 + h * 20, 80, 170).astype(np.uint8)
    return albedo, normal, roughness, emissive


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate_masters() -> dict[str, dict[str, object]]:
    maps = {"albedo": "RGB", "normal": "RGB", "roughness": "L", "emissive-mask": "L"}
    canvases = {name: Image.new(mode, (SIZE, SIZE)) for name, mode in maps.items()}
    tile_root = MASTER / "tiles"
    tile_root.mkdir(parents=True, exist_ok=True)

    for row in range(4):
        for col in range(4):
            arrays = tile_arrays(row, col)
            for (name, mode), array in zip(maps.items(), arrays):
                image = Image.fromarray(array, mode=mode)
                tile_path = tile_root / f"{name}-r{row+1}c{col+1}-2048.png"
                image.save(tile_path, format="PNG", compress_level=3)
                canvases[name].paste(image, (col*TILE, row*TILE))

    manifest: dict[str, dict[str, object]] = {}
    for name, image in canvases.items():
        path = MASTER / f"tennis-ball-{name}-8192.png"
        image.save(path, format="PNG", compress_level=6)
        manifest[name] = {"path": str(path.relative_to(ROOT)), "width": SIZE, "height": SIZE, "sha256": sha(path)}
    return manifest


def render_sprite(size: int, glow: bool = False) -> Image.Image:
    """Cut the approved photoreal plate from black and preserve its fuzzy edge."""
    source = Image.open(PHOTO_SOURCE).convert("RGB")
    rgb = np.asarray(source, dtype=np.float32)
    height, width = rgb.shape[:2]
    yy, xx = np.mgrid[0:height, 0:width]
    cx, cy = (width - 1) / 2, (height - 1) / 2
    radial = np.sqrt(((xx - cx) / width) ** 2 + ((yy - cy) / height) ** 2)

    # The opaque core keeps naturally shadowed felt solid. Outside it, luminance
    # isolates the back-lit loose fibers from the true black studio background.
    luminance = rgb.max(axis=2)
    fiber_alpha = np.clip((luminance - 2.0) / 24.0, 0, 1)
    outer_fade = np.clip((0.49 - radial) / 0.025, 0, 1)
    alpha = np.where(radial <= 0.425, 1.0, fiber_alpha * outer_fade)
    alpha = Image.fromarray((alpha * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(0.35))

    ball = source.convert("RGBA")
    ball.putalpha(alpha)
    if glow:
        halo = Image.new("RGBA", source.size, (0, 0, 0, 0))
        halo_alpha = alpha.filter(ImageFilter.GaussianBlur(width * .038)).point(lambda p: int(p * .16))
        halo.paste((176, 232, 42, 0), (0, 0, width, height))
        halo.putalpha(halo_alpha)
        ball = Image.alpha_composite(halo, ball)
    return ball.resize((size, size), Image.Resampling.LANCZOS)


def generate_web() -> dict[str, dict[str, object]]:
    WEB.mkdir(parents=True, exist_ok=True)
    outputs = {}
    for size in (1024, 512, 256):
        for mode in ("day", "glow"):
            path = WEB / f"tennis-ball-{mode}-{size}.webp"
            render_sprite(size, glow=mode == "glow").save(path, "WEBP", lossless=True, method=6)
            outputs[f"{mode}-{size}"] = {"path": str(path.relative_to(ROOT)), "width": size, "height": size, "sha256": sha(path), "bytes": path.stat().st_size}
    return outputs


def main() -> None:
    MASTER.mkdir(parents=True, exist_ok=True)
    manifest = {
        "method": "archived deterministic 4x4 PBR experiment; not the visible identity source",
        "sourceSize": [SIZE, SIZE],
        "seed": SEED,
        "masters": generate_masters(),
        "visibleSource": {
            "path": str(PHOTO_SOURCE.relative_to(ROOT)),
            "width": 1024,
            "height": 1024,
            "sha256": sha(PHOTO_SOURCE),
            "type": "locally generated photoreal plate; not a photograph, scan, or native 8K source",
        },
        "webDerivatives": generate_web(),
    }
    path = MASTER / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(path)


if __name__ == "__main__":
    main()
