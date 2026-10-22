# Which words a decision uses

One set of words for asking a person, in every product, and how a screen behaves while they decide.

## A question is not an approval, but it is the same role

An agent that stops to ask ("Which database should the migration target?") needs a person as much as a held push does, so a
question takes the approval role: the orange diamond, the lit card, the place at the top of the queue. The word tells them
apart: **Needs approval** for a yes or no on an action, **Needs input** for a question with options or free text. Never a
new shape or a new color for questions; the sixth status is still `off`. See the ApprovalCard and Question components.

## Decision words

One set of words for the act, in every product:

| What | Word |
| --- | --- |
| The status of a held action | **Needs approval** |
| The status of a question | **Needs input** |
| The two buttons | **Approve** and **Deny**, with the object when it helps: "Approve push", "Deny refund" |
| The stopped status | **Denied** (the placard) |
| The past tense in a verdict | Approved by Sean, Denied by Sean |

Sign, Decline, Reject and Blocked are retired as UI words for this act, and so is "Needs your signature". Receipts may
still say they were signed: a signature is how a receipt proves the decision, not what the person does.

## Waiting on others stays grey

A request that needs more approvals than it has, where this person has approved or cannot approve, is **Waiting on others**:
the queued role (a grey ring) with words that say how many, `Waiting on 2 others`, and a quorum strip that says whose approval
is in. It is not orange, because nobody *here* is needed; the card is not lit and has no primary action. The moment it
becomes this person's turn it is an approval again. The same goes for a question addressed to someone else.

## Alert inhibition

Airbus inhibits alerts during takeoff and landing so a crew mid-task is not interrupted by anything that can wait. Airframe
inhibits them during a decision: while a dialog or a drawer is open, or a text field has focus (a deny reason, a steer, an
answer), non-critical notices are held and shown afterwards, in order. A notice about the thing the person is doing, or
about a connection that dropped, is critical and shows at once. MasterCaution is not inhibited; it is the summary the held
notices roll up into. The Toast component and `airframe.js` implement the rule; a product that writes its own notices follows it.

Part of [Status](Status.md), a chapter of the [brand book](brand.md). See also [Data](Data.md) and [Products](Products.md).
