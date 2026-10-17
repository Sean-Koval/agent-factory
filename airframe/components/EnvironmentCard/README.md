An environment card describes an image a sandbox boots from: its name, what it is for, the digest, the harnesses it carries and how many sandboxes use it, with one action in the foot.

## You provide
- An icon (`environment`, or `gpu` for GPU pools) and the environment name in mono.
- A tag for its role (`default`, `gpu pool`) or, when the last build failed, a failed status instead of the tag.
- One or two sentences of purpose.
- Image digest (shortened with an ellipsis), harnesses, sandboxes in use.
- A foot: who built it and when, and one small secondary button (Fork, Rebuild).

## Markup
```html
<article class="af-card">
  <div class="af-card__top">
    <span class="af-card__lead"><svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true">…</svg><span class="af-card__name">base-codex</span></span>
    <span class="af-tag">default</span>
  </div>
  <p class="af-card__desc">Codex and Claude Code with the shared skill set, 14 tools and package-registry egress.</p>
  <dl class="af-kv af-kv--tight">
    <dt>Image</dt><dd class="af-mono">sha256:41bd…0c9e</dd>
    <dt>Harnesses</dt><dd>claude-code, codex, pi</dd>
    <dt>In use</dt><dd>22 sandboxes</dd>
  </dl>
  <div class="af-card__foot"><span>Built 2 h ago by CI</span><button type="button" class="af-btn af-btn--secondary af-btn--sm">Fork</button></div>
</article>

<!-- failed build: status replaces the tag; the action becomes Rebuild -->
<span class="af-status af-status--failed"><i class="af-status__mark"></i>Build failed</span>
```

## When to use
- The environments index (three across, `af-grid af-grid--3`), and the environment picker when creating a sandbox.

## Do
- Keep the same three rows in the same order on every card so they scan across a row.
- On a failed build, say what still runs on the old image ("1 sandbox, on the old image").

## Don't
- Don't light a failed environment card; the status mark carries it. Lit is for things waiting on a person.
- Don't show full digests; shorten to the first and last four characters.
- Don't put more than one button in the foot.
