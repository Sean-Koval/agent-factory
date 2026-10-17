# Airframe theme changelog

Every change to `airframe.css` or `airframe-docs.css` gets an entry here, newest first, under a
new `## theme-vN` heading. Merging it to `main` tags `theme-vN` and opens a sync pull request in
each tool repo (hangar, flightdeck, ai-dlc, Tower), or prints the one-command sync when the
workflow has no cross-repo token. Keep token names stable; list each token whose value changed.

## theme-v1 · 2026-10-17

First tagged release: the "Night Panel" flavor (black canvas, signal-yellow accent, Archivo
Expanded display, Red Hat Text body, DM Mono labels, 2px radius, quiet status colors).
Changes since the copy the tool repos first vendored:

- `airframe.css`, light theme (both the `prefers-color-scheme` block and `[data-theme="light"]`):
  - `--af-surface` `#F7F7F7` → `#F8F8F7`
  - `--af-raised` `#FFFFFF` → `#F1F1F0` (tonal cards instead of white-on-white)
  - `--af-selected` `#EBEBEB` → `#E8E8E7`
- `airframe-docs.css`:
  - Footer sits on the canvas with a top rule (`.md-footer`, `.md-footer-meta`, `.md-copyright`).
  - `figure.af-figure` spans the full column; its SVG or image scales to width; captions upright.
