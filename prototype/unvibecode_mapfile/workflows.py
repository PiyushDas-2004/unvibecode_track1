"""Read UnvibeCode's Business Workflow Map and turn it into a line-free workflow index.

Input: the `business-workflows.html` page UnvibeCode writes into its results folder
(report-support/business-workflows.html, same layout as the published samples under
FinanceFlash/unvibecode/docs/gitdocs/*/2026-10-18/). Only the visible report is parsed:
workflow title, workflow area, and each "Implementation references" item (symbol, file).

Line numbers are dropped on purpose: the index must survive later commits that shift lines,
and the LLM stage that produces it is refreshed rarely (it is costly and, per upstream
issues #408/#516, not deterministic), while the index is looked up on every change.
"""
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser

_LOCATION = re.compile(r"^(?P<file>.+?)\s+·\s+lines?\s+(?P<start>\d+)\s*[–-]\s*(?P<end>\d+)\s*$")


@dataclass
class Workflow:
    title: str
    area: str
    refs: dict = field(default_factory=dict)   # file -> sorted tuple of symbols ("Class.method")


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.workflows, self.area, self.current = [], "", None
        self.stack, self.capture, self.buffer, self.pending_symbol = [], None, "", None
        self.in_item = False

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "") or ""
        self.stack.append(cls)
        if tag == "h2" and "workflow-group" in " ".join(self.stack):
            self.capture, self.buffer = "area", ""
        elif tag == "article" and "workflow-card" in cls:
            self.current = Workflow(title="", area=self.area)
            self.workflows.append(self.current)
        elif tag == "h3" and "workflow-title" in cls:
            self.capture, self.buffer = "title", ""
        elif tag == "li":
            self.in_item = "implementation-item" in cls
        elif tag == "strong" and self.in_item:
            self.capture, self.buffer = "symbol", ""
        elif tag == "span" and "implementation-location" in cls:
            self.capture, self.buffer = "location", ""

    def handle_endtag(self, tag):
        if self.capture and tag in {"h2", "h3", "strong", "span"}:
            text = re.sub(r"\s+", " ", self.buffer).strip()
            if self.capture == "area":
                self.area = text
            elif self.capture == "title" and self.current:
                self.current.title = text
            elif self.capture == "symbol":
                self.pending_symbol = text.rstrip("()").strip()
            elif self.capture == "location" and self.current and (m := _LOCATION.match(text)):
                refs = self.current.refs.setdefault(m.group("file"), set())
                if self.pending_symbol:
                    refs.add(self.pending_symbol)
                self.pending_symbol = None
            self.capture = None
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.capture:
            self.buffer += data


def parse_workflow_html(text):
    parser = _Parser()
    parser.feed(text)
    result = []
    for wf in parser.workflows:
        if wf.title and wf.refs:
            wf.refs = {f: tuple(sorted(s)) for f, s in sorted(wf.refs.items())}
            result.append(wf)
    return result


# ---- matching a change to workflows ------------------------------------------
def touched_workflows(workflows, files, names_by_file):
    """[(workflow, [(file, matched symbols)], strength)]: strength is 'symbol' when a referenced
    definition changed, 'file' when the change only shares a file with the workflow."""
    from .changes import matches
    hits = []
    for wf in workflows:
        found, strength = [], "file"
        for f in files:
            if f not in wf.refs:
                continue
            symbols = [s for s in wf.refs[f] if matches(s, names_by_file.get(f, set()))]
            if symbols:
                strength = "symbol"
            found.append((f, symbols))
        if found:
            hits.append((wf, found, strength))
    hits.sort(key=lambda h: (h[2] != "symbol", h[0].title))
    return hits
