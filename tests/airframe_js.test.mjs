// Smoke tests for airframe/js/airframe.js under node --test (no DOM: the string helpers and the contract they keep).
// Run by tests/test_airframe_js.py when node is installed: node --test tests/airframe_js.test.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import af, { status, icon, meta, btn, avatar, obj, tag, esc, inhibited, config } from "../airframe/js/airframe.js";

test("escapes everything it is given", () => {
  assert.equal(esc(`<b>&"'`), "&lt;b&gt;&amp;&quot;&#39;");
  assert.ok(status("approval", "<script>").includes("&lt;script&gt;"));
  assert.ok(btn("<x>", { attrs: { "data-id": '"q"' } }).includes('data-id="&quot;q&quot;"'));
  assert.ok(obj({ key: "<k>", title: "<t>", state: "<s>" }).includes("&lt;k&gt;"));
});

test("status: six roles, mark + word, lit only when asked", () => {
  assert.equal(status("running"), '<span class="af-status af-status--running"><i class="af-status__mark"></i>Running</span>');
  assert.ok(status("queued", "Waiting on 2 others").includes("af-status--queued"));
  assert.ok(status("approval", "Needs input", { lit: true }).includes("af-status--lit"));
  assert.throws(() => status("green"), RangeError);
});

test("icon uses the sprite and is decorative unless labelled", () => {
  config.icons = "/airframe/airframe-icons.svg";
  assert.equal(icon("agent"), '<svg class="af-ic" aria-hidden="true"><use href="/airframe/airframe-icons.svg#af-agent"/></svg>');
  assert.ok(icon("check", { size: 14, label: "Passed" }).includes('role="img" aria-label="Passed"'));
});

test("meta is keyed data, with the three tones", () => {
  const m = meta([["policy", "require-approval-main-push", "approval"], ["model", "gpt-5.1"]]);
  assert.ok(m.startsWith('<span class="af-meta">'));
  assert.ok(m.includes('af-meta__item af-meta__item--approval'));
  assert.ok(m.includes('<span class="af-meta__key">model</span><span class="af-meta__val">gpt-5.1</span>'));
  assert.ok(meta({ env: "prod" }).includes("af-meta__key"));
});

test("btn composes the kinds, sizes, icon and the text variant", () => {
  assert.equal(btn("Approve push", { kind: "primary", sm: true }), '<button type="button" class="af-btn af-btn--primary af-btn--sm">Approve push</button>');
  assert.ok(btn("Deny", { kind: "danger" }).includes("af-btn--danger"));
  assert.ok(btn("Not now", { text: true }).includes("af-btn--text"));
  assert.ok(btn("", { kind: "ghost", icon: "close", attrs: { "aria-label": "Close" } }).includes("af-btn--icon"));
  assert.ok(btn("Start", { disabled: true }).includes(" disabled>"));
  assert.throws(() => btn("x", { kind: "success" }), RangeError);
});

test("avatar: the triad, the sizes, the agent glyph", () => {
  assert.ok(avatar("person", "SK", { size: 28, name: "Sean Koval" }).includes('class="af-avatar af-avatar--person af-avatar--28" title="Sean Koval"'));
  assert.ok(avatar("agent", null).includes("#af-agent"));
  assert.ok(avatar("firm", "GX", { pending: true }).includes("af-avatar--pending"));
  assert.throws(() => avatar("robot", "R2"), RangeError);
  assert.throws(() => avatar("person", "SK", { size: 32 }), RangeError);
});

test("obj: link, restricted (key only), approval mark, trust line", () => {
  const link = obj({ source: "pr", key: "acme/api#412", title: "Fix auth", state: "Open", href: "https://example.test/412", trust: { source: "GitHub", read: "2 min ago", by: "HGR-3MX9" } });
  assert.ok(link.startsWith('<a class="af-obj af-obj--link" href="https://example.test/412">'));
  assert.ok(link.includes('<span class="af-obj__key">acme/api#412</span>'));
  assert.ok(link.includes('role="tooltip"') && link.includes("af-meta__key\">read</span>"));
  const r = obj({ key: "TR-88231", title: "secret title", restricted: true, href: "https://example.test" });
  assert.ok(r.startsWith('<span class="af-obj af-obj--restricted"'));
  assert.ok(!r.includes("secret title") && r.includes("restricted") && r.includes("#af-lock"));
  assert.ok(obj({ key: "PAY-415", state: "Needs approval", approval: true }).includes("af-status--approval"));
  assert.throws(() => obj({ title: "no key" }), TypeError);
});

test("tag and the default export", () => {
  assert.equal(tag("cedar"), '<span class="af-tag">cedar</span>');
  for (const k of ["status", "icon", "meta", "btn", "avatar", "obj", "tag", "toast", "confirm", "drawer"]) assert.equal(typeof af[k], k === "drawer" ? "object" : "function");
});

test("without a document nothing is inhibited and the helpers do not touch the DOM", () => {
  assert.equal(typeof document, "undefined");
  assert.equal(inhibited(), false);
});
