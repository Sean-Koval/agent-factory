# 1.0 readiness

Is the suite ready for 1.0, and what is still in the way? This page maps every exit criterion to its Jira ticket, its status and the evidence. Checked on 18 November 2026. Every `release:1.0` ticket, with who can move it, is on [Every 1.0 ticket](readiness-tickets.md). The decisions behind the criteria are on [1.0 decisions](readiness-decisions.md).

**Headline:** of 74 `release:1.0` tickets, 37 are done. Of the rest, 23 are agent-workable and 14 are human-only. Of 17 exit criteria, 1 is met. None of the 5 release-candidate gates is met yet.

A criterion is met only with evidence a reviewer can open: a run, a receipt, a tag or a drill record. A merged PR is only "Partly" when something must run.

## The release candidate

D1 ([KAN-239](https://seanmkoval.atlassian.net/browse/KAN-239)) set the 1.0-rc for 24 November 2026, with five gates. Full 1.0 adds adoption, realistically in late February 2027.

| Gate | Tickets | Status | Evidence or blocker |
| --- | --- | --- | --- |
| Production runs a tag | KAN-20, KAN-27, KAN-145 | Not met | The newest deploy run is for main @ `603040f`, not a tag. v1.0.0-rc.1 is prepared in hangar#483, not tagged. |
| Capture is on | KAN-22 | Not met | Human-only: it needs cloud credentials. |
| Two engineers on repo 1 | KAN-23, KAN-244, KAN-214 | Not met | Not named yet (D6). Keys and infosec sign-off come first. |
| Tower enforces job release and landing | KAN-32, KAN-33 | Not met | The code is merged and off by default. Tower isn't deployed, so no shadow week has run. |
| Restore drill passed | KAN-143 | Partly | hangar's drills are on main (#472), with first results. Tower's are in tower#135. Neither has run on GKE. |

## Exit criteria

From [KAN-141](https://seanmkoval.atlassian.net/browse/KAN-141). All must hold.

| # | Criterion | Tickets | Status | Evidence or blocker |
| --- | --- | --- | --- | --- |
| H1 | hangar has a tagged release with a changelog and green CI | KAN-28 | Met | Tag v0.2.0, with its changelog section. |
| H2 | Production runs that tag, and the live intake check passes | KAN-20, KAN-27 | Not met | KAN-20 cleared the stale deploy. The next deploy is a main commit. hangar#482 adds KAN-27's check script, which hasn't run live. |
| H3 | The credentials policy is enforced | KAN-74 | Partly | Merged in hangar#388 after v0.2.0. It ships in v1.0.0-rc.1 (hangar#483). |
| H4 | Every run is captured | KAN-22 | Not met | Human-only. |
| H5 | Six engineers active across three repos | KAN-23, KAN-24, KAN-68 | Not met | Human-only. Waits on D6 and KAN-214. |
| T1 | Tower is deployed next to hangar behind TLS | KAN-18, KAN-32 | Partly | Tower#95 and hangar#354 are merged; a person applies the deploy. |
| T2 | Agents act under passports | KAN-198, KAN-33 | Partly | Merged in hangar#447, #450 and #451, off by default. Needs a deploy and a shadow week. |
| T3 | One approval of each kind works end to end | KAN-54 | Not met | tower#133 runs one approval of each kind in CI. The live run needs Tower deployed. |
| T4 | hangar asks Tower; the hook fails closed; suspend, resume and stop work | KAN-57, KAN-77, KAN-78, KAN-79 | Partly | Three of four are done. KAN-78 works on Docker; GKE and E2B refuse governed turns. |
| F1 | A regression suite from real failures | KAN-222, KAN-25, KAN-86, KAN-88 | Partly | D7 moved it to regression-v0. Its 20 tasks are on team-harness main. team-harness#92 fixes three graders. |
| F2 | A flightdeck verdict changes one real decision | KAN-31, KAN-87 | Not met | flightdeck#110 readies the run, and #112 checks the v0 exit. The run waits on KAN-223 (human-only). |
| O1 | Security review done, no high or critical finding open | KAN-142, KAN-83 | Partly | H-1 (KAN-165) is closed. M-2 (tower#109) and M-7 (hangar#446) merged on 9 November; their tickets are still open. No outside reviewer has signed off. |
| O2 | Restore drill and upgrade rehearsal passed for every store | KAN-143 | Partly | See the gate above. |
| O3 | SLOs, alerts, on-call and runbooks for hangar and Tower | KAN-144 | Partly | hangar's side is on main. Tower's is tower#108. Alerts haven't fired, and on-call has no backup. |
| O4 | Tower and flightdeck have versioned releases | KAN-145 | Partly | Versions, changelogs and release workflows are on main. Neither has a tag. |
| R1 | The suite docs say what 1.0 includes | KAN-146 | Partly | [Compatibility](compatibility.md) lists the versions. The 1.0 page, with known limits and accepted risks, isn't written. |
| X1 | KAN-146: a reviewer who didn't do the work checks the evidence | KAN-146 | Not met | Human-only, after the rest. |

## Keeping it current

Re-check each status against Jira and the repos' tags, then change the date at the top.
