"""Build the suite's architecture diagrams as theme-aware SVG.

Every color is an Airframe token (`var(--af-*, <dark fallback>)`), so a diagram inlined in a docs
page follows the page's theme, and the same file opened on its own renders in the dark flavor.
`scripts/render.py` turns them into PNGs for slides and READMEs.

    python3 scripts/diagrams.py            # writes docs/assets/diagrams/*.svg
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "diagrams"
# The dark fallbacks come from the Airframe build, so a stand-alone SVG matches the current Night theme.
NIGHT = json.loads((ROOT / "theme" / "airframe-tokens.json").read_text())["themes"]["dark"]
# The docs show a 1200-wide drawing in a 1188px column at best and a 938px one beside a sidebar, so the
# smallest source size is 12px: nothing drops below about 9.4px on screen. `check_floor` enforces it.
FLOOR = 12


def with_fallbacks(svg_text: str) -> str:
    """Rewrite every var(--af-<token>, <fallback>) so the fallback is that token's Night value."""
    return re.sub(r"var\(--af-([a-z0-9-]+), [^)]+\)", lambda m: f"var(--af-{m.group(1)}, {NIGHT[m.group(1)]})", svg_text)

# Every box carries the same 2px product rule along its top; the centre of a drawing (box-hub) is marked
# by size, position and a 1px line-strong edge, never by the brand yellow or a product hue around it: a
# colored outline reads as a status (see airframe/guide/Status.md).
STYLE = """
<style>
  .af-d .bg { fill: var(--af-canvas, #000); }
  .af-d .box { fill: var(--af-raised, #141414); }
  .af-d .box-hub { fill: var(--af-raised, #141414); stroke: var(--af-line-strong, #6B6B6B); stroke-width: 1; }
  .af-d .box-plan { fill: none; stroke: var(--af-line-strong, #6B6B6B); stroke-width: 1; stroke-dasharray: 4 4; }
  .af-d .box-ext { fill: var(--af-surface, #0A0A0A); stroke: var(--af-line-strong, #6B6B6B); stroke-width: 1; }
  .af-d .person { fill: var(--af-surface, #0A0A0A); stroke: var(--af-fg-subtle, #8A8A8A); stroke-width: 1; }
  .af-d .bound { fill: none; stroke: var(--af-rule, #3A3A3A); stroke-width: 1; stroke-dasharray: 2 5; }
  .af-d .bound-fill { fill: var(--af-surface, #0A0A0A); }
  .af-d .name { font: 700 16px "Archivo", "Helvetica Neue", Arial, sans-serif; font-stretch: 125%; fill: var(--af-fg, #fff); }
  .af-d .name-s { font: 700 14px "Archivo", "Helvetica Neue", Arial, sans-serif; font-stretch: 125%; fill: var(--af-fg, #fff); }
  .af-d .title { font: 700 20px "Archivo", "Helvetica Neue", Arial, sans-serif; font-stretch: 125%; fill: var(--af-fg, #fff); }
  .af-d .body { font: 400 13px "Red Hat Text", "Helvetica Neue", Arial, sans-serif; fill: var(--af-fg-muted, #A6A6A6); }
  .af-d .lbl { font: 500 12px "DM Mono", ui-monospace, Menlo, monospace; letter-spacing: .08em; fill: var(--af-fg-subtle, #8A8A8A); }
  .af-d .lbl-hi { font: 500 12px "DM Mono", ui-monospace, Menlo, monospace; letter-spacing: .08em; fill: var(--af-brand-text, #FFC400); }
  .af-d .edge { fill: none; stroke: var(--af-fg-subtle, #8A8A8A); stroke-width: 1.25; }
  .af-d .edge-plan { fill: none; stroke: var(--af-fg-subtle, #8A8A8A); stroke-width: 1.25; stroke-dasharray: 5 4; }
  .af-d .elabel { font: 400 12.5px "Red Hat Text", "Helvetica Neue", Arial, sans-serif; fill: var(--af-fg-subtle, #8A8A8A); }
  .af-d .arrowhead { fill: var(--af-fg-subtle, #8A8A8A); }
  .af-d .dot { fill: var(--af-dot-field, #262626); }
</style>
"""

