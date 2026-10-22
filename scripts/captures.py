#!/usr/bin/env python3
"""Capture the products as they are now, from their own demos, for the deck and the docs.

    python3 scripts/captures.py                      # every product; sibling checkouts ../hangar, ../tower, ../flightdeck
    python3 scripts/captures.py hangar tower         # some of them
    HANGAR_DIR=… TOWER_DIR=… FLIGHTDECK_DIR=… python3 scripts/captures.py

Writes docs/assets/captures/<product>-<screen>.png (a 1440x900 window, Night, at 2x) and captures.json: what each
one shows, the repository and commit it came from, and when. A screen a docs page shows (DAY) also gets a Day twin,
<product>-<screen>-day.png, which the page swaps in for the light scheme. deck/src.html and the docs pages reference them;
nothing here is drawn or retouched by hand, so a capture is regenerated, never edited.

A full window shown 600 px wide puts the product's text at 3-4 px, so each screen also has named crops (CROPS): the
subject of the screen, cut from the full capture by the same script, as <product>-<screen>-<crop>.png. A page or a
slide shows the crop; the full capture stays behind a link.

    python3 scripts/captures.py --crops              # re-cut the crops from the captures already here (no demos)

Every product is captured from its own demo and fixture data through its real UI, never from a stub:

- hangar: docs/assets/front/demo.py (the real control plane on the fake provider, a scripted agent and a stand-in
  GitHub) on its own port, and the demo ticket (issue #42 becomes a job, a sandbox run and draft PR #43): the job's
  change and composer. Needs you and the Fleet are a team's afternoon, docs/assets/front/fixture.py served over the
  same console as hangar's own front-page stills do: the decision deck with a held push on top, the agents as rows.
- Tower: server/tools/ui_tour.py (the offline demo and its stand-ins, with the tour's seed), as Marcus, an approver.
  Screens: the Desk; an object page with its chips, composer and card.
- flightdeck: docs/assets/report-comment-full-{dark,light}.html, rendered by docs/assets/build.py from the fixture
  experiment: the verdict as the pull-request comment.
- Airframe: this repository's gallery previews (ApprovalCard, Diff), built by scripts/airframe.py gallery, plus a
  Night thumbnail of every component's preview in docs/assets/airframe/ for the Components page.

Needs Playwright with Chromium here (pip install playwright; python -m playwright install chromium) and each
product's own environment: HANGAR_PYTHON (default `uv run --project <dir> python`) and TOWER_PYTHON (default
<dir>/server/.venv/bin/python, as Tower's own tour uses).
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from datetime import date
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "captures"
VIEW = {"width": 1440, "height": 900}
# The narrow window: a second capture of each hangar screen at 720 CSS px, the width a docs column or a slide shows it
# at, so the product's own responsive layout puts the subject in frame and its text renders at or near 1:1.
NARROW = {"width": 720, "height": 900}
# The Fleet's rows at the widest window a deck slide shows legibly: wide enough for the desktop row, narrow enough to cut.
MID = {"width": 940, "height": 900}
PRODUCTS = ("hangar", "tower", "flightdeck", "airframe")
PEOPLE = {"marcus": 102}  # Tower's demo: Marcus Chen, an approver
SCALE = 2  # device_scale_factor of every capture

# Where a crop is shown, and the CSS width (and height) it gets there: the docs home hero at 1440, a tool page's content
# column, a deck screen slide (max-height 500). A crop is cut no wider than shown / LEGIBLE, so the product's 13 px
# labels render at 11 px or more where the page shows them; the test enforces it.
SHOWN = {"hero": (610, 900), "page": (690, 2000), "deck": (800, 500)}
LEGIBLE = 0.85

# Named crops, in the window's CSS pixels (x, y, width, height), what the crop shows, and the surfaces that show it.
# The box frames the one thing the page or slide is about, at a width that keeps its text legible there.
CROPS = {
    "hangar-fleet": {
        "deck": ((64, 232, 672, 384), "The Fleet's decision deck: a held git push to main with the work, the command, Deny, Allow for this turn and Approve push", ("hero",)),
    },
    "hangar-fleet-rows": {
        "list": ((16, 58, 908, 548), "The Fleet's rows for base-codex: eight agents, what each is doing, its owner, stage rail and stage times", ("deck",)),
    },
    "hangar-needs-you-narrow": {
        "decision": ((0, 56, 720, 512), "Needs you in a 720 px window: the decision deck with a held git push to main on top, ending at the card stack, with Approve push", ("page", "deck")),
    },
    "hangar-review-narrow": {
        "change": ((0, 68, 720, 588), "Job #42 in a 720 px window: the agent's summary, the reply box, and the first file's change as a greyscale diff, whole", ("deck",)),
    },
    "tower-desk": {
        "approval": ((264, 160, 656, 588), "Needs you on Marcus's Desk: the decision deck with a ticket for Globex to approve, what will run and what approving does", ("page", "deck")),
    },
    "tower-object": {
        "composer": ((264, 168, 680, 316), "Start work about PAY-412: the composer addressed to Breaks, the issue as a chip with its state, and suggested asks", ("deck",)),
    },
    "flightdeck-verdict": {
        "verdict": ((0, 0, 800, 484), "The report as GitHub shows the comment on the harness PR: the verdict, the experiment, the rule, the outcome table and the paired difference", ("page", "deck")),
    },
    "airframe-approvalcard": {
        "card": ((16, 12, 780, 584), "One ApprovalCard: a held push to main with its policy, checks, expiry, deny and approve, and the quorum", ("deck",)),
    },
}

# The screens a docs page shows, which get a Day twin (<name>-day.png) cut with the same boxes; the deck is Night only.
# The deck follows the docs page's scheme, so the screens a slide shows get a twin too.
DAY = ("hangar-fleet", "hangar-needs-you-narrow", "hangar-fleet-rows", "hangar-review-narrow", "tower-desk", "tower-object",
       "flightdeck-verdict")
CROPS.update({f"{name}-day": CROPS[name] for name in DAY})

# Extra work for hangar's demo, so the Fleet shows a pool rather than three tiles. Each becomes a real job on the
# scripted agent; most finish in seconds and leave their sandbox up.
MORE_JOBS = [  # each title lands on one of the scripted agent's paths (ruff, refund, non-ASCII), so the work finishes
    ("Bump ruff in CI and fix the new findings", "Bump ruff to 0.15 in the workflow and fix whatever it newly flags."),
    ("Refund line items, not whole orders", "Let POST /refunds take line items so a partial refund does not refund the order."),
    ("Keep non-ASCII names in the invoice export", "Invoice PDFs drop accented customer names the same way the CSV export did; keep UTF-8."),
    ("Add a reason to the refunds API", "Each refund should carry a reason code; store it and show it on the order."),
    ("Bump ruff for the dev tools", "Bump ruff in the dev dependencies to match CI."),
    ("Export non-ASCII addresses in the shipping file", "The shipping export drops non-ASCII street names; encode as UTF-8 like the CSV export."),
]


def repo_dir(product: str) -> Path:
    env = {"hangar": "HANGAR_DIR", "tower": "TOWER_DIR", "flightdeck": "FLIGHTDECK_DIR"}[product]
    d = Path(os.environ.get(env) or ROOT.parent / product).resolve()
    if not d.is_dir():
        sys.exit(f"captures: {product} checkout not found at {d} (set {env})")
    return d


def commit(d: Path) -> str:
    try:
        return subprocess.run(["git", "-C", str(d), "rev-parse", "--short", "HEAD"], check=True,
                              capture_output=True, text=True).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def python_for(product: str, d: Path) -> list[str]:
    env = os.environ.get({"hangar": "HANGAR_PYTHON", "tower": "TOWER_PYTHON"}[product])
    if env:
        return shlex.split(env)
    if product == "tower":
        return [str(d / "server" / ".venv" / "bin" / "python")]
    return ["uv", "run", "--project", str(d), "python"]


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def http(url: str, token: str | None = None, data: dict | None = None, timeout: float = 30):
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                 headers={"content-type": "application/json", **({"authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    return json.loads(body) if body else {}


def wait_for(check, what: str, timeout: float = 90, every: float = 0.5) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if check():
                return
        except (urllib.error.URLError, ConnectionError, OSError, json.JSONDecodeError):
            pass
        time.sleep(every)
    raise TimeoutError(f"captures: {what} did not happen within {timeout:.0f} s")


class Browser:
    def __init__(self, pw):
        self.b = pw.chromium.launch()

    def page(self, init: str | None = None, viewport: dict | None = None, scheme: str = "dark"):
        ctx = self.b.new_context(viewport=viewport or VIEW, device_scale_factor=2, color_scheme=scheme)
        if init:
            ctx.add_init_script(init)
        return ctx.new_page()

    def close(self) -> None:
        self.b.close()


def shoot(page, name: str, clip: dict | None = None) -> None:
    page.evaluate("document.fonts.ready")
    page.wait_for_timeout(400)
    page.screenshot(path=str(OUT / f"{name}.png"), clip=clip)
    print("captures: wrote", OUT / f"{name}.png")
    cut(name)


def cut(name: str) -> list[str]:
    """Write the named crops of one capture from its full PNG; returns the names written."""
    from PIL import Image

    written = []
    src = OUT / f"{name}.png"
    if name not in CROPS or not src.exists():
        return written
    with Image.open(src) as img:
        for crop, ((x, y, w, h), _, _) in CROPS[name].items():
            box = (x * SCALE, y * SCALE, min((x + w) * SCALE, img.width), min((y + h) * SCALE, img.height))
            out = OUT / f"{name}-{crop}.png"
            img.crop(box).save(out, optimize=True)
            print("captures: wrote", out)
            written.append(out.name)
    return written


def crops_manifest() -> dict:
    return {f"{name}-{crop}": {"from": name, "box": list(box), "shows": shows, "shown": list(where)}
            for name, crops in CROPS.items() for crop, (box, shows, where) in crops.items()}


# ------------------------------------------------------------------------------------------------------- hangar
def hangar(br: Browser, manifest: dict) -> None:
    d = repo_dir("hangar")
    demo = d / "docs" / "assets" / "front" / "demo.py"
    token = re.search(r'^TOKEN = "([^"]+)"', demo.read_text(), re.M).group(1)
    port = free_port()
    url = f"http://127.0.0.1:{port}"
    env = {**os.environ, "HANGAR_DEMO_PORT": str(port)}
    log = open(OUT / ".hangar-demo.log", "w")
    proc = subprocess.Popen(python_for("hangar", d) + [str(demo)], cwd=d, env=env, stdout=log, stderr=subprocess.STDOUT)
    try:
        def jobs():
            got = http(f"{url}/api/jobs", token)
            return got.get("jobs", got) if isinstance(got, dict) else got

        def settled():
            js = jobs()
            return bool(js) and all(j["state"] in ("succeeded", "failed", "cancelled", "needs_input") for j in js)

        wait_for(lambda: http(f"{url}/api/jobs", token) is not None, "hangar's demo to start")
        wait_for(settled, "the seeded jobs to finish", 180)
        ticket = subprocess.run(python_for("hangar", d) + [str(demo), "ticket"], cwd=d, env=env, check=True,
                                capture_output=True, text=True).stdout
        job_id = json.loads(ticket.strip().splitlines()[-1])["job"]
        for title, text in MORE_JOBS:
            http(f"{url}/api/jobs", token, {"instructions": text, "title": title, "environment": "checkout-python",
                                           "repo": "https://github.com/acme/checkout-api.git", "deliver": "branch"})
        wait_for(settled, "the demo jobs to finish", 300)
        pr = (http(f"{url}/api/jobs/{job_id}", token).get("result") or {}).get("pr_url")
        if not pr:
            raise RuntimeError("the demo ticket did not end in a pull request")

        # the review loop: the job's change as an Airframe diff, and the composer to reply to the agent
        for name, view, theme in (("hangar-review", VIEW, "dark"), ("hangar-review-narrow", NARROW, "dark"),
                                   ("hangar-review-narrow-day", NARROW, "light")):
            page = br.page(f"localStorage.setItem('hangar.token', '{token}'); localStorage.setItem('hangar.theme', '{theme}')",
                           viewport=view, scheme=theme)
            page.goto(f"{url}/#jobs", wait_until="networkidle")
            page.locator("#job-list li", has_text="#42").first.click()
            page.wait_for_selector("#job-detail .af-composer", timeout=15000)
            page.locator("#job-detail [data-diff-show]").first.click()
            page.wait_for_selector("#job-detail .af-diff__hunk", timeout=15000)
            # scroll so the agent's summary, the composer and the first hunk share the window
            page.evaluate("""() => { const head = [...document.querySelectorAll('#job-detail h4')].find(e => /agent.s summary/i.test(e.textContent));
                (head || document.querySelector('#job-detail .af-composer')).scrollIntoView({block: 'start'}); window.scrollBy(0, -72); }""")
            page.wait_for_timeout(500)
            shoot(page, name)
            page.context.close()
        # Needs you and the Fleet: the afternoon from hangar's fixture, over this console, in Night and Day. The fixture
        # wires Playwright's async API, so it runs on its own thread with its own Playwright.
        err: list[BaseException] = []
        t = threading.Thread(target=lambda: _run(err, hangar_fixture(d, url, token)))
        t.start()
        t.join()
        if err:
            raise err[0]
        manifest["hangar"] = {"repo": "Sean-Koval/hangar", "commit": commit(d), "demo": "docs/assets/front/demo.py",
                              "fixture": "docs/assets/front/fixture.py",
                              "screens": {"hangar-needs-you": "Needs you (fixture): the decision deck, a held git push to main on top, then what stopped",
                                          "hangar-review": "Job #42's detail (demo): the agent's summary, the composer to reply, and the change as a greyscale diff",
                                          "hangar-fleet": "The Fleet (fixture): the headline, the decision deck with the held push, Needs you and Stopped beside it",
                                          "hangar-fleet-rows": "The Fleet in a 940 px window (fixture): the agents of base-codex as rows",
                                          "hangar-needs-you-narrow": "Needs you in a 720 px window (fixture): the decision deck with the held push on top",
                                          "hangar-review-narrow": "Job #42's detail in a 720 px window (demo): summary, composer and the diff",
                                          **{f"{n}-day": "The same screen in Day" for n in ("hangar-fleet", "hangar-needs-you", "hangar-needs-you-narrow",
                                                                              "hangar-fleet-rows", "hangar-review-narrow")}}}
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()
        log.close()


def _run(err: list, coro) -> None:
    import asyncio

    try:
        asyncio.run(coro)
    except BaseException as e:  # noqa: BLE001 - re-raised on the caller's thread
        err.append(e)


async def hangar_fixture(d: Path, url: str, token: str) -> None:
    """Needs you and the Fleet on hangar's fixture (docs/assets/front/fixture.py), as its own make.py shoots them."""
    from playwright.async_api import async_playwright

    sys.path.insert(0, str(d / "docs" / "assets" / "front"))
    from fixture import Fixture

    async def open_(b, theme: str, view: dict, hash_: str):
        ctx = await b.new_context(viewport=view, device_scale_factor=SCALE, color_scheme=theme)
        await ctx.add_init_script(f"localStorage.setItem('hangar.token', '{token}'); localStorage.setItem('hangar.theme', '{theme}')")
        page = await ctx.new_page()
        await Fixture().wire(page)
        await page.goto(f"{url}/#{hash_}", wait_until="networkidle")
        await page.wait_for_selector(".af-decision", timeout=15000)
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(900)
        return ctx, page

    async def save(page, name: str, clip: dict | None = None) -> None:
        await page.screenshot(path=str(OUT / f"{name}.png"), clip=clip)
        print("captures: wrote", OUT / f"{name}.png")
        cut(name)

    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for theme, suffix in (("dark", ""), ("light", "-day")):
            ctx, page = await open_(b, theme, VIEW, "needs")
            await save(page, f"hangar-needs-you{suffix}")
            await ctx.close()
            ctx, page = await open_(b, theme, NARROW, "needs")
            await save(page, f"hangar-needs-you-narrow{suffix}")
            await ctx.close()
            ctx, page = await open_(b, theme, VIEW, "fleet")
            await save(page, f"hangar-fleet{suffix}")
            await ctx.close()
        # the rows: the Fleet heading just under the sticky top bar
        for theme, suffix in (("dark", ""), ("light", "-day")):
            ctx, page = await open_(b, theme, MID, "fleet")
            await page.evaluate("""() => { const h = document.querySelector('#fleet-body').getBoundingClientRect().top;
                window.scrollBy(0, h - 64); }""")
            await page.wait_for_timeout(400)
            await save(page, f"hangar-fleet-rows{suffix}")
            await ctx.close()
        await b.close()


