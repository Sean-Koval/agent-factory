# Fonts for generated assets

The three Airframe families as small static files, used only by `scripts/banners.py` to convert banner text to
outlines. Sites and consoles keep loading the families from Google Fonts (see `airframe-components.css`).

| File | Family and instance | Source |
| --- | --- | --- |
| `Archivo-ExpandedBold.ttf` | Archivo, `wdth` 125 and `wght` 700 (Archivo Expanded Bold, the display face) | `ofl/archivo/Archivo[wdth,wght].ttf` v2.001 |
| `RedHatText-Regular.ttf` | Red Hat Text, `wght` 400 (the body face) | `ofl/redhattext/RedHatText[wght].ttf` v1.030 |
| `DMMono-Medium.ttf` | DM Mono Medium (labels) | `ofl/dmmono/DMMono-Medium.ttf` v1.000 |

All three come from [google/fonts](https://github.com/google/fonts) at commit `47d54ca1ebb14fd864695f1d39dc734f39017c33`,
instanced (variable fonts) and subset to Latin (`U+0020-007E` and a few punctuation marks) with fontTools.
`python3 scripts/banners.py fonts` re-derives them. Each family is licensed under the SIL Open Font License 1.1
with no reserved font name; the license texts are `OFL-*.txt` beside the files.