PRODUCT = {
    "hangar": "var(--af-product-hangar, #EE8F63)",
    "flightdeck": "var(--af-product-flightdeck, #D98CD2)",
    "tower": "var(--af-product-tower, #C5A93B)",
    "aidlc": "var(--af-product-aidlc, #69C27E)",
    "spaceport": "var(--af-product-spaceport, #B199F4)",
    # The team harness repo is not a product: it has no hue of its own.
    "harness": "var(--af-fg-subtle, #8A8A8A)",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w: int, h: int, label: str, body: list[str], dots: tuple[int, int, int, int] | None = None,
        pid: str | None = None) -> str:
    pid = pid or label.lower().replace(" ", "-")[:24]
    field = ""
    if dots:
        x, y, fw, fh = dots
        field = (f'<pattern id="{pid}-dots" width="8" height="8" patternUnits="userSpaceOnUse">'
                 f'<circle class="dot" cx="4" cy="4" r="1.1"/></pattern>'
                 f'<rect x="{x}" y="{y}" width="{fw}" height="{fh}" fill="url(#{pid}-dots)"/>')
    return (f'<svg class="af-d" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{esc(label)}">{STYLE}'
            f'<defs><marker id="{pid}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path class="arrowhead" d="M0 0L10 5L0 10z"/></marker></defs>'
            f'<rect class="bg" width="{w}" height="{h}"/>{field}'
            + "".join(body).replace("ARROW", f"url(#{pid}-arrow)") + "</svg>\n")


def box(x, y, w, h, name, lines=(), eyebrow=None, kind="box", product=None, name_cls="name"):
    out = [f'<rect class="{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>']
    if product:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="2" fill="{PRODUCT[product]}"/>')
    ty = y + 26
    if eyebrow:
        cls = "lbl"
        out.append(f'<text class="{cls}" x="{x + 18}" y="{ty}">{esc(eyebrow)}</text>')
        ty += 22
    out.append(f'<text class="{name_cls}" x="{x + 18}" y="{ty}">{esc(name)}</text>')
    ly = ty + 22
    for line in lines:
        out.append(f'<text class="body" x="{x + 18}" y="{ly}">{esc(line)}</text>')
        ly += 18
    return "".join(out)


def edge(d, plan=False):
    return f'<path class="{"edge-plan" if plan else "edge"}" d="{d}" marker-end="ARROW"/>'


def text(x, y, s, cls="elabel", anchor="start", rotate=None):
    t = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}"{t}>{esc(s)}</text>'


# ---------------------------------------------------------------------------------------------
# 1. The suite at a glance: four planes, the doors and the gate


