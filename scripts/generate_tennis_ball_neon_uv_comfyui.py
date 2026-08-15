#!/usr/bin/env python3
"""Generate a reference-informed native 4 MP neon UV tennis-ball candidate with ComfyUI."""
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
OUT = ROOT / "artifacts/tennis-ball-neon-uv-candidates"
SEED = 5201
MEGAPIXELS = 4.0

PROMPT = """Reference-informed ultraviolet-induced fluorescence product photograph of this exact regulation tennis ball. One centered ball, completely visible with generous pure-black margin. Absolutely perfect circular spherical silhouette: equal width and height, no bulges, no flat spots, no egg shape, no perspective distortion; straight-on long-lens product camera. Preserve the authentic curved recessed off-white seam and dense woven wool-nylon felt. Under a real 365 nm black light the optic-yellow felt fluoresces an intense saturated electric chartreuse / neon yellow-green, brighter and more vivid than daylight, while individual fuzzy fibers and rough tactile microtexture remain sharply resolved. Balanced bilateral UV illumination and faint neutral fill reveal convincing spherical volume without deforming the contour. Controlled photographic bloom forms a vivid narrow green aura around the fibers, falling quickly into black. The seam stays dim warm ivory, recessed, and non-emissive. No floor or cast shadow. One object only, no crop, no text, no logo, no watermark. Real UV fluorescence photography, not CGI or a plastic neon orb."""
NEGATIVE = """oval, egg shape, bulged contour, flattened edge, dented sphere, asymmetric silhouette, perspective distortion, illustration, icon, vector, CGI, 3D render, smooth plastic, rubber toy, flat circle, painted seam, bracket seams, laser neon, clipped highlights, featureless glow, blurry fibers, cropped, floor, hand, racket, text, logo, watermark, multiple balls, blue seam, emissive white seam"""


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
    workflow["19"]["inputs"]["filename_prefix"] = f"baseline-tennis/neon-uv-4mp-seed-{SEED}"

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
                path = OUT / f"neon-uv-4mp-seed-{SEED}.png"
                path.write_bytes(payload)
                return path, prompt_id
        time.sleep(1)


if __name__ == "__main__":
    output, prompt_id = run()
    with Image.open(output) as image:
        print(json.dumps({"output": str(output), "prompt_id": prompt_id, "seed": SEED, "size": image.size}))
