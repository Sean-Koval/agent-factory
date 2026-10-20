Controls are soft-cornered (8 px) and recessed: switches, segmented controls, text inputs and select fields sit on `surface` with a `line-strong` hairline, and every one shows the 2 px `focus` ring.

## You provide
- A visible label for every field (`af-field__label`, sentence-case sans), linked with `for` / `aria-labelledby`.
- Real elements: `<button role="switch" aria-checked>`, `<button aria-pressed>` inside a `role="group"`, `<input>`, and a `<button aria-haspopup="listbox">` for a select.
- Optionally a hint under a field (`af-field__hint`), a leading icon, or a key hint (`<kbd class="af-kbd">⌘E</kbd>`) inside an input.

## Markup
```html
<!-- switch row -->
<div class="af-setting">
  <span class="af-setting__text" id="s1">Auto-approve read-only tools<small>file reads, grep, list</small></span>
  <button type="button" class="af-switch" role="switch" aria-checked="true" aria-labelledby="s1"></button>
</div>

<!-- segmented control -->
<div class="af-field">
  <span class="af-field__label" id="mp">Model policy</span>
  <div class="af-seg" role="group" aria-labelledby="mp">
    <button type="button" class="af-seg__btn" aria-pressed="false">Economy</button>
    <button type="button" class="af-seg__btn" aria-pressed="true">Balanced</button>
    <button type="button" class="af-seg__btn" aria-pressed="false">Frontier</button>
  </div>
</div>

<!-- text input with a key hint -->
<div class="af-field">
  <label class="af-field__label" for="env">Environment</label>
  <div class="af-input"><input id="env" value="base-codex"><kbd class="af-kbd">⌘E</kbd></div>
  <span class="af-field__hint">22 of 24 slots in use</span>
</div>

<!-- select field and its menu -->
<button type="button" class="af-select" aria-haspopup="listbox" aria-expanded="false">
  <span class="af-select__value">claude-code<small>@2.1</small></span>
  <svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true"><path d="M6 8l4 4 4-4"/></svg>
</button>
<ul class="af-menu" role="listbox">
  <li class="af-menu__item" role="option" aria-selected="true"><span class="af-mono">claude-code</span><small>@2.1</small><svg class="af-ic af-ic--14" …>check</svg></li>
  <li class="af-menu__item" role="option" aria-selected="false"><span class="af-mono">codex</span><small>gpt-5.1</small></li>
</ul>
```

## States
| State | How it looks | How it's set |
|---|---|---|
| Hover | border steps up to `fg-subtle`; segment gets `selected` | `:hover` |
| Focus | 2 px `focus` ring, 2 px offset | `:focus-visible` / `:focus-within` |
| On / pressed | switch fills `brand` with an `on-brand` knob; segment inverts to `fg` | `aria-checked="true"`, `aria-pressed="true"` |
| Disabled | 45% opacity, no pointer | `disabled` on the element |
| Invalid | border `status-failed`, message in the hint | `af-input is-invalid` |

`is-hover` and `is-focus` exist only to show those states in specimens; don't use them in product UI.

## Do
- Put values in mono (branches, environments, harnesses); put the setting's name in Red Hat Text.
- Keep segmented controls to two to four short options.
- Use the menu (`af-menu`) for select options and the product switcher; it is the only surface with a shadow (`shadow-overlay`).

## Don't
- Don't color a switch for state other than brand-on; never green.
- Don't remove the focus ring or replace it with a glow.
- Don't use placeholder text as the label.
