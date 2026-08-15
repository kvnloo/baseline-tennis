# Tennis-ball asset pipeline

Baseline uses one reusable textured tennis-ball symbol in navigation, the hero, map legend, statistical reports, and action controls.

## Canonical day source

The day identity is derived from `assets/tennis-ball/source/photoreal-source-seed-4101.png`, a **1024 × 1024 locally generated photoreal plate** made with FLUX.2 Klein. It was selected for visible felt fibers, fuzzy silhouette, recessed off-white seam, spherical lighting, and legibility at icon sizes.

The plate is not represented as a photograph, scan, CC0 library asset, or native 8K capture. Its SHA-256 is:

```text
56c81be91ecd708b63931cf29917cf1bb6627863b7b1d776e961d2588f47bd89
```

## Dark-mode neon UV source

Glow web derivatives now come from a separate **2048 × 2048** reference-informed ultraviolet fluorescence plate:

```text
assets/tennis-ball/source/neon-uv-4mp-seed-5201.png
```

Seed `5201` was generated with FLUX.2 Klein after reviewing real blacklight / UV-induced fluorescence tennis-ball photography. The felt is intentionally more neon chartreuse than the day plate while retaining fuzzy fibers, a near-circular silhouette, and a recessed non-emissive seam. It is not a scan, photograph, or native 8K capture.

Rejected experimental plate (kept for process evidence):

```text
assets/tennis-ball/source/uv-glow-4mp-seed-5101.png
```

Seed `5101` failed shape QA (upper-right bulge / lower flattening) and is **not** used at runtime.

## Web derivatives

`scripts/generate_tennis_ball_assets.py` removes the black studio background while preserving loose edge fibers, then produces lossless 1024, 512, and 256 WebP derivatives for both day and glow modes. Neon glow sprites receive transparent breathing room so the fluorescent edge and browser halo never touch the square frame. Browsers load those optimized derivatives.

## Archived procedural experiment

`artifacts/tennis-ball-8k/` contains the earlier deterministic 8192 × 8192 tiled PBR experiment. It failed the visual realism gate and is **not** the canonical visible identity source. The repository retains its generator and receipts only as reproducible process evidence; its 487 MB outputs remain ignored.

No native, rights-safe 8K photographic tennis-ball material was found in Poly Haven, ambientCG, Blendkit, or OpenGameArt. Baseline therefore makes no claim that the shipped photoreal plates are native 8K sources.

## Runtime motion and theme

`src/TennisBallSymbol.tsx` provides five sizes and three motion modes. The hero ball uses a squash/stretch rebound with a synchronized contact shadow. Small instances use restrained hover lift. Dark surfaces load the neon UV glow derivatives plus a low-opacity CSS halo without erasing the felt texture.

`src/ThemeToggle.tsx` persists light/dark preference under `baseline-theme`.

`prefers-reduced-motion: reduce` disables the rebound and shadow animation.
