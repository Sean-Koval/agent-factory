# Deck

Fourteen slides for the team or leadership. The problem at sixty sessions, the four planes, and how a ticket becomes a merged PR. Then what the team sees in hangar, flightdeck and Tower, captured from each product's demo. Then the harness improving on evidence, governance, Airframe, and where things stand.

[Open the slides](deck/slides/){ .md-button .md-button--primary } [Download the PDF](deck/agent-factory.pdf){ .md-button }

<iframe class="af-deck-frame" src="deck/slides/" title="The agent factory deck" loading="lazy"></iframe>

Use the arrow keys, the buttons in the corner, or swipe. Printing from the browser gives one slide per page. On a phone the slides open as one page you scroll, each slide stacked and set at a readable size.

The source is [`deck/src.html`](https://github.com/Sean-Koval/agent-factory/blob/main/deck/src.html); `python3 scripts/build_deck.py --pdf` rebuilds the page and the PDF with the current Airframe theme. The screens are in `docs/assets/captures/`, made by `python3 scripts/captures.py` from each product's own demo, never by hand. `captures.json` records which commit each came from.

## Diagrams for your own slides

| Diagram | Dark | Light | Source |
| --- | --- | --- | --- |
| The agent factory at a glance | [PNG](assets/diagrams/planes-dark.png) | [PNG](assets/diagrams/planes-light.png) | [SVG](assets/diagrams/planes.svg) |
| System context (C4 level 1) | [PNG](assets/diagrams/c4-context-dark.png) | [PNG](assets/diagrams/c4-context-light.png) | [SVG](assets/diagrams/c4-context.svg) |
| Containers (C4 level 2) | [PNG](assets/diagrams/c4-containers-dark.png) | [PNG](assets/diagrams/c4-containers-light.png) | [SVG](assets/diagrams/c4-containers.svg) |
