# Which status a group shows

## Grouping: a group leads with what needs a person

A pool, environment, job, experiment or page header shows the status of the child that most needs attention, and
lists its children, columns and keyed counts in the same order:

1. **approval**: a person is needed now
2. **failed**: something broke and someone should look
3. **denied**: policy stopped it; already decided, kept on record
4. **running**
5. **queued**
6. **off**

A held request leads a denied one because the held one is work and the denied one is a record. (MasterCaution is the
exception: its two lamps follow the cockpit convention, warning before caution.)

- A pool with 16 running sandboxes and one waiting on approval shows **Needs approval**.
- A group that is all queued shows **Queued**; a group with any running child shows **Running**. A group is off only when every child is off.
- Pair the group mark with keyed counts so nothing is hidden: `Waiting 1  Running 16  Queued 3`. Write zero counts as `0`; drop a count only when the role cannot occur in that scope.
- A lit group mark is a pointer, not a summary. Clicking it takes the person to the child that lit it.

Part of [Status](Status.md), a chapter of the [brand book](brand.md). See also [Data](Data.md) and [Products](Products.md).