# -------------------------------------------------------------------------------------------------------- tower
TOWER_DEMO = """
import signal, sys
sys.path[:0] = ["tools", "."]
import ui_tour as t
port = int(sys.argv[1]); url = f"http://localhost:{port}"
p = t.start_demo(url, port)
signal.signal(signal.SIGTERM, lambda *a: (p.terminate(), sys.exit(0)))
t.seed(url)
print("ready", flush=True)
p.wait()
"""


def tower(br: Browser, manifest: dict) -> None:
    d = repo_dir("tower")
    server = d / "server"
    port = free_port()
    url = f"http://localhost:{port}"
    proc = subprocess.Popen(python_for("tower", d) + ["-c", TOWER_DEMO, str(port)], cwd=server,
                            stdout=subprocess.PIPE, stderr=open(OUT / ".tower-demo.log", "w"), text=True)
    try:
        wait_for(lambda: proc.stdout.readline().strip() == "ready", "Tower's demo to start and seed", 120, 0)
        for theme, suffix in (("dark", ""), ("light", "-day")):
            page = br.page(scheme=theme)
            page.goto(f"{url}/api/dev/as/{PEOPLE['marcus']}?theme={theme}", wait_until="load")
            page.wait_for_timeout(1200)
            for name, hash_ in (("tower-desk", "#needs"), ("tower-object", "#object/jira:issue/PAY-412")):
                if suffix and name not in DAY:
                    continue
                page.evaluate(f"location.hash = {json.dumps(hash_)}")
                page.wait_for_timeout(1000)
                shoot(page, name + suffix)
            page.context.close()
        manifest["tower"] = {"repo": "Sean-Koval/tower", "commit": commit(d), "demo": "server/tools/ui_tour.py",
                             "screens": {"tower-desk": "Marcus's Desk: Start work (the composer, handing a task to hangar), Needs you with an approval card, the agents he approves for",
                                         "tower-object": "The object page for Jira issue PAY-412: its chip, the composer about it, and the hangar release waiting for an approval",
                                         "tower-desk-day": "The same Desk in Day",
                                         "tower-object-day": "The same object page in Day"}}
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()


