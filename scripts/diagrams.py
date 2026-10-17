"""Build the suite's architecture diagrams as theme-aware SVG.

Every color is an Airframe token (`var(--af-*, <dark fallback>)`), so a diagram inlined in a docs
page follows the page's theme, and the same file opened on its own renders in the dark flavor.
`scripts/render.py` turns them into PNGs for slides and READMEs.

    python3 scripts/diagrams.py            # writes docs/assets/diagrams/*.svg
"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets" / "diagrams"

STYLE = """
<style>
  .af-d .bg { fill: var(--af-canvas, #000); }
  .af-d .box { fill: var(--af-raised, #141414); }
  .af-d .box-hub { fill: var(--af-raised, #141414); stroke: var(--af-brand-line, #FFC400); stroke-width: 1.5; }
  .af-d .box-plan { fill: none; stroke: var(--af-line-strong, #6B6B6B); stroke-width: 1; stroke-dasharray: 4 4; }
  .af-d .box-ext { fill: var(--af-surface, #0A0A0A); stroke: var(--af-line-strong, #6B6B6B); stroke-width: 1; }
  .af-d .person { fill: var(--af-surface, #0A0A0A); stroke: var(--af-fg-subtle, #8A8A8A); stroke-width: 1; }
  .af-d .bound { fill: none; stroke: var(--af-rule, #3A3A3A); stroke-width: 1; stroke-dasharray: 2 5; }
  .af-d .bound-fill { fill: var(--af-surface, #0A0A0A); }
  .af-d .name { font: 700 15px "Archivo", "Helvetica Neue", Arial, sans-serif; font-stretch: 125%; fill: var(--af-fg, #fff); }
  .af-d .name-s { font: 700 13px "Archivo", "Helvetica Neue", Arial, sans-serif; font-stretch: 125%; fill: var(--af-fg, #fff); }
  .af-d .title { font: 700 20px "Archivo", "Helvetica Neue", Arial, sans-serif; font-stretch: 125%; fill: var(--af-fg, #fff); }
  .af-d .body { font: 400 12.5px "Red Hat Text", "Helvetica Neue", Arial, sans-serif; fill: var(--af-fg-muted, #A6A6A6); }
  .af-d .lbl { font: 500 10.5px "DM Mono", ui-monospace, Menlo, monospace; letter-spacing: .08em; fill: var(--af-fg-subtle, #8A8A8A); }
  .af-d .lbl-hi { font: 500 10.5px "DM Mono", ui-monospace, Menlo, monospace; letter-spacing: .08em; fill: var(--af-brand-text, #FFC400); }
  .af-d .edge { fill: none; stroke: var(--af-fg-subtle, #8A8A8A); stroke-width: 1.25; }
  .af-d .edge-plan { fill: none; stroke: var(--af-fg-subtle, #8A8A8A); stroke-width: 1.25; stroke-dasharray: 5 4; }
  .af-d .elabel { font: 400 11.5px "Red Hat Text", "Helvetica Neue", Arial, sans-serif; fill: var(--af-fg-subtle, #8A8A8A); }
  .af-d .arrowhead { fill: var(--af-fg-subtle, #8A8A8A); }
  .af-d .dot { fill: var(--af-dot, #262626); }
</style>
"""

PRODUCT = {
    "hangar": "var(--af-p-hangar, #EE8F63)",
    "flightdeck": "var(--af-p-flightdeck, #D98CD2)",
    "workspace": "var(--af-p-workspace, #C5A93B)",
    "aidlc": "var(--af-p-aidlc, #69C27E)",
    "spaceport": "var(--af-p-spaceport, #B199F4)",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w: int, h: int, label: str, body: list[str], dots: tuple[int, int, int, int] | None = None) -> str:
    pid = label.lower().replace(" ", "-")[:24]
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
        box(L, 110, LW, 128, "Define", ["ai-dlc authors the team workflow plugin and provisions machines",
                                         "The team harness repo holds harness.lock and native files",
                                         "One identity everywhere: harness_digest"],
            eyebrow="AI-DLC  +  TEAM HARNESS REPO", product="aidlc"),
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
            eyebrow="GOVERNED WORKSPACE", product="workspace"),
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
        text(L + 386, 490, "hangar.experiment/v1", anchor="end"),
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
                                                    "hangar · flightdeck · governed workspace · ai-dlc",
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
    E = dict(kind="box-ext", name_cls="name-s", eyebrow="EXTERNAL")
    b = [
        text(40, 48, "Containers and where they run", "title"),
        text(40, 72, "C4 LEVEL 2  ·  SOLID: ON MAIN  ·  DASHED: IN REVIEW OR PLANNED", "lbl"),
        # engineer machine
        '<rect class="bound" x="30" y="100" width="240" height="600" rx="4"/>',
        text(46, 124, "ENGINEER MACHINE AND CI", "lbl"),
        box(46, 150, 208, 104, "Agent client", ["Claude Code or Codex", "with the hangar MCP"], eyebrow="CLI · MCP", name_cls="name-s"),
        box(46, 290, 208, 104, "ai-dlc", ["Machine setup, local work", "lifecycle, workflow plugin"], eyebrow="PYTHON CLI", product="aidlc", name_cls="name-s"),
        box(46, 430, 208, 104, "flightdeck", ["Ingest, statistics, specs,", "reports, experiments"], eyebrow="PYTHON CLI · DUCKDB", product="flightdeck", name_cls="name-s"),
        box(46, 570, 208, 104, "Nightly checks", ["GitHub Actions: canary", "and flightdeck checks"], eyebrow="CI", kind="box-plan", name_cls="name-s"),
        # google cloud
        '<rect class="bound" x="330" y="100" width="560" height="846" rx="4"/>',
        text(346, 124, "GOOGLE CLOUD PROJECT", "lbl"),
        '<rect class="bound" x="346" y="140" width="528" height="500" rx="4"/>',
        text(362, 164, "GKE CLUSTER", "lbl"),
        box(362, 180, 220, 264, "hangar control plane", ["REST, MCP and web UI :8787", "Jobs, sessions, intake",
                                                          "Landing and the inbox", "SQLite on a persistent disk",
                                                          "Writes the run outbox"],
            eyebrow="PYTHON · ALWAYS ON", kind="box-hub", product="hangar", name_cls="name-s"),
        box(650, 180, 208, 124, "Governed workspace", ["Decision point, approvals,", "receipts, passports"],
            eyebrow="PLANNED · SPEC 0015", kind="box-plan", product="workspace", name_cls="name-s"),
        box(650, 340, 208, 104, "Gateway and egress", ["Git gateway :8788", "Egress proxy :3128"],
            eyebrow="IN THE CONTROL PLANE POD", product="hangar", name_cls="name-s"),
        box(362, 500, 496, 112, "Agent sandboxes", ["Claude Code, Codex, pi, Antigravity · gVisor on Spot nodes, 0 to N",
                                                    "Pools off 01:00–10:00 ET · optional Kata heavy tier for Docker"],
            eyebrow="AGENT SANDBOX ADD-ON", product="hangar", name_cls="name-s"),
        box(346, 670, 168, 108, "Checkpoints", ["Session state that", "outlives the disk"], eyebrow="GCS", name_cls="name-s"),
        box(530, 670, 168, 108, "Run outbox", ["hangar.run/v1,", "written once"], eyebrow="GCS · IN REVIEW", kind="box-plan", name_cls="name-s"),
        box(714, 670, 160, 108, "Data plane", ["Parquet tables,", "one folder a day"], eyebrow="GCS · PLANNED", kind="box-plan", name_cls="name-s"),
        box(346, 806, 168, 116, "Images", ["Environment images", "and harness packs"], eyebrow="ARTIFACT REGISTRY", name_cls="name-s"),
        box(530, 806, 344, 116, "Compactor", ["Flattens new runs into Parquet each", "night, while the sandbox pools are off"],
            eyebrow="CLOUD RUN JOB · PLANNED", kind="box-plan", product="flightdeck", name_cls="name-s"),
        # externals
        box(940, 150, 230, 104, "Jira and Slack", ["Doors in; questions and", "approvals out"], **E),
        box(940, 340, 230, 104, "GitHub", ["Team repos, PRs, the App,", "the team harness repo"], **E),
        box(940, 470, 230, 104, "Model providers", ["Reached only through", "the egress allowlist"], **E),
        box(940, 600, 230, 104, "MCP servers", ["Spaceport, internal tools,", "bound at claim time"], kind="box-ext", name_cls="name-s", eyebrow="EXTERNAL", product="spaceport"),
        # engineer -> control plane
        edge("M254 222H360"), text(262, 214, "MCP / REST"),
        edge("M254 470H300V300H360", plan=True), text(306, 292, "submit"),
        edge("M254 510H316V962H882V724H876", plan=True), text(600, 980, "flightdeck reads Parquet", anchor="middle"),
        # inside the cluster
        edge("M582 240H648", plan=True), text(616, 232, "decide", anchor="middle"),
        edge("M472 444V498"), text(480, 476, "creates"),
        edge("M754 500V446"), text(762, 478, "git, egress"),
        # to storage
        edge("M362 420H354V652H614V668", plan=True),
        edge("M354 652H430V668"),
        edge("M614 778V804", plan=True), edge("M794 806V780", plan=True),
        # to externals
        edge("M858 380H938"), text(866, 372, "push"),
        edge("M858 420H916V522H938"),
        edge("M858 580H902V652H938"),
        # webhooks bus over the top
        edge("M1170 392H1184V88H472V178"), '<path class="edge" d="M1170 202H1184"/>',
        text(1176, 80, "webhooks from GitHub, Jira and Slack", anchor="end"),
    ]
    return svg(1200, 996, "Containers and where they run", b)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in (("planes", planes), ("c4-context", context), ("c4-containers", containers)):
        (OUT / f"{name}.svg").write_text(fn())
        print("wrote", OUT / f"{name}.svg")


if __name__ == "__main__":
    main()
