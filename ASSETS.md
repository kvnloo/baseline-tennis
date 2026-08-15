# Tennis-ball asset pipeline

Baseline uses one reusable textured tennis-ball symbol in navigation, the hero, map legend, statistical reports, and action controls.

## Canonical source

The source material is generated at a true **8192 × 8192** resolution by `scripts/generate_tennis_ball_assets.py`.

It follows the same exact-grid method used for the Temple Guard detail master:

1. Render sixteen native 2048 × 2048 tiles in a strict 4 × 4 grid.
2. Preserve every tile losslessly as PNG.
3. Stitch tiles with exact non-overlapping boundaries.
4. Produce independent albedo, normal, roughness, and emissive-mask masters.
5. Record dimensions and SHA-256 receipts in `assets/tennis-ball-8k-manifest.json`.
6. Derive lossless 1024, 512, and 256 WebP UI sprites from the high-resolution source.

There is no neural upscaling, fake super-resolution, overlap, feathering, or collage reconstruction.

## Repository boundary

The reproducible lossless masters and 64 source tiles occupy approximately 487 MB and remain under ignored `artifacts/tennis-ball-8k/`. The deterministic generator, hash manifest, and optimized web derivatives are tracked. Run:

```bash
python scripts/generate_tennis_ball_assets.py
```

## Runtime motion

`src/TennisBallSymbol.tsx` provides five sizes and three motion modes. The hero ball uses a squash/stretch rebound with a synchronized contact shadow. Small instances use restrained hover lift. Dark surfaces add two low-opacity drop-shadow halos rather than shipping the emissive 8K map to browsers.

`prefers-reduced-motion: reduce` disables the rebound and shadow animation.
