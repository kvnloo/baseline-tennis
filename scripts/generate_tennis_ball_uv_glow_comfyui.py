#!/usr/bin/env python3
"""Generate a native 4 MP UV-fluorescent tennis-ball hypothesis with ComfyUI."""
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
SOURCE = ROOT / "assets/tennis-ball/source/photoreal-source-seed-4101.png"
OUT = ROOT / "artifacts/tennis-ball-uv-glow-candidates"
SEED = 5101
MEGAPIXELS = 4.0

PROMPT = """Physically plausible macro product photograph of this exact regulation tennis ball under ultraviolet black-light illumination, centered and completely visible, straight-on, exact sphere. Preserve the authentic two-lobed recessed off-white rubber seam geometry and dense woven wool-nylon felt. The chartreuse fluorescent felt emits a restrained yellow-green fluorescence from within the fibers, with thousands of individually resolved fuzzy fibers and realistic rough tactile microtexture still visible. A subtle soft green halo falls into the pure black surroundings while the ball retains deep spherical shading, local contrast, and detailed felt rather than becoming a flat neon disk. The seam remains dim ivory and non-emissive. No floor, no cast shadow, no logo, no text, no brand, no watermark. One object only, not cropped. Photographic black-light exposure, controlled bloom, physically credible fluorescence."""
NEGATIVE = """illustration, icon, vector, CGI, 3D render, smooth plastic, rubber toy, flat circle, painted seam, bracket seams, laser neon, overexposed, clipped highlights, featureless glow, blurry fibers, cropped, floor, hand, racket, text, logo, watermark, multiple balls, deformed sphere, blue seam, emissive white seam"""


def upload_source() -> str:
    data = io.BytesIO()
    Image.open(SOURCE).convert("RGB").save(data, "PNG")
    data.seek(0)
    response = requests.post(
        HOST + "/upload/image",
        files={"image": ("baseline-tennis-seed-4101.png", data, "image/png")},
        data={"type": "input", "overwrite": "true"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["name"]


def run() -> tuple[Path, str]:
    workflow = copy.deepcopy(json.loads(WORKFLOW.read_text()))
    workflow["1"]["inputs"]["image"] = upload_source()
    workflow["2"]["inputs"]["megapixels"] = MEGAPIXELS
    workflow["7"]["inputs"]["text"] = PROMPT
    workflow["8"]["inputs"]["text"] = NEGATIVE
    workflow["12"]["inputs"]["cfg"] = 4.0
    workflow["14"]["inputs"]["steps"] = 32
    workflow["16"]["inputs"]["noise_seed"] = SEED
    workflow["19"]["inputs"]["filename_prefix"] = f"baseline-tennis/uv-glow-4mp-seed-{SEED}"

    response = requests.post(
        HOST + "/prompt",
        json={"prompt": workflow, "client_id": str(uuid.uuid4())},
        timeout=60,
    )
    response.raise_for_status()
    record = response.json()
    prompt_id = record.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(record)

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
                OUT.mkdir(parents=True, exist_ok=True)
                path = OUT / f"uv-glow-4mp-seed-{SEED}.png"
                path.write_bytes(payload)
                return path, prompt_id
        time.sleep(1)


if __name__ == "__main__":
    output, prompt_id = run()
    with Image.open(output) as image:
        print(json.dumps({"output": str(output), "prompt_id": prompt_id, "seed": SEED, "size": image.size}))
