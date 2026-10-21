A diff is a unified, greyscale view of one file's change: a header with the path and the `+N −M` stat in mono, hunk headers, additions in `fg` with a 2px gutter bar, deletions in `fg-muted`, line numbers, a per-line Comment affordance whose thread goes to the agent, and a failed triangle on the one hunk a failing test points at.

## You provide
- The file path with its directory in `small` (`src/auth/` `refresh.py`), the stat as two mono numbers (`+42`, `−17`, a real minus sign), and keyed facts (`Against main`, `Commit a41f2c0`); optional tools on the right (Copy patch, Open).
- Hunks: a header line (`@@ -118,7 +118,9 @@ def refresh(…)`) and lines. Each line is a grid: old number, new number, sign column, code, and a Comment button.
- Line kinds: `af-diff__line--ctx` (context, `fg-subtle`), `af-diff__line--add` (`fg`, a 2px `fg` bar in the sign column, sign `+`), `af-diff__line--del` (`fg-muted`, a 2px `line-strong` bar, sign `−`).
- An inline comment thread (`af-diff__thread`) under the line it is on: `af-comment` rows (avatar, name, time, text), a Composer to reply, and the note "Sent to the agent with your next message".
- The failing-hunk variant: `af-diff__hunk--failed`, whose header carries `af-status--failed` with the words `test 38 of 41 points here`. That triangle is the only color in a diff.
- A `af-diff__more` line for collapsed context (`12 unchanged lines`).

## Markup
```html
<div class="af-diff" aria-label="Diff of src/auth/refresh.py">
  <header class="af-diff__file">
    <svg class="af-ic" …>diff</svg>
    <span class="af-diff__path"><small>src/auth/</small>refresh.py</span>
    <span class="af-diff__stat"><b class="af-diff__add">+42</b><b class="af-diff__del">−17</b></span>
    <span class="af-meta">…AGAINST main · COMMIT a41f2c0…</span>
    <span class="af-diff__tools"><button type="button" class="af-btn af-btn--ghost af-btn--sm">Copy patch</button></span>
  </header>
  <section class="af-diff__hunk">
    <div class="af-diff__hh"><code>@@ -118,7 +118,9 @@ def refresh(token: Token) -&gt; Token:</code></div>
    <div class="af-diff__line af-diff__line--ctx"><span class="af-diff__n">118</span><span class="af-diff__n">118</span><span class="af-diff__s"> </span><code class="af-diff__code">    now = time.time()</code><button type="button" class="af-btn af-btn--ghost af-diff__cmt">Comment</button></div>
    <div class="af-diff__line af-diff__line--del"><span class="af-diff__n">119</span><span class="af-diff__n"></span><span class="af-diff__s">−</span><code class="af-diff__code">    if token.expires_at &lt; now:</code><button …>Comment</button></div>
    <div class="af-diff__line af-diff__line--add"><span class="af-diff__n"></span><span class="af-diff__n">119</span><span class="af-diff__s">+</span><code class="af-diff__code">    if token.expires_at - EARLY_REFRESH_S &lt; now:</code><button … aria-pressed="true">Comment</button></div>
    <div class="af-diff__thread" role="group" aria-label="Comment thread on line 119">
      <div class="af-comment">
        <span class="af-avatar af-avatar--person af-avatar--22">SK</span>
        <span class="af-comment__who"><span class="af-comment__name">Sean</span><span class="af-comment__time">14:09</span></span>
        <p class="af-comment__text">Cache the check; this path runs per request.</p>
      </div>
      <div class="af-composer"><div class="af-composer__box">
        <textarea class="af-composer__input" rows="1" placeholder="Reply" aria-label="Reply"></textarea>
        <div class="af-composer__row"><span class="af-diff__note"><svg class="af-ic" …>agent</svg><span>Sent to the agent with your next message</span></span><button type="button" class="af-btn af-btn--primary af-btn--sm af-composer__send">Add</button></div>
      </div></div>
    </div>
  </section>
  <section class="af-diff__hunk af-diff__hunk--failed">
    <div class="af-diff__hh"><code>@@ -140,6 +142,10 @@ def _issue(…)</code><span class="af-status af-status--failed"><i class="af-status__mark"></i>test 38 of 41 points here</span></div>
    …
    <div class="af-diff__more">12 unchanged lines</div>
  </section>
</div>
```

Line numbers sit in two `--af-diff-n` columns (3.6em; widen it on the `af-diff` for long files). The Comment button is invisible until the line is hovered or focused, and stays visible (`aria-pressed="true"`) on a line with an open thread.

## Why greyscale
Every diff viewer on the market is red and green. Airframe's rule is that color appears only when a person is needed, and a change is not that: it is the work. So the change is the brightest thing on the screen (additions in `fg`), what was removed recedes (`fg-muted`), and context is quieter still. The sign column and the two bars carry the meaning without hue, so the diff reads the same in greyscale, for color-blind readers and in forced colors, where both bars become `CanvasText` (the deletion's dashed) and the signs do the rest. Only a hunk that a failing test points at gets a mark, the failed triangle, because that is where someone should look.

## When to use
- A job's or session's changes in hangar (per commit, per file), the held push in a Tower approval, flightdeck's prompt diffs.
- The stat alone (`af-diff__stat`) in run lists and approval meta; the file header alone in a file list.

## Do
- Show the real diff, not a summary; show the stat next to the file, not only at the top.
- Route line comments to the agent and say so in the thread ("Sent to the agent with your next message"); keep the person's words, not a paraphrase.
- Point the failed triangle at the hunk a test names, with the test's name or number in the words.
- Keep code in DM Mono at 12 px with tabular figures, `white-space: pre`, no wrapping; scroll sideways.

## Don't
- Don't fill additions green or deletions red, in the lines, the bars or the stat.
- Don't strike through deletions; the sign and tone are enough and the code stays readable.
- Don't color a hunk because it is large or because a reviewer commented; only a failing test lights it.
- Don't put a product hue or the brand yellow in a diff. Yellow appears only as the focus ring and the Add button.
