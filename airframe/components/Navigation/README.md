The app header is 56 px on the canvas with a hairline below: a product switcher (mark, name, chevrons), sentence-case tabs with icons, a mono count (the Needs-you count is the orange `af-nav__badge` while above zero) and a 2 px product-hue marker under the active one, a ⌘K search and an avatar; a breadcrumb row sits under it on detail pages.

## You provide
- The product, as `af-hue--<product>` on the header. It colors the active-tab marker.
- The product mark and name in the switcher button, with `aria-haspopup="menu"` and `aria-expanded`.
- Tabs as links with an icon and a short word; mark the current one with `aria-current="page"`. An optional count goes in `af-nav__count`.
- A search button with the scope in its text and `⌘K`, and an avatar button with an `aria-label`.
- For detail pages: a breadcrumb list (product / section / tail number) and optionally the item's status and keyed data at the right.

## Markup
```html
<header class="af-nav af-hue--hangar">
  <button type="button" class="af-nav__switch" aria-haspopup="menu" aria-expanded="false" aria-label="hangar, switch product">
    <span class="af-mark af-hue--hangar" aria-hidden="true"><svg viewBox="0 0 24 24">…</svg></span>
    <span class="af-nav__name">hangar</span>
    <svg class="af-ic" viewBox="0 0 20 20" aria-hidden="true"><path d="M6.5 8 10 4.5 13.5 8M6.5 12l3.5 3.5 3.5-3.5"/></svg>
  </button>
  <span class="af-nav__sep" aria-hidden="true"></span>
  <nav class="af-nav__tabs" aria-label="hangar">
    <a class="af-nav__tab" href="/fleet" aria-current="page"><svg class="af-ic" …>…</svg>Fleet</a>
    <a class="af-nav__tab" href="/approvals"><svg class="af-ic" …>…</svg>Approvals<span class="af-nav__count">1</span></a>
  </nav>
  <div class="af-nav__right">
    <button type="button" class="af-search"><svg class="af-ic" …>…</svg><span>Search sandboxes</span><kbd class="af-kbd">⌘K</kbd></button>
    <button type="button" class="af-avatar" aria-label="Account: Sean">SK</button>
  </div>
</header>

<div class="af-crumbs">
  <ol class="af-crumbs__list" aria-label="Breadcrumb">
    <li><a href="/">hangar</a></li><li><a href="/fleet">fleet</a></li><li><span aria-current="page">HGR-3MX9</span></li>
  </ol>
  <div class="af-crumbs__end"><span class="af-status af-status--approval"><i class="af-status__mark"></i>Needs approval</span></div>
</div>
```

The switcher opens an `af-menu` listing the products, each with a small mark (`af-mark--sm`), the current one with a check in `brand-text`.

## Do
- Keep tab words to one or two; the header must fit six tabs at 1120 px. Below 860 px tabs scroll and search collapses to its icon and ⌘K.
- Use the product's own icon set for tabs (sandbox, session, job, environment, approval, trace).

## Don't
- Don't color anything else in the header with the product hue: not the tab text, not the icons, not the search.
- Don't underline the active tab in brand yellow; the marker is the product hue.
- Don't put status lamps or counts in color in the header. The master caution banner is where attention goes.
