# IDs and numbers

How a person reads an ID, a number or a unit: tail numbers, units, ratios and money.

## Tail-number IDs

- Give every object a person can point at a tail number: product prefix, optional type, short code; uppercase, hyphenated. `HGR-7Q2K` sandbox, `FDK-EXP-0142` experiment, `TWR-APR-0391` approval, `TWR-RCPT-88A1` receipt.
- Set IDs in `af-id` (DM Mono 500). Never lowercase, wrap or truncate an ID; truncate the description beside it. The fleet board may show the code alone (`7Q2K`) because the pool header carries the prefix.
- Lead with the ID: "HGR-0PZ4 failed at test", not "Test failed for sandbox HGR-0PZ4".
- Derive the code from the real ID: a hash written in Crockford base32 (`0-9`, `A-Z` without `I L O U`), four characters. When two objects on the same page share a code, lengthen both until they differ. Keep the real ID on hover (`title`), on copy, and in URLs and the API.
- Kind segments: the product's main object has none (`HGR-7Q2K` is a sandbox). Others use a short word: `JOB`, `SES` session, `APR` approval, `SNAP` snapshot, `REQ` request, `RUN`, `BLD` build, `TOK` token, `EXP` experiment, `RCPT` receipt. Things people name (environments, credentials, named sessions) keep their names.
- Where a machine reads the text (commands, commit trailers, logs), keep the real ID. Where a person reads it (Slack, PR comments), lead with the tail number and give the real ID beside it.

## Numbers and units

- Use tabular figures wherever numbers stack (`data` style, `af-num`, `af-mono`). Right-align numeric columns.
- Put a space between number and unit: `14.0 s`, `41 min`, `2 vCPU`, `48.6k tokens`. No space before `%` or after a currency sign: `61%`, `$1.18`.
- Elapsed clocks as `00:41:07`. Span durations in seconds with one decimal. Relative time axes run `-60 min` to `now`.
- Money: two decimals in tables (`$0.42`), whole units in headlines (`$142`). Group thousands: `2,481`.
- Ratios in words: `22 of 24 slots`, `38 of 41`. Never `38/41`.
- Show zero as a number (`0`, `$0.00`). Use an em dash only for "not applicable".

Part of the [brand book](brand.md). See also [Status](Status.md), [Data](Data.md) and [Products](Products.md).