# --------------------------------------------------------------------------------------------------- flightdeck
def flightdeck(br: Browser, manifest: dict) -> None:
    d = repo_dir("flightdeck")
    for theme, suffix in (("dark", ""), ("light", "-day")):
        page_file = d / "docs" / "assets" / f"report-comment-full-{theme}.html"
        page = br.page(viewport={"width": 1200, "height": 900}, scheme=theme)
        page.goto(page_file.as_uri(), wait_until="networkidle")
        # the comment down to the outcome table, as flightdeck's own build.py crops it
        page.evaluate("""() => { const h = [...document.querySelectorAll('.md h3')].find(e => e.textContent.trim() === 'Process');
            if (h) { while (h.nextSibling) h.nextSibling.remove(); h.remove(); } }""")
        box = page.locator("div.page").first.bounding_box()
        shoot(page, "flightdeck-verdict" + suffix, clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": min(box["height"], 870)})
        page.context.close()
    manifest["flightdeck"] = {"repo": "Sean-Koval/flightdeck", "commit": commit(d), "demo": "docs/assets/build.py",
                              "screens": {"flightdeck-verdict": "The report on the harness pull request: the verdict, the pins of both variants and the outcome table, from the fixture experiment",
                                          "flightdeck-verdict-day": "The same report in GitHub's light theme"}}


# ----------------------------------------------------------------------------------------------------- airframe
THUMBS = ROOT / "docs" / "assets" / "airframe"          # one Night thumbnail per component, for the Components page
THUMB_VIEW = {"width": 800, "height": 500}


class _Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args) -> None:  # noqa: D102 - keep the capture log readable
        pass


