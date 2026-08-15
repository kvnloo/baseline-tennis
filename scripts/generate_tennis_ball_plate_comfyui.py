#!/usr/bin/env python3
"""Generate bounded photoreal tennis-ball plate hypotheses with local FLUX.2 Klein."""
from __future__ import annotations

import copy
import io
import json
import time
import uuid
from pathlib import Path

import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HOST = "http://127.0.0.1:8188"
WORKFLOW = Path("/mnt/zer0models/comfyui/user/default/workflows/wooloo-flux2-klein-edit-api.json")
SOURCE = ROOT / "public/tennis-ball/tennis-ball-day-1024.webp"
OUT = ROOT / "artifacts/tennis-ball-photoreal-candidates"
SEEDS = (4101, 4102, 4103, 4104)

PROMPT = """Photorealistic macro product photograph of one brand-new regulation tennis ball, centered and filling the square frame, seen straight-on at eye level. Exact round sphere. Dense chartreuse fluorescent yellow woven wool-nylon felt with individually visible short fuzzy fibers, irregular soft nap, realistic tactile microtexture, and a subtly hairy silhouette. Authentic recessed curved white rubber tennis-ball seam wrapping around the sphere in the recognizable two-lobed tennis seam geometry, narrow off-white channel with soft felt fibers touching its edges; not painted brackets. Natural spherical volume, soft studio key light from upper left, gentle occlusion and realistic rough non-plastic material response. Pure solid black background with no floor and no cast shadow. No logo, no text, no brand, no watermark. One object only, centered, complete ball not cropped."""
NEGATIVE = """illustration, icon, vector, CGI, 3D render, smooth plastic, rubber toy, golf ball, cricket ball, flat circle, painted line, parallel bracket seams, glowing neon, overexposed, blurry, cropped, floor, hand, racket, text, logo, watermark, multiple balls, deformed sphere"""


def upload_png(image: Image.Image) -> str:
    data = io.BytesIO()
    image.convert("RGB").save(data, "PNG")
    data.seek(0)
    response = requests.post(
        HOST + "/upload/image",
        files={"image": ("baseline-tennis-reference.png", data, "image/png")},
        data={"type": "input", "overwrite": "true"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["name"]


def run(seed: int, source_name: str) -> Path:
    workflow = copy.deepcopy(json.loads(WORKFLOW.read_text()))
    workflow["1"]["inputs"]["image"] = source_name
    workflow["2"]["inputs"]["megapixels"] = 1.0
    workflow["7"]["inputs"]["text"] = PROMPT
    workflow["8"]["inputs"]["text"] = NEGATIVE
    workflow["12"]["inputs"]["cfg"] = 4.0
    workflow["14"]["inputs"]["steps"] = 28
    workflow["16"]["inputs"]["noise_seed"] = seed
    workflow["19"]["inputs"]["filename_prefix"] = f"baseline-tennis/photoreal-seed-{seed}"

    response = requests.post(HOST + "/prompt", json={"prompt": workflow, "client_id": str(uuid.uuid4())}, timeout=60)
    response.raise_for_status()
    record = response.json()
    if "prompt_id" not in record:
        raise RuntimeError(record)
    prompt_id = record["prompt_id"]

    while True:
        history = requests.get(HOST + f"/history/{prompt_id}", timeout=60).json()
        if prompt_id in history:
            item = history[prompt_id]
            if item.get("status", {}).get("status_str") == "error":
                raise RuntimeError(item)
            images = []
            for node in item.get("outputs", {}).values():
                images.extend(node.get("images", []))
            if images:
                payload = requests.get(HOST + "/view", params=images[-1], timeout=120).content
                path = OUT / f"photoreal-seed-{seed}.png"
                path.write_bytes(payload)
                return path
        time.sleep(1)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_name = upload_png(Image.open(SOURCE))
    for seed in SEEDS:
        path = OUT / f"photoreal-seed-{seed}.png"
        if not path.exists():
            path = run(seed, source_name)
        print(path, flush=True)


if __name__ == "__main__":
    main()
