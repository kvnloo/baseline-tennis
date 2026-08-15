#!/usr/bin/env python3
"""Deterministically author native 8K tennis-ball PBR masters and web sprites.

The master follows the Temple Guard exact-grid method: 16 independently
rendered 2048 px tiles, stitched as a lossless, non-overlapping 4 x 4 atlas.
No neural upscaling or resampling is used to create the 8192 px masters.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "artifacts" / "tennis-ball-8k"
WEB = ROOT / "public" / "tennis-ball"
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
    scale = 4
    s = size * scale
    yy, xx = np.mgrid[0:s, 0:s]
    cx = cy = (s-1)/2
    radius = s * .44
    nx = (xx-cx)/radius
    ny = (yy-cy)/radius
    r2 = nx*nx + ny*ny
    mask = r2 <= 1
    nz = np.sqrt(np.clip(1-r2, 0, 1))
    # Directional studio light plus authentic high-frequency felt.
    light = np.clip(nx * -.38 + ny * -.48 + nz * .82, 0, 1)
    fuzz = field(xx * (SIZE/s), yy * (SIZE/s))
    tone = np.clip(.48 + light*.54 + fuzz*.038, .14, 1.08)
    base = np.array([190, 222, 45], dtype=np.float32)
    rgb = np.clip(base[None,None,:] * tone[...,None], 0, 255).astype(np.uint8)
    rgba = np.zeros((s,s,4), dtype=np.uint8)
    rgba[...,:3] = rgb
    rgba[...,3] = np.where(mask, 255, 0).astype(np.uint8)
    ball = Image.fromarray(rgba, "RGBA")

    # Tennis seam: two mirrored smooth arcs, clipped by the ball silhouette.
    seam = Image.new("RGBA", (s,s), (0,0,0,0))
    d = ImageDraw.Draw(seam)
    width = max(4, int(s*.018))
    color = (241, 245, 214, 235)
    bbox = (int(s*.13), int(s*.05), int(s*.87), int(s*.94))
    d.arc(bbox, -67, 67, fill=color, width=width)
    d.arc(bbox, 113, 247, fill=color, width=width)
    seam.putalpha(Image.composite(seam.getchannel("A"), Image.new("L",(s,s),0), ball.getchannel("A")))
    ball = Image.alpha_composite(ball, seam)

    if glow:
        halo = Image.new("RGBA", (s,s), (0,0,0,0))
        halo_alpha = ball.getchannel("A").filter(ImageFilter.GaussianBlur(s*.055)).point(lambda p: int(p*.18))
        halo.paste((176,232,42,0), (0,0,s,s))
        halo.putalpha(halo_alpha)
        ball = Image.alpha_composite(halo, ball)
    return ball.resize((size,size), Image.Resampling.LANCZOS)


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
        "method": "native deterministic 4x4 grid; 16 exact non-overlapping 2048px tiles; lossless PNG stitch",
        "sourceSize": [SIZE, SIZE],
        "seed": SEED,
        "masters": generate_masters(),
        "webDerivatives": generate_web(),
    }
    path = MASTER / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(path)


if __name__ == "__main__":
    main()
