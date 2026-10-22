# How to show a change

## Diffs

A diff is greyscale, like code. The change is the brightest thing: additions in `fg` with a 2px `fg` bar in the gutter,
deletions in `fg-muted` with a 2px `line-strong` bar, context in `fg-subtle`, the sign column (`+`, `−`) carrying the meaning
without hue, line numbers in mono. The stat is two mono numbers, `+42 −17`, in the same tones. No red, no green, no fills:
a change is work, not a state, and the rule that color appears only when a person is needed holds. The one mark a diff may
carry is the failed triangle in the header of the hunk a failing test points at, with the test in the words (`test 38 of 41
points here`). Line comments route to the agent and say so. See the Diff component.

Part of [Data](Data.md), a chapter of the [brand book](brand.md). See also [Status](Status.md) and [Products](Products.md).
