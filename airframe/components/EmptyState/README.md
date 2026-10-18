An empty state says what is not here and what to do about it: an icon, a title in the display face, one sentence, one primary action and at most one text link, in three kinds (no data, after an action, error); the clear state of a needs-you queue ("Nothing is waiting on you.") is the hero of the dark cockpit, so it gets the large title and the grey counts.

## You provide
- `data-kind`: `no-data` (nothing exists yet), `after-action` (the person did something and this is the result: a filter, a decision, an all-clear) or `error` (the view could not load).
- An icon from the set at 24 px (not for errors), a title as a short sentence with a full stop, one sentence of text with the real numbers and names, and an action row: one primary or secondary button, optionally one `af-link`.
- For the clear state: `af-empty--clear`, the approval icon, the title "Nothing is waiting on you.", the counts as plain statuses (`31 running`, `4 queued`), and a sentence with the next thing that will happen.
- For an error: the failed status (mark and word, lit) above the title, what failed and when, what still works, and one action (Retry). No illustration, no second action, never "Something went wrong".
- `af-empty--compact` inside a card or a column: one row with a 16 px icon, a 13.5 px title and the sentence, an action at the right.

## Markup
```html
<div class="af-empty af-empty--clear" data-kind="after-action">
  <svg class="af-ic af-ic--24" …>approval</svg>
  <h2 class="af-empty__title">Nothing is waiting on you.</h2>
  <div class="af-empty__counts">
    <span class="af-status af-status--running"><i class="af-status__mark"></i>31 running</span>
    <span class="af-status af-status--queued"><i class="af-status__mark"></i>4 queued</span>
  </div>
  <p class="af-empty__text">Decided today: 12, each with a receipt. The next expiry is in <b>2 h 40 min</b>.</p>
  <div class="af-empty__act"><button type="button" class="af-btn af-btn--secondary">Open the record</button></div>
</div>

<div class="af-empty" data-kind="no-data">
  <svg class="af-ic af-ic--24" …>sandbox</svg>
  <h3 class="af-empty__title">No sandboxes running.</h3>
  <p class="af-empty__text">Start one from an environment. The first boot of <span class="af-mono">base-codex</span> takes about 40 s.</p>
  <div class="af-empty__act"><button type="button" class="af-btn af-btn--primary">Start a sandbox</button><a class="af-link" href="#">Environments</a></div>
</div>

<div class="af-empty" data-kind="error">
  <span class="af-status af-status--failed af-status--lit"><i class="af-status__mark"></i>Failed</span>
  <h3 class="af-empty__title">The fleet did not load.</h3>
  <p class="af-empty__text">hangar's API answered <span class="af-mono">502</span> at 14:07:40. The sandboxes keep running; only this view is stale.</p>
  <div class="af-empty__act"><button type="button" class="af-btn af-btn--secondary">Retry</button></div>
</div>

<div class="af-empty af-empty--compact" data-kind="no-data">
  <svg class="af-ic" …>eval</svg>
  <div class="af-empty__body"><span class="af-empty__title">No checks have run yet.</span><span class="af-empty__text">They start when the agent opens the PR.</span></div>
</div>
```

| Kind | Icon | Title | Actions |
|---|---|---|---|
| `no-data` | yes | what is not here | one primary, one link at most |
| `after-action` | yes | the result | one secondary (undo the filter, open the record) |
| `error` | none; the failed status instead | what did not load | one action, never a second |

## When to use
- Any list, table, column, panel or page that has nothing to show; the needs-you queue when it is clear; a view that failed to load.
- Not for loading. Loading is a sentence in `fg-subtle` or the skeleton of the real layout, never this component.

## Do
- Make the clear state the best screen in the product: large title, grey counts, a sentence about what happens next.
- Write what failed and what still works, with the time and the code; say what the button does.
- Use the real numbers: "41 sessions are hidden by the filter", not "no results".

## Don't
- Don't apologize, don't draw an illustration for an error, and don't add a second action to one.
- Don't color an empty state. The one color allowed is the failed mark on an error.
- Don't center a compact empty state; it reads as a row.