def _serve(root: Path) -> tuple[ThreadingHTTPServer, str]:
    """Serve the gallery over http on a free local port: previews that import airframe.js are ES modules, which
    Chromium will not load from file://."""
    srv = ThreadingHTTPServer(("127.0.0.1", 0), partial(_Quiet, directory=str(root)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def airframe(br: Browser, manifest: dict) -> None:
    """The two deck captures at 1440x900 and 2x, then a 800x500 Night thumbnail of every component's preview."""
    tmp = Path(tempfile.mkdtemp(prefix="af-gallery-"))
    try:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "airframe.py"), "gallery", str(tmp)], check=True, capture_output=True)
        srv, base = _serve(tmp)
        for comp in ("ApprovalCard", "Diff"):
            page = br.page()
            page.goto(f"{base}/{comp}.html?theme=dark", wait_until="networkidle")
            page.wait_for_timeout(600)
            shoot(page, f"airframe-{comp.lower()}")
            page.context.close()
        THUMBS.mkdir(parents=True, exist_ok=True)
        names = sorted(p.stem for p in tmp.glob("*.html") if p.stem not in ("index", "Cover"))
        for comp in names:
            ctx = br.b.new_context(viewport=THUMB_VIEW, device_scale_factor=1, color_scheme="dark")
            page = ctx.new_page()
            page.goto(f"{base}/{comp}.html?theme=dark", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(400)
            page.add_style_tag(content=".afg-bar,.afg-spacer{display:none !important}")
            page.screenshot(path=str(THUMBS / f"{comp}.png"))
            print("captures: wrote", THUMBS / f"{comp}.png")
            ctx.close()
        srv.shutdown()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    manifest["airframe"] = {"repo": "Sean-Koval/agent-factory", "commit": commit(ROOT), "demo": "scripts/airframe.py gallery",
                            "screens": {"airframe-approvalcard": "The ApprovalCard preview from the gallery: inspect, deny with a reason, approve, quorum, waiting on others, verdicts",
                                        "airframe-diff": "The Diff preview from the gallery: a greyscale diff with one failed hunk and a comment thread"},
                            "thumbnails": f"docs/assets/airframe/<Name>.png: the top {THUMB_VIEW['width']}x{THUMB_VIEW['height']} of every "
                                          f"component's Night preview ({len(names)} components), shown on the Components page"}


def main(argv: list[str]) -> int:
    products = [a for a in argv if not a.startswith("-")] or list(PRODUCTS)
    bad = [p for p in products if p not in PRODUCTS]
    if bad:
        sys.exit(f"captures: unknown product {bad}; choose from {', '.join(PRODUCTS)}")
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_file = OUT / "captures.json"
    manifest = json.loads(manifest_file.read_text()) if manifest_file.exists() else {}
    if "--crops" in argv:
        for name in CROPS:
            cut(name)
    else:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as pw:
            br = Browser(pw)
            try:
                for p in products:
                    globals()[p](br, manifest)
            finally:
                br.close()
        manifest["captured"] = date.today().isoformat()
    manifest["crops"] = crops_manifest()
    manifest_file.write_text(json.dumps(dict(sorted(manifest.items())), indent=2) + "\n")
    print("captures: wrote", manifest_file)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
