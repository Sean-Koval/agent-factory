# Deck

Fourteen slides that explain the suite to the team or to leadership, to present or to borrow from.

[Open the slides](deck/slides/){ .md-button .md-button--primary } [Download the PDF](deck/agent-factory.pdf){ .md-button }

<iframe class="af-deck-frame" src="deck/slides/" title="The agent factory deck" loading="lazy"></iframe>

Use the arrow keys, the buttons in the corner, or swipe. Printing from the browser gives one slide per page. On a phone the slides open as one page you scroll, each slide stacked and set at a readable size.

## What the slides cover

1. The problem at sixty sessions, the four planes, and how a ticket becomes a merged PR.
2. What the team sees in hangar, flightdeck and Tower, captured from each product's demo.
3. The harness improving on evidence, governance, Airframe, and where things stand.

## Rebuilding the deck

The source is [`deck/src.html`](https://github.com/Sean-Koval/agent-factory/blob/main/deck/src.html); `python3 scripts/build_deck.py --pdf` rebuilds the page and the PDF with the current Airframe theme.

The screens are in `docs/assets/captures/`, made by `python3 scripts/captures.py` from each product's own demo, never by hand. `captures.json` records which commit each came from.

## Diagrams for your own slides

Each diagram comes as a PNG for dark slides, a PNG for light slides, and the SVG source.

| Diagram | Files |
| --- | --- |
| The agent factory at a glance | [Dark PNG](assets/diagrams/planes-dark.png), [light PNG](assets/diagrams/planes-light.png), [SVG](assets/diagrams/planes.svg) |
| Four planes, one loop | [Dark PNG](assets/diagrams/slide-planes-dark.png), [light PNG](assets/diagrams/slide-planes-light.png), [SVG](assets/diagrams/slide-planes.svg) |
| A ticket's journey | [Dark PNG](assets/diagrams/journey-dark.png), [light PNG](assets/diagrams/journey-light.png), [SVG](assets/diagrams/journey.svg) |
| The harness improvement loop | [Dark PNG](assets/diagrams/slide-loop-dark.png), [light PNG](assets/diagrams/slide-loop-light.png), [SVG](assets/diagrams/slide-loop.svg) |
| System context (C4 level 1) | [Dark PNG](assets/diagrams/c4-context-dark.png), [light PNG](assets/diagrams/c4-context-light.png), [SVG](assets/diagrams/c4-context.svg) |
| Containers (C4 level 2) | [Dark PNG](assets/diagrams/c4-containers-dark.png), [light PNG](assets/diagrams/c4-containers-light.png), [SVG](assets/diagrams/c4-containers.svg) |
