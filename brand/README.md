# Brand surfaces

Where most people first meet a product: the top of its README, the card a link unfurls into, the tab icon and
the docs header. Everything in this folder is generated from Airframe by `scripts/banners.py`; never edit a
file here. Change `airframe/tokens.json`, `airframe/icons/marks.json` or the copy in the script, run
`python3 scripts/banners.py --png`, and commit the result. CI regenerates the SVGs and fails when they differ.

| File, in `brand/<product>/` | Size | Use |
| --- | --- | --- |
| `banner-dark.svg`, `banner-light.svg` | 960x320 | The README banner, both themes (see the snippet below). |
| `banner-dark.png`, `banner-light.png` | 1920x640 | The same at 2x for places that take no SVG: Slack, a deck, a blog. |
| `social.png` | 1280x640 | The GitHub social preview (Settings → General → Social preview), Night. PNG under 1 MB, as GitHub asks. |
| `favicon.svg` | 32x32 | The tab icon: the mark on canvas, following the viewer's color scheme. |
| `mark.svg` | 44x44 | The ProductMarks tile for a docs or app header (`theme.logo` in mkdocs.yml). |

Products: `agent-factory` (the suite home, with the family mark), `airframe`, `hangar`, `flightdeck`, `tower`,
`ai-dlc`, `spaceport`.

## The banner

One composition for the family: the eyebrow names the suite and the product's role (Run, Judge, Govern, Setup;
the word "plane" stays out of it), the product mark sits beside the name in Archivo Expanded, the product's
line follows in Red Hat Text, and a strip along the bottom shows the suite story with the 2 px nav marker under
this product's own: the four planes (Define = the team harness, Run = hangar, Judge = flightdeck, Govern = Tower),
then ai-dlc as Setup and Spaceport as the capability. The product hue appears in the mark and that
marker and nowhere else; the brand yellow is the eyebrow hairline, as on the docs heroes. Night is black,
Day is paper, with the dot field top right, once. Nothing is clickable and nothing is a status.

Text is converted to outlines. GitHub serves README images through its proxy as `<img>`, which loads no web
fonts and no external files, so an SVG with `font-family` falls back to whatever the viewer has installed.
Outlines render the same everywhere (GitHub, Slack unfurls, an image viewer) and keep the files
deterministic, so `git diff` can check them. The fonts come from `airframe/fonts/`.

## In a README

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/brand/banner-dark.svg">
  <img alt="hangar: hand a ticket to a coding agent in an isolated cloud sandbox, and get back a verified draft pull request. Part of the agent factory (Run)." src="docs/assets/brand/banner-light.svg" width="960" height="320">
</picture>
```

Keep the `# name` heading under the banner: GitHub reads it for the page title and screen readers read it
first. The `width` and `height` stop the page jumping while the image loads.

## In a tool repo

Tool repos vendor their product's files with `scripts/sync-brand.sh` (a copy of [`sync-brand.sh`](sync-brand.sh)
with `PRODUCT` set), the way they vendor the theme with `sync-airframe.sh`, and never edit them:

```sh
sh scripts/sync-brand.sh theme-v4      # at a release tag
sh scripts/sync-brand.sh               # main
```

Setting the social preview is a repository setting on GitHub: upload `social.png` by hand (Settings →
General → Social preview). The repository description and the docs-site `site_description` should say the same
thing as the banner's line.
