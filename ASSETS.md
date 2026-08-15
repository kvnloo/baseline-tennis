# Tennis-ball asset pipeline

Baseline uses one reusable textured tennis-ball symbol in navigation, the hero, map legend, statistical reports, and action controls.

## Canonical visible source

The shipped symbol is derived from `assets/tennis-ball/source/photoreal-source-seed-4101.png`, a **1024 × 1024 locally generated photoreal plate** made with FLUX.2 Klein. It was selected for visible felt fibers, fuzzy silhouette, recessed off-white seam, spherical lighting, and legibility at icon sizes.

The plate is not represented as a photograph, scan, CC0 library asset, or native 8K capture. Its SHA-256 is:

```text
56c81be91ecd708b63931cf29917cf1bb6627863b7b1d776e961d2588f47bd89
```

`scripts/generate_tennis_ball_assets.py` removes the black studio background while preserving loose edge fibers, then produces lossless 1024, 512, and 256 WebP derivatives. Browsers load those optimized derivatives.

## Archived procedural experiment

`artifacts/tennis-ball-8k/` contains the earlier deterministic 8192 × 8192 tiled PBR experiment. It failed the visual realism gate and is **not** the canonical visible identity source. The repository retains its generator and receipts only as reproducible process evidence; its 487 MB outputs remain ignored.

No native, rights-safe 8K photographic tennis-ball material was found in Poly Haven, ambientCG, Blendkit, or OpenGameArt. Baseline therefore makes no claim that the shipped photoreal plate is a native 8K source.

## Runtime motion

`src/TennisBallSymbol.tsx` provides five sizes and three motion modes. The hero ball uses a squash/stretch rebound with a synchronized contact shadow. Small instances use restrained hover lift. Dark surfaces add low-opacity halos without erasing the felt texture.

`prefers-reduced-motion: reduce` disables the rebound and shadow animation.
