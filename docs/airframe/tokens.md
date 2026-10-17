<span class="af-eyebrow">Airframe</span>

# Tokens

Every value Airframe uses, generated from [`airframe/tokens.json`](https://github.com/Sean-Koval/agent-factory/blob/main/airframe/tokens.json). In CSS each token is `var(--af-<name>)`. The swatches are live: switch the site's theme and they follow. Use a token for what its note says, not for the color it happens to be today.

## Color

Text tokens meet 4.5:1 on `canvas`, `surface` and `raised` in both themes; `line-strong`, `focus` and the status colors meet 3:1. The tests in `tests/test_airframe.py` hold every release to that.

--8<-- "airframe-colors.md"

## Type

--8<-- "airframe-type.md"

## Space, shape and layout

--8<-- "airframe-shape.md"
