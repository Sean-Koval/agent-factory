# How to show a whole fleet

## Fleet board

FleetView shows every sandbox in a fleet as a stand (tile), grouped by pool, and switches between the board and lanes with two `aria-pressed` buttons.

- Each pool header shows the pool name, keyed counts (`Running 16  Waiting 1  Queued 3`) and capacity (`22 of 24 slots`). The fleet header carries the pool schedule.
- A stand is tonal: a faint `fg` tint on `raised`, no border, `radius-control`, `space-4` from its neighbours. It shows the short code (`7Q2K`), its status mark, four stage pips (plan, edit, test, PR, on the `rail` tokens) and nothing else.
- Running and queued stands stay grey. Needs approval, failed and denied stands keep the same neutral ground and take a 3px status edge on their leading side; their current pip lights in the status color too. Off stands are a 1px `line` outline with no fill; free slots a dashed `line` outline.
- A selected stand takes a 1px `fg` outline offset 2px (focus adds the 2px `focus` ring), and the inspector line under the board shows its keyed data and actions.
- Where there is room for words, the fleet is the runway: AgentRow (rows) and AgentCard (board cards) over the same model, with StageRail for progress and DecisionDeck for what needs a person. FleetConsole composes them. hangar's Fleet keeps List and Board as its two views, with Owners as a filter.
- Progress is a claim: fill a rail, ring or capsule solid only for a pct the agent reported. An estimate (elapsed time against the stage's usual length) is dotted from the stage start with a hollow head (`af-rail--est`), and its label says "about"; with neither, fill to the stage start and stop.

Part of [Data](Data.md), a chapter of the [brand book](brand.md). See also [Status](Status.md) and [Products](Products.md).
