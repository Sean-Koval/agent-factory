#!/usr/bin/env python3
"""Capture the products as they are now, from their own demos, for the deck and the docs.

    python3 scripts/captures.py                      # every product; sibling checkouts ../hangar, ../tower, ../flightdeck
    python3 scripts/captures.py hangar tower         # some of them
    HANGAR_DIR=… TOWER_DIR=… FLIGHTDECK_DIR=… python3 scripts/captures.py

Writes docs/assets/captures/<product>-<screen>.png (a 1440x900 window, Night, at 2x) and captures.json: what each
one shows, the repository and commit it came from, and when. deck/src.html and the docs pages reference them;
nothing here is drawn or retouched by hand, so a capture is regenerated, never edited.

A full window shown 600 px wide puts the product's text at 3-4 px, so each screen also has named crops (CROPS): the
subject of the screen, cut from the full capture by the same script, as <product>-<screen>-<crop>.png. A page or a
slide shows the crop; the full capture stays behind a link.

    python3 scripts/captures.py --crops              # re-cut the crops from the captures already here (no demos)

Every product is captured from its own demo and fixture data through its real UI, never from a stub:

- hangar: docs/assets/front/demo.py (the real control plane on the fake provider, a scripted agent and a stand-in
  GitHub) on its own port, the demo ticket (issue #42 becomes a job, a sandbox run and draft PR #43) and a few more
  jobs so the fleet has something on it. Screens: Needs you; the job's change and composer; the Fleet.
- Tower: server/tools/ui_tour.py (the offline demo and its stand-ins, with the tour's seed), as Marcus, an approver.
  Screens: the Desk; an object page with its chips, composer and card.
- flightdeck: docs/assets/report-comment.html, rendered by docs/assets/build.py from the fixture experiment: the
  verdict as the pull-request comment.
- Airframe: this repository's gallery previews (ApprovalCard, Diff), built by scripts/airframe.py gallery.

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
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "captures"
VIEW = {"width": 1440, "height": 900}
PRODUCTS = ("hangar", "tower", "flightdeck", "airframe")
PEOPLE = {"marcus": 102}  # Tower's demo: Marcus Chen, an approver
SCALE = 2  # device_scale_factor of every capture

# Named crops, in the window's CSS pixels (x, y, width, height), with what the crop shows. The box frames the one
# thing the page or slide is about, wide enough that a 600 px rendering keeps the product's text at 9 px or more.
CROPS = {
    "hangar-fleet": {
        "needs-you": ((72, 196, 1296, 428), "The checkout-python pool: ten tiles, the one that needs a person selected, and its question beside them"),
    },
    "hangar-needs-you": {
        "question": ((72, 176, 1296, 420), "Needs you: an agent's question with the answer box, and draft PR #43 waiting for review"),
    },
    "hangar-review": {
        "change": ((480, 60, 880, 600), "Job #42: the agent's summary, the reply box, and the change as a greyscale diff"),
    },
    "tower-desk": {
        "approval": ((264, 428, 680, 472), "Needs you on Marcus's Desk: an approval card with what will run and what signing does"),
    },
    "tower-object": {
        "release": ((264, 528, 680, 372), "On PAY-412: hangar's job waiting for a maintainer to release it, with the repo and the issue it names"),
    },
    "flightdeck-verdict": {
        "verdict": ((0, 0, 936, 560), "The report comment on the harness PR: the verdict line and the pins of both variants"),
    },
    "airframe-approvalcard": {
        "card": ((16, 12, 780, 584), "One ApprovalCard: a held push to main with its policy, checks, expiry, deny and approve, and the quorum"),
    },
}

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

    def page(self, init: str | None = None, viewport: dict | None = None):
        ctx = self.b.new_context(viewport=viewport or VIEW, device_scale_factor=2, color_scheme="dark")
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
        for crop, ((x, y, w, h), _) in CROPS[name].items():
            box = (x * SCALE, y * SCALE, min((x + w) * SCALE, img.width), min((y + h) * SCALE, img.height))
            out = OUT / f"{name}-{crop}.png"
            img.crop(box).save(out, optimize=True)
            print("captures: wrote", out)
            written.append(out.name)
    return written


def crops_manifest() -> dict:
    return {f"{name}-{crop}": {"from": name, "box": list(box), "shows": shows}
            for name, crops in CROPS.items() for crop, (box, shows) in crops.items()}


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

        page = br.page(f"localStorage.setItem('hangar.token', '{token}')")
        # Needs you: the agent's question and the PR waiting for review
        page.goto(f"{url}/#needs", wait_until="networkidle")
        page.wait_for_selector("#needs-list .af-question, #needs-list .af-approval, #needs-list li", timeout=15000)
        page.wait_for_timeout(800)
        bottom = page.evaluate("document.querySelector('#needs-list').getBoundingClientRect().bottom")
        shoot(page, "hangar-needs-you", clip={"x": 0, "y": 0, "width": VIEW["width"], "height": min(VIEW["height"], int(bottom) + 48)})
        # the review loop: the job's change as an Airframe diff, and the composer to reply to the agent
        page.goto(f"{url}/#jobs", wait_until="networkidle")
        page.locator("#job-list li", has_text="#42").first.click()
        page.wait_for_selector("#job-detail .af-composer", timeout=15000)
        page.locator("#job-detail summary, #job-detail button", has_text="Show the change").first.click()
        page.wait_for_selector("#job-detail .af-diff__hunk", timeout=15000)
        # scroll so the agent's summary, the composer and the first hunk share the window
        page.evaluate("""() => { const head = [...document.querySelectorAll('#job-detail h4')].find(e => /agent.s summary/i.test(e.textContent));
            (head || document.querySelector('#job-detail .af-composer')).scrollIntoView({block: 'start'}); window.scrollBy(0, -72); }""")
        page.wait_for_timeout(500)
        shoot(page, "hangar-review")
        # the Fleet: the board with the sandbox that needs a person selected, its detail beside it
        page.goto(f"{url}/#fleet", wait_until="networkidle")
        page.wait_for_selector("[data-tile]", timeout=15000)
        page.locator("[data-tile]").first.click()
        page.wait_for_timeout(900)
        shoot(page, "hangar-fleet")
        page.context.close()
        manifest["hangar"] = {"repo": "Sean-Koval/hangar", "commit": commit(d), "demo": "docs/assets/front/demo.py",
                              "screens": {"hangar-needs-you": "Needs you: a question from an agent (job on the demo's scripted agent) and draft PR #43 waiting for review",
                                          "hangar-review": "Job #42's detail: the agent's summary, the composer to reply, and the change as a greyscale diff",
                                          "hangar-fleet": "The Fleet board for the checkout-python pool with the sandbox that needs a person selected"}}
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()
        log.close()


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
        page = br.page()
        page.goto(f"{url}/api/dev/as/{PEOPLE['marcus']}?theme=dark", wait_until="load")
        page.wait_for_timeout(1200)
        for name, hash_ in (("tower-desk", "#needs"), ("tower-object", "#object/jira:issue/PAY-412")):
            page.evaluate(f"location.hash = {json.dumps(hash_)}")
            page.wait_for_timeout(1000)
            shoot(page, name)
        page.context.close()
        manifest["tower"] = {"repo": "Sean-Koval/tower", "commit": commit(d), "demo": "server/tools/ui_tour.py",
                             "screens": {"tower-desk": "Marcus's Desk: Start work (the composer, handing a task to hangar), Needs you with an approval card, the agents he signs for",
                                         "tower-object": "The object page for Jira issue PAY-412: its chip, the composer about it, and the hangar release waiting for a signature"}}
    finally:
        proc.terminate()
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()


# --------------------------------------------------------------------------------------------------- flightdeck
def flightdeck(br: Browser, manifest: dict) -> None:
    d = repo_dir("flightdeck")
    page_file = d / "docs" / "assets" / "report-comment.html"
    page = br.page(viewport={"width": 1200, "height": 900})
    page.goto(page_file.as_uri(), wait_until="networkidle")
    # the comment down to the outcome table, as flightdeck's own build.py crops it
    page.evaluate("""() => { const h = [...document.querySelectorAll('.md h3')].find(e => e.textContent === 'Process');
        if (h) { while (h.nextSibling) h.nextSibling.remove(); h.remove(); } }""")
    box = page.locator("div.page").first.bounding_box()
    shoot(page, "flightdeck-verdict", clip={"x": box["x"], "y": box["y"], "width": box["width"], "height": min(box["height"], 870)})
    page.context.close()
    manifest["flightdeck"] = {"repo": "Sean-Koval/flightdeck", "commit": commit(d), "demo": "docs/assets/build.py",
                              "screens": {"flightdeck-verdict": "The report on the harness pull request: the verdict, the pins of both variants and the outcome table, from the fixture experiment"}}


# ----------------------------------------------------------------------------------------------------- airframe
def airframe(br: Browser, manifest: dict) -> None:
    tmp = Path(tempfile.mkdtemp(prefix="af-gallery-"))
    try:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "airframe.py"), "gallery", str(tmp)], check=True, capture_output=True)
        for comp in ("ApprovalCard", "Diff"):
            page = br.page()
            page.goto((tmp / f"{comp}.html").as_uri() + "?theme=dark", wait_until="networkidle")
            page.wait_for_timeout(600)
            shoot(page, f"airframe-{comp.lower()}")
            page.context.close()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    manifest["airframe"] = {"repo": "Sean-Koval/agent-factory", "commit": commit(ROOT), "demo": "scripts/airframe.py gallery",
                            "screens": {"airframe-approvalcard": "The ApprovalCard preview from the gallery: inspect, deny with a reason, approve, quorum, waiting on others, verdicts",
                                        "airframe-diff": "The Diff preview from the gallery: a greyscale diff with one failed hunk and a comment thread"}}


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
