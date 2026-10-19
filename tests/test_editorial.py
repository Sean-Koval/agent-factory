"""The editorial rule in AGENTS.md: paragraphs of at most 60 words, sentences of at most 25, pages of at most 700.

Run: python3 -m unittest discover -s tests. Measured on the Markdown in docs/ (and README.md) with front matter,
code blocks, HTML tags, tables, headings and link targets removed; a page over 700 words is split or allowlisted
below with the reason.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PARAGRAPH, SENTENCE, PAGE = 60, 25, 700

# Pages allowed over 700 words, each with its reason. Add here only when splitting would hurt the reader.
LONG_PAGES = {
    "glossary.md": "one entry per term; a reader looks one up, nobody reads it top to bottom",
    "work/index.md": "the company runbook: four repos, a change set and what stays yours, read once by a platform engineer",
}
# Writing that is not prose: a heading, a snippet include, a tag on its own line, an image, a line of buttons.
SKIP_LINE = re.compile(r"^\s*(#|--8<--|<[a-z/!]|!\[|\[.*\]\(.*\)\s*$|:)")
TABLE_RULE = re.compile(r"^\s*\|?\s*:?-{3,}")


def pages() -> list[Path]:
    out = [ROOT / "README.md"]
    for p in sorted(DOCS.rglob("*.md")):
        if any(part in ("theme", "deck", "gallery", "r", "components", "guide") for part in p.relative_to(DOCS).parts[:-1]):
            continue  # generated or vendored
        out.append(p)
    return out


def prose(text: str) -> tuple[list[str], str]:
    """Return the paragraphs of a page as plain prose, and the whole page's prose for the word count."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)  # front matter
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # code blocks
    text = re.sub(r"<style>.*?</style>", "", text, flags=re.S)
    text = re.sub(r"<figure.*?</figure>", "", text, flags=re.S)
    paragraphs = []
    for block in re.split(r"\n\s*\n", text):
        lines = [ln for ln in block.splitlines() if ln.strip() and not SKIP_LINE.match(ln)]
        if not lines:
            continue
        for line in lines:
            if TABLE_RULE.match(line):
                continue
            if line.lstrip().startswith("|"):  # a table: every cell is read on its own
                paragraphs.extend(plain(c) for c in line.strip().strip("|").split("|") if plain(c))
                continue
            # a list item is a paragraph of its own; a wrapped paragraph is one
            item = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", line)
            paragraphs.append(plain(item))
    return paragraphs, " ".join(paragraphs)


def plain(md: str) -> str:
    md = re.sub(r"<[^>]+>", "", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)  # link text only
    md = re.sub(r"`[^`]*`", "code", md)  # a code span is one word
    md = re.sub(r"[*_]{1,2}", "", md)
    md = re.sub(r"\{\s*\.[^}]*\}", "", md)  # attr_list
    md = md.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("\\|", "|")
    return md.strip()


def sentences(paragraph: str) -> list[str]:
    # split on . ! ? followed by space and a capital, a quote or a product name; a semicolon ends an
    # independent clause, so it counts as a sentence end too. "e.g." and version numbers do not split.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Za-z\"'(])|;\s+", paragraph)
    return [p for p in parts if p.strip()]


def words(s: str) -> int:
    return len(s.split())


class EditorialTests(unittest.TestCase):
    def test_paragraphs_and_sentences_are_short(self):
        failures = []
        for page in pages():
            paragraphs, _ = prose(page.read_text())
            for para in paragraphs:
                if words(para) > PARAGRAPH:
                    failures.append(f"{page.relative_to(ROOT)}: paragraph of {words(para)} words: {para[:70]}…")
                for sent in sentences(para):
                    if words(sent) > SENTENCE:
                        failures.append(f"{page.relative_to(ROOT)}: sentence of {words(sent)} words: {sent[:70]}…")
        self.assertEqual(failures, [], "\n" + "\n".join(failures))

    def test_pages_are_short_or_allowlisted(self):
        failures = []
        for page in pages():
            _, text = prose(page.read_text())
            rel = str(page.relative_to(DOCS)) if page.is_relative_to(DOCS) else page.name
            if words(text) > PAGE and rel not in LONG_PAGES:
                failures.append(f"{rel}: {words(text)} words; split it or allowlist it with a reason in tests/test_editorial.py")
            if rel in LONG_PAGES and words(text) <= PAGE:
                failures.append(f"{rel}: {words(text)} words; it no longer needs the allowlist entry")
        self.assertEqual(failures, [], "\n" + "\n".join(failures))

    def test_the_rule_is_written_down(self):
        agents = (ROOT / "AGENTS.md").read_text()
        for phrase in ("60 words", "25 words", "700 words"):
            self.assertIn(phrase, agents, "AGENTS.md states the editorial rule the test enforces")


if __name__ == "__main__":  # report the numbers for every page, and what breaks the rule
    for page in pages():
        paragraphs, text = prose(page.read_text())
        longest = max((words(p) for p in paragraphs), default=0)
        long_s = [s for p in paragraphs for s in sentences(p) if words(s) > SENTENCE]
        print(f"{str(page.relative_to(ROOT)):40} words={words(text):5} longest_para={longest:3} long_sentences={len(long_s)}")
        for p in paragraphs:
            if words(p) > PARAGRAPH:
                print(f"    P{words(p)}: {p[:100]}")
        for s in long_s:
            print(f"    S{words(s)}: {s[:100]}")