def planes() -> str:
    L, LW, R, RW = 110, 520, 770, 380
    b = [
        text(40, 48, "The agent factory at a glance", "title"),
        text(40, 72, "DEFINE  ·  RUN  ·  JUDGE  ·  GOVERN", "lbl"),
        # left column
        box(L, 110, LW, 128, "Define", ["Native files and harness.lock, frozen from a good hangar run",
                                         "One identity everywhere: harness_digest",
                                         "ai-dlc contributes the optional workflow plugin and machine setup"],
            eyebrow="THE TEAM HARNESS REPO"),
        box(L, 300, LW, 146, "Run", ["Doors in, admission, intake posture, taint tracking",
                                      "Sandboxes, sessions, jobs and experiment trials on GKE",
                                      "Sealed graders; infrastructure errors retried and excluded",
                                      "Trusted verify, gateway push, landing on approval"],
            eyebrow="HANGAR", kind="box-hub", product="hangar"),
        box(L, 508, LW, 128, "Judge", ["Reads runs from a Parquet data plane, never from live hangar",
                                        "Paired statistics, behavior specs, nightly ADR checks",
                                        "Reports and promotion evidence posted on PRs"],
            eyebrow="FLIGHTDECK", product="flightdeck"),
        # right column
        box(R, 110, RW, 128, "Doors", ["Jira “Ready for agent”", "GitHub label or Projects column",
                                        "Slack @hangar · MCP from laptops · schedules"], eyebrow="MANY DOORS"),
        box(R, 300, RW, 146, "Govern", ["Cedar rules and human approvals", "The approver is never the requester",
                                         "Passports and signed receipts", "Fails closed: off, shadow, enforce"],
            eyebrow="TOWER", product="tower"),
        box(R, 508, RW, 128, "One gate: the PR", ["Tainted work opens as a draft",
                                                  "A second human approves the exact SHA",
                                                  "Questions and reviews reach people in Slack"],
            eyebrow="GITHUB"),
        # capabilities band
        box(L, 690, R + RW - L, 72, "Capabilities", ["MCP servers bound into sandboxes when they are claimed: Spaceport data products, internal tools, docs search"],
            eyebrow=None, kind="box-ext", product="spaceport", name_cls="name-s"),
        # edges
        edge(f"M{L + 170} 238V298"),
        text(L + 184, 264, "thaw: pin the harness,"), text(L + 184, 282, "check drift on turn 1"),
        edge(f"M{L + 110} 446V506"), text(L + 124, 472, "outbox"), text(L + 124, 490, "hangar.run/v1"),
        edge(f"M{L + 400} 508V448"), text(L + 386, 472, "trials", anchor="end"),
        text(L + 386, 490, "pin sets, experiments", anchor="end"),
        edge(f"M{L} 572H{L - 40}V174H{L - 2}"), text(L - 50, 373, "report, then promote the stable channel", rotate=-90, anchor="middle"),
        edge(f"M{R} 174H{R - 64}V330H{L + LW + 2}"), text(R - 74, 250, "work items", anchor="middle", rotate=-90),
        edge(f"M{L + LW} 372H{R - 2}"), text((L + LW + R) // 2, 364, "decide", anchor="middle"),
        edge(f"M{R} 412H{L + LW + 2}"), text((L + LW + R) // 2, 432, "receipt", anchor="middle"),
        edge(f"M{L + LW} 432H{R - 70}V572H{R - 2}"), text(R - 62, 524, "push,"), text(R - 62, 542, "open PR"),
        edge(f"M{L + LW} 442H{L + LW + 20}V688"),
        text(L + LW + 12, 672, "tools over MCP", anchor="end"),
    ]
    return svg(1200, 800, "The agent factory at a glance", b, dots=(900, 20, 300, 70))


# ---------------------------------------------------------------------------------------------
# 2. C4 level 1: system context


def context() -> str:
    P = dict(kind="person", name_cls="name-s", eyebrow="PERSON")
    X = dict(kind="box-ext", name_cls="name-s", eyebrow="EXTERNAL SYSTEM")
    b = [
        text(40, 48, "System context", "title"),
        text(40, 72, "C4 LEVEL 1  ·  WHO USES THE SUITE AND WHAT IT DEPENDS ON", "lbl"),
        box(40, 110, 210, 104, "Reviewer", ["Reviews agent PRs and", "approves the exact commit"], **P),
        box(380, 110, 210, 104, "Engineer", ["Hands work to agents and", "steers ~10 sessions"], **P),
        box(610, 110, 210, 104, "Harness owner", ["Runs experiments and", "promotes the harness"], **P),
        box(950, 110, 210, 104, "Approver", ["Decides release, landing,", "egress and secrets"], **P),
        box(380, 300, 440, 170, "Agent factory", ["Defines, runs, judges and governs cloud coding agents",
                                                    "hangar · flightdeck · Tower · ai-dlc",
                                                    "Every change leaves through a reviewed pull request"],
            eyebrow="SOFTWARE SYSTEM", kind="box-hub"),
        box(40, 300, 210, 104, "GitHub", ["Repos, PRs, checks, App,", "labels, Projects columns"], **X),
        box(40, 454, 210, 104, "Jira", ["Tickets moved to", "“Ready for agent”"], **X),
        box(950, 300, 210, 104, "Slack", ["Requests and questions,", "approval cards, digests"], **X),
        box(950, 454, 210, 104, "Model providers", ["Anthropic, OpenAI, Google", "APIs, with API keys"], **X),
        box(380, 600, 210, 104, "Google Cloud", ["GKE, Cloud Storage,", "Cloud Run, registry"], **X),
        box(610, 600, 210, 104, "MCP servers", ["Spaceport data products,", "internal tools, docs"], **X),
        # people
        edge("M145 214V298"), text(157, 262, "approves PRs"),
        edge("M485 214V298"), text(497, 248, "hands off work,"), text(497, 266, "answers questions"),
        edge("M715 214V298"), text(703, 248, "promotes", anchor="end"), text(703, 266, "harnesses", anchor="end"),
        edge("M1055 214V250H790V298"), text(1043, 240, "decides risky actions", anchor="end"),
        # GitHub, Jira
        edge("M380 334H252"), text(316, 326, "pushes, opens PRs", anchor="middle"),
        edge("M250 380H378"), text(314, 400, "webhooks", anchor="middle"),
        edge("M250 506H314V444H378"), text(322, 482, "webhooks"),
        # Slack, models
        edge("M820 334H948"), text(884, 326, "questions", anchor="middle"),
        edge("M950 380H822"), text(886, 400, "requests", anchor="middle"),
        edge("M820 444H886V506H948"), text(878, 482, "model calls", anchor="end"),
        # platform
        edge("M485 470V598"), text(497, 540, "runs on"),
        edge("M715 470V598"), text(727, 540, "calls tools"),
    ]
    return svg(1200, 736, "System context", b, dots=(900, 20, 300, 70))


# ---------------------------------------------------------------------------------------------
# 3. C4 level 2: containers and where they run


def containers() -> str:
    """Twelve containers: the three on an engineer's machine, the cluster, one storage box, the externals."""
    E = dict(kind="box-ext", name_cls="name-s", eyebrow="EXTERNAL")
    b = [
        text(40, 48, "Containers and where they run", "title"),
        text(40, 72, "C4 LEVEL 2  ·  SOLID: ON MAIN  ·  DASHED: PLANNED OR NOT YET WIRED", "lbl"),
        # engineer machine
        '<rect class="bound" x="30" y="100" width="240" height="460" rx="4"/>',
        text(46, 124, "ENGINEER MACHINE AND CI", "lbl"),
        box(46, 150, 208, 104, "Agent client", ["Claude Code or Codex", "with the hangar MCP"], eyebrow="CLI · MCP", name_cls="name-s"),
        box(46, 290, 208, 104, "ai-dlc", ["Machine setup, local work", "lifecycle, workflow plugin"], eyebrow="PYTHON CLI", product="aidlc", name_cls="name-s"),
        box(46, 430, 208, 104, "flightdeck", ["Ingest, statistics, specs,", "reports, experiments"], eyebrow="PYTHON CLI · DUCKDB", product="flightdeck", name_cls="name-s"),
        # google cloud
        '<rect class="bound" x="330" y="100" width="560" height="850" rx="4"/>',
        text(346, 124, "GOOGLE CLOUD PROJECT", "lbl"),
        '<rect class="bound" x="346" y="140" width="528" height="500" rx="4"/>',
        text(362, 164, "GKE CLUSTER", "lbl"),
        box(362, 180, 220, 264, "hangar control plane", ["REST, MCP and web UI :8787", "Jobs, sessions, intake",
                                                          "Landing and the inbox", "SQLite on a persistent disk",
                                                          "Writes the run outbox"],
            eyebrow="PYTHON · ALWAYS ON", kind="box-hub", product="hangar", name_cls="name-s"),
        box(650, 180, 208, 124, "Tower", ["Decision point, approvals,", "receipts, passports"],
            eyebrow="ON MAIN · NOT DEPLOYED", product="tower", name_cls="name-s"),
        box(650, 340, 208, 104, "Gateway and egress", ["Git gateway :8788", "Egress proxy :3128"],
            eyebrow="CONTROL PLANE POD", product="hangar", name_cls="name-s"),
        box(362, 500, 496, 112, "Agent sandboxes", ["Claude Code, Codex, pi, Antigravity · gVisor on Spot nodes, 0 to N",
                                                    "Pools off 01:00–10:00 ET · optional Kata heavy tier for Docker"],
            eyebrow="AGENT SANDBOX ADD-ON", product="hangar", name_cls="name-s"),
        box(346, 670, 528, 124, "Storage", ["Checkpoints: session state that outlives the disk",
                                             "Run outbox: hangar.run/v1, written once · off in the deploy",
                                             "Data plane: Parquet tables, one folder a day"],
            eyebrow="CLOUD STORAGE · ARTIFACT REGISTRY FOR IMAGES", name_cls="name-s"),
        box(346, 826, 528, 104, "Compactor", ["Flattens new runs into Parquet each night, while the sandbox pools are off"],
            eyebrow="CLOUD RUN JOB · NIGHTLY · NOT DEPLOYED", product="flightdeck", name_cls="name-s"),
        # externals
        box(940, 150, 230, 104, "Jira and Slack", ["Doors in; questions and", "approvals out"], **E),
        box(940, 340, 230, 104, "GitHub", ["Team repos, PRs, the App,", "the team harness repo"], **E),
        box(940, 470, 230, 104, "Model providers", ["Reached only through", "the egress allowlist"], **E),
        box(940, 600, 230, 104, "MCP servers", ["Spaceport, internal tools,", "bound at claim time"], kind="box-ext", name_cls="name-s", eyebrow="EXTERNAL", product="spaceport"),
        # engineer -> control plane
        edge("M254 222H360"), text(262, 214, "MCP / REST"),
        edge("M254 470H300V300H360"), text(306, 292, "trials"),
        edge("M254 510H316V980H1190V732H876"), text(750, 1000, "flightdeck reads Parquet", anchor="middle"),
        # inside the cluster
        edge("M582 240H648", plan=True), text(616, 232, "decide", anchor="middle"),
        edge("M472 444V498"), text(480, 476, "creates"),
        edge("M754 500V446"), text(762, 478, "git, egress"),
        # to storage: checkpoints always; the outbox and the compactor are on main but off in the GKE deploy (hangar#273)
        edge("M362 420H354V652H430V668"), text(438, 652, "checkpoints, runs"),
        edge("M520 794V824", plan=True), edge("M700 826V796", plan=True),
        # to externals
        edge("M858 380H938"), text(866, 372, "push"),
        edge("M858 420H916V522H938"),
        edge("M858 580H902V652H938"),
        # webhooks bus over the top
        edge("M1170 392H1184V88H472V178"), '<path class="edge" d="M1170 202H1184"/>',
        text(1176, 80, "webhooks from GitHub, Jira and Slack", anchor="end"),
    ]
    return svg(1200, 1020, "Containers and where they run", b)


# ---------------------------------------------------------------------------------------------
# 4. A ticket's journey: the seven steps on docs/how-it-fits.md, wide and stacked

JOURNEY_STYLE = """
<style>
  .af-d .step { fill: var(--af-canvas, #000); stroke: var(--af-fg-subtle, #8A8A8A); stroke-width: 1; }
  .af-d .stepn { font: 500 12px "DM Mono", ui-monospace, Menlo, monospace; fill: var(--af-fg, #fff); }
  .af-d .hub-lbl { font: 500 12px "DM Mono", ui-monospace, Menlo, monospace; letter-spacing: .08em; fill: var(--af-fg-subtle, #8A8A8A); }
</style>
"""


def step(x, y, n) -> str:
    """A numbered marker that ties a part of the drawing to step n of the text."""
    return (f'<circle class="step" cx="{x}" cy="{y}" r="9"/>'
            f'<text class="stepn" x="{x}" y="{y + 4}" text-anchor="middle">{n}</text>')


def journey() -> str:
    hub_x, hub_w, row, row_h = 250, 620, 250, 170
    inner_y, inner_w, inner_h = 280, 180, 112
    ix = (266, 468, 670)                       # intake, sandbox, verify inside the hangar box
    cx = [x + inner_w // 2 for x in ix]
    low_y, low_w, low_h = 500, 190, 120
    lx = (250, 465, 680)                       # flightdeck, compactor, outbox (data flows right to left)
    I = dict(kind="box-ext", name_cls="name-s")
    b = [JOURNEY_STYLE,
         text(40, 48, "A ticket's journey", "title"),
         text(40, 72, "SEVEN STEPS  ·  SOLID: ON MAIN  ·  DASHED: TOWER BUILT, HANGAR WIRING OPEN", "lbl"),
         # Tower above hangar
         box(hub_x, 96, hub_w, 104, "Decision point", ["Answers allow, deny or wait, and signs a receipt",
                                                       "A wait goes to an approver who is not the requester"],
             eyebrow="TOWER · GOVERN", product="tower", name_cls="name-s"),
         # main row: doors, hangar, the gate
         box(40, row, 170, row_h, "Doors", ["Jira, GitHub, Slack,", "MCP, schedules"], eyebrow="MANY DOORS",
             name_cls="name-s"),
         f'<rect class="box-hub" x="{hub_x}" y="{row}" width="{hub_w}" height="{row_h}" rx="3"/>',
         f'<rect x="{hub_x}" y="{row}" width="{hub_w}" height="2" fill="{PRODUCT["hangar"]}"/>',
         text(hub_x + 16, row + row_h - 12, "HANGAR · RUN", "hub-lbl"),
         box(ix[0], inner_y, inner_w, inner_h, "Admit", ["Signed webhook; tainted", "Budget and review cap"],
             eyebrow="INTAKE", **I),
         box(ix[1], inner_y, inner_w, inner_h, "Claim", ["team-default@stable", "harness_digest, trace"],
             eyebrow="SANDBOX", **I),
         box(ix[2], inner_y, inner_w, inner_h, "Deliver", ["The repo's own checks", "One commit, a draft PR"],
             eyebrow="VERIFY · GATEWAY", **I),
         box(910, row, 250, row_h, "One gate: the PR", ["Review packet, Harness-Digest", "A second human approves",
                                                         "the exact commit"], eyebrow="GITHUB", name_cls="name-s"),
         # bottom row: outbox -> compactor -> flightdeck -> the team harness repo
         box(40, low_y, 170, low_h, "Harness repo", ["harness.lock", "channels.yaml", "promotion by PR"],
             eyebrow="DEFINE", name_cls="name-s"),
         box(lx[0], low_y, low_w, low_h, "Judge", ["Parquet and DuckDB", "stable vs candidate", "on pinned trials"],
             eyebrow="FLIGHTDECK · JUDGE", product="flightdeck", name_cls="name-s"),
         box(lx[1], low_y, low_w, low_h, "Compactor", ["Outbox to Parquet", "flightdeck.parquet/v1"],
             eyebrow="CLOUD RUN · NIGHTLY", product="flightdeck", name_cls="name-s"),
         box(lx[2], low_y, low_w, low_h, "Run outbox", ["Each run written once", "run.json last"], eyebrow="GCS",
             name_cls="name-s"),
         # 1, 2, 3, 5: along the top row
         edge(f"M210 336H{ix[0] - 2}"), step(237, 320, 1),
         edge(f"M{ix[0] + inner_w} 336H{ix[1] - 2}"), edge(f"M{ix[1] + inner_w} 336H{ix[2] - 2}"),
         step(ix[0] + inner_w - 16, inner_y + 18, 2), step(ix[1] + inner_w - 16, inner_y + 18, 3),
         edge(f"M{ix[2] + inner_w} 336H908"), step(880, 320, 5),
         # 4 (and 2, 5): decide down, receipt up, at each enforcement point
         *[edge(f"M{c - 10} 200V{inner_y - 2}", plan=True) + edge(f"M{c + 10} {inner_y}V202", plan=True) for c in cx],
         text(cx[0] - 16, 236, "decide", anchor="end"), text(cx[0] + 16, 236, "receipt"),
         step(cx[1] + 32, 236, 4),
         # 6: every finished run goes out once, and is compacted overnight
         edge(f"M{cx[2]} {inner_y + inner_h}V{low_y - 2}"), step(cx[2] + 18, 470, 6),
         text(cx[2] - 10, 470, "every run", anchor="end"),
         edge(f"M{lx[2]} 560H{lx[1] + low_w + 2}"), edge(f"M{lx[1]} 560H{lx[0] + low_w + 2}"),
         # 7: the verdict on the harness PR, then stable moves and the next claim uses it
         edge(f"M{lx[0]} 560H212"), step(231, 544, 7),
         edge(f"M190 {low_y}V460H{cx[1]}V{inner_y + inner_h + 2}"),
         text(222, 452, "the next claim uses the new stable"),
         # legend
         text(910, 530, "NUMBERS MATCH THE STEPS", "lbl"), text(910, 548, "IN THE TEXT", "lbl"),
         text(910, 578, "Tower's side is built; hangar's"), text(910, 596, "wiring is hangar#172 and #173"),
         ]
    return svg(1200, 660, "A ticket's journey", b, dots=(900, 20, 300, 70), pid="journey")


def journey_stacked() -> str:
    """The same seven steps, one above the other, for phone-width pages."""
    x, w, h, gap, y0 = 20, 350, 104, 34, 100
    steps_ = [
        ("DOORS", "Ready for agent", ["A ticket moves; a signed webhook", "reaches hangar"], None, "box"),
        ("HANGAR · INTAKE", "Admit", ["Tainted: ticket text is untrusted", "Within budget and reviewer capacity"],
         "hangar", "box"),
        ("HANGAR · SANDBOX", "Claim team-default@stable", ["The manifest records harness_digest",
                                                             "Every step streams into a trace"], "hangar", "box"),
        ("TOWER · GOVERN", "Ask before a risky step", ["Allow, deny or wait, with a receipt",
                                                       "A wait goes to someone else"], "tower", "box-plan"),
        ("HANGAR · GATEWAY", "Verify and open the PR", ["Repo checks, one commit, a draft PR",
                                                        "A second human approves the commit"], "hangar", "box"),
        ("OUTBOX · COMPACTOR", "Captured once", ["The run lands in the GCS outbox",
                                                 "and in Parquet overnight"], None, "box"),
        ("FLIGHTDECK · HARNESS REPO", "Judge, then promote", ["Stable vs candidate on pinned trials",
                                                              "A different person moves stable"], "flightdeck", "box"),
    ]
    b = [JOURNEY_STYLE, text(20, 44, "A ticket's journey", "title"),
         text(20, 68, "SOLID: ON MAIN  ·  DASHED: HANGAR WIRING OPEN", "lbl")]
    ys = []
    for i, (eyebrow, name, lines, product, kind) in enumerate(steps_):
        y = y0 + i * (h + gap)
        ys.append(y)
        b.append(box(x, y, w, h, name, lines, eyebrow=eyebrow, kind=kind, product=product, name_cls="name-s"))
        b.append(step(x + w - 22, y + 22, i + 1))
        if i:
            b.append(edge(f"M{x + 40} {y - gap}V{y - 2}", plan=kind == "box-plan" or steps_[i - 1][4] == "box-plan"))
    # the loop: the promoted stable is what the next claim runs
    y3, y7 = ys[2] + h // 2, ys[6] + h // 2
    b.append(edge(f"M{x + w} {y7}H{x + w + 22}V{y3}H{x + w + 2}"))
    b.append(text(x + w + 36, (y3 + y7) // 2, "the next claim uses the new stable", anchor="middle", rotate=-90))
    end = ys[-1] + h
    b.append(text(20, end + 34, "Tower's side is built; hangar's wiring is", "elabel"))
    b.append(text(20, end + 52, "hangar#172 and #173.", "elabel"))
    return svg(420, end + 72, "A ticket's journey, stacked", b, pid="journey-stacked")


FONT_SIZE = re.compile(r"font(?:-size)?:[^;}]*?(\d+(?:\.\d+)?)px")


def check_floor(svg_text: str, name: str) -> None:
    """Every font size a drawing declares is at least FLOOR px at source size."""
    small = sorted({float(m) for m in FONT_SIZE.findall(svg_text) if float(m) < FLOOR})
    if small:
        raise SystemExit(f"diagrams: {name} declares {small} px type; the floor is {FLOOR}px")


def write(name: str, fn) -> None:
    text_ = with_fallbacks(fn())
    check_floor(text_, name)
    (OUT / f"{name}.svg").write_text(text_)
    print("wrote", OUT / f"{name}.svg")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("planes", planes), ("c4-context", context), ("c4-containers", containers),
                     ("journey", journey), ("journey-stacked", journey_stacked)):
        write(name, fn)


# ---------------------------------------------------------------------------------------------
# Slide-sized drawings: fewer words, larger type, made for 1280×720 slides


SLIDE_STYLE = """
<style>
  .af-d .name { font-size: 22px; }
  .af-d .body { font-size: 16px; }
  .af-d .lbl { font-size: 12.5px; }
  .af-d .elabel { font-size: 15px; }
</style>
"""


def sbox(x, y, w, h, eyebrow, name, lines=(), kind="box", product=None):
    out = [f'<rect class="{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>']
    if product:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="3" fill="{PRODUCT[product]}"/>')
    out.append(f'<text class="lbl" x="{x + 22}" y="{y + 32}">{esc(eyebrow)}</text>')
    out.append(f'<text class="name" x="{x + 22}" y="{y + 64}">{esc(name)}</text>')
    for i, line in enumerate(lines):
        out.append(f'<text class="body" x="{x + 22}" y="{y + 94 + 24 * i}">{esc(line)}</text>')
    return "".join(out)


def slide_planes() -> str:
    b = [SLIDE_STYLE,
         sbox(40, 20, 330, 150, "DOORS", "Many doors", ["Jira, GitHub, Slack, MCP,", "schedules"]),
         sbox(40, 230, 330, 150, "TEAM HARNESS REPO", "Define", ["Native files, harness.lock,", "one digest"]),
         sbox(470, 120, 340, 260, "HANGAR", "Run", ["Sandboxes, sessions, jobs", "and trials on GKE", "Verify, push through the", "gateway, land on approval"], kind="box-hub", product="hangar"),
         sbox(910, 20, 330, 150, "TOWER", "Govern", ["Rules, human approvals,", "signed receipts"], product="tower"),
         sbox(910, 230, 330, 150, "GITHUB", "One gate: the PR", ["A second human approves", "the exact commit"]),
         sbox(470, 440, 340, 150, "FLIGHTDECK", "Judge", ["Paired statistics and", "behavior specs on every run"], product="flightdeck"),
         edge("M370 95H420V180H468"), text(380, 85, "work"),
         edge("M370 305H468"), text(380, 295, "lock"),
         edge("M810 165H860V95H908"), text(820, 155, "decide"),
         edge("M908 130H880V200H812"), text(888, 230, ""),
         edge("M810 305H908"), text(820, 295, "PR"),
         edge("M560 380V438"), text(572, 418, "every run"),
         edge("M720 440V382"), text(708, 418, "trials", anchor="end"),
         edge("M470 515H205V382"), text(215, 505, "promote the next harness"),
         ]
    return svg(1280, 610, "Four planes, one loop", b)


def slide_loop() -> str:
    cx, cy, r = 640, 300, 210
    import math
    steps = [("1", "Change", "a skill, hook or plugin in the harness", "harness"),
             ("2", "Freeze", "a good run into harness.lock", "hangar"),
             ("3", "Experiment", "stable vs candidate, paired", "flightdeck"),
             ("4", "Report", "verdict with intervals on the PR", "flightdeck"),
             ("5", "Promote", "move stable; drift checks guard it", "hangar")]
    b = [SLIDE_STYLE, f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="var(--af-rule, #3A3A3A)" stroke-width="1.25" stroke-dasharray="3 6"/>',
         text(cx, cy - 8, "harness_digest", "name", anchor="middle"),
         text(cx, cy + 22, "ONE IDENTITY FROM LOCK TO REPORT", "lbl", anchor="middle")]
    for i, (n, name, line, prod) in enumerate(steps):
        a = -math.pi / 2 + i * 2 * math.pi / len(steps)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="{PRODUCT[prod]}"/>')
        right = math.cos(a) >= -0.01
        tx = x + (26 if right else -26)
        anchor = "start" if right else "end"
        if abs(math.cos(a)) < 0.2:
            tx, anchor = x + 22, "start"
        b.append(text(tx, y - 4, f"{n}  {name}", "name", anchor=anchor))
        b.append(text(tx, y + 22, line, "body", anchor=anchor))
    return svg(1280, 600, "The harness improvement loop", b)


def main_slides() -> None:
    for name, fn in (("slide-planes", slide_planes), ("slide-loop", slide_loop)):
        write(name, fn)


if __name__ == "__main__":
    main()
    main_slides()
