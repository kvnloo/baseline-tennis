# Baseline — Open Tennis Atlas

A clean, interactive tennis intelligence experiment inspired by ACE Facility's dark operational interface.

## What works

- Interactive SVG world map of 31 ATP/WTA tournament venues
- Tour, surface, and venue filtering
- Live match, player, ace, surface, and season charts
- Plain-language statistical reports with visible methodology
- Responsive desktop/mobile layout
- Open data provenance and reproducible data build

## Data

The current prototype includes 2,547 matches from the 2024 ATP/WTA season, sourced from the open archival mirror of Jeff Sackmann's Tennis Abstract datasets. See [DATA_SOURCES.md](./DATA_SOURCES.md) for provenance and licensing.

## Stack

React 19 · TypeScript · Vite · D3 Geo · TopoJSON · Recharts · Motion · Phosphor Icons · Vitest

## Run

```bash
npm install
npm run data
npm test
npm run dev
```

## Verify

```bash
npm run lint
npm run build
```

## Scope

The query box currently uses a deterministic local statistical engine, so every answer is calculated from the visible dataset rather than generated text. A future service can add broader SQL/LLM planning while retaining the same traceable report contract.
