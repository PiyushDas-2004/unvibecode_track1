"""End-to-end tests of impact/check/diff on a throwaway git repository (no network)."""
import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from unvibecode_mapfile import cli
from unvibecode_mapfile.bundle import load_bundle
from unvibecode_mapfile.impact import IMPORT_LINE, reach
from unvibecode_mapfile.mapfile import from_bundle

FIX = Path(__file__).resolve().parent.parent / "fixtures"


def git(repo, *args):
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True,
                   env={**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"})


def write_bundle(folder, connections, files):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "manifest.json").write_text(json.dumps({"repository": "demo", "source_files": len(files)}))
    (folder / "connections.jsonl").write_text("\n".join(json.dumps(c) for c in connections) + "\n")
    (folder / "chunks.jsonl").write_text("\n".join(json.dumps({"file": f}) for f in files) + "\n")


def edge(src, dst, sym=None):
    return {"source_file": src, "target_file": dst, "symbol": sym, "confidence": "high"}


def run(*argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = cli.main(list(argv))
    return code, buf.getvalue()


class GitRepoCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        files = {"core.py": "def price(x):\n    return x\n\ndef tax(x):\n    return x\n",
                 "shop.py": "from core import price\n", "report.py": "from core import tax\n",
                 "billing.py": "from core import price, tax\n", "util.py": "X = 1\n"}
        for name, text in files.items():
            (self.repo / name).write_text(text)
        git(self.repo, "init", "-q"); git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "init")
        self.bundle = Path(self.tmp.name) / "bundle"
        write_bundle(self.bundle, [edge("shop.py", "core.py", "price"), edge("report.py", "core.py", "tax"),
                                   edge("billing.py", "core.py", "price"), edge("billing.py", "core.py", "tax")],
                     list(files))
        code, _ = run("build", "--repository", str(self.repo), "--bundle", str(self.bundle))
        self.assertEqual(code, 0)
        git(self.repo, "add", "UNVIBECODE.md"); git(self.repo, "commit", "-qm", "add map")

    def tearDown(self):
        self.tmp.cleanup()

    def test_impact_names_importers_of_changed_symbol(self):
        (self.repo / "core.py").write_text("def price(x):\n    return x * 2\n\ndef tax(x):\n    return x\n")
        code, out = run("impact", "--repository", str(self.repo))
        self.assertEqual(code, 0)
        self.assertIn("core.py: 3 direct importer(s)", out)
        self.assertIn("changed symbol price is used by billing.py, shop.py", out)
        self.assertNotIn("changed symbol tax", out)
        self.assertIn("No import lines changed", out)

    def test_impact_flags_import_change_and_markdown_footer(self):
        (self.repo / "util.py").write_text("from core import tax\nX = 1\n")
        code, out = run("impact", "--repository", str(self.repo), "--markdown")
        self.assertIn("**Import lines changed** in `util.py`", out)
        self.assertIn("No code was uploaded", out)

    def test_check_skips_upload_when_no_import_line_changed(self):
        (self.repo / "core.py").write_text("def price(x):\n    return x + 1\n\ndef tax(x):\n    return x\n")
        code, out = run("check", "--repository", str(self.repo), "--since", "HEAD")
        self.assertEqual(code, 0)
        self.assertIn("skipped the UnvibeCode upload", out)

    def test_check_reports_new_connection_and_strict_exit(self):
        newer = Path(self.tmp.name) / "bundle2"
        write_bundle(newer, [edge("shop.py", "core.py", "price"), edge("report.py", "core.py", "tax"),
                             edge("billing.py", "core.py", "price"), edge("billing.py", "core.py", "tax"),
                             edge("util.py", "core.py", "tax")], ["core.py", "shop.py", "report.py", "billing.py", "util.py"])
        code, out = run("check", "--repository", str(self.repo), "--bundle", str(newer))
        self.assertEqual(code, 0)                       # warn-only by default
        self.assertIn("+1 / -0", out)
        self.assertIn("`util.py` → `core.py` · tax", out)
        code, _ = run("check", "--repository", str(self.repo), "--bundle", str(newer), "--strict")
        self.assertEqual(code, 1)

    def test_diff_between_git_revisions(self):
        code, out = run("diff", "--repository", str(self.repo), "HEAD", "HEAD")
        self.assertIn("No structural change", out)

    def test_build_is_idempotent(self):
        code, out = run("build", "--repository", str(self.repo), "--bundle", str(self.bundle))
        self.assertIn("Unchanged", out)

    def test_usage_log_is_opt_in_and_local(self):
        log = Path(self.tmp.name) / "usage.jsonl"
        run("impact", "--repository", str(self.repo))
        self.assertFalse(log.exists())
        os.environ["UNVIBECODE_MAPFILE_USAGE_LOG"] = str(log)
        try:
            run("impact", "--repository", str(self.repo))
        finally:
            del os.environ["UNVIBECODE_MAPFILE_USAGE_LOG"]
        record = json.loads(log.read_text().splitlines()[0])
        self.assertEqual(record["event"], "impact")
        self.assertIn(record["trigger"], {"ci", "manual"})


class RealMapReach(unittest.TestCase):
    def test_hub_and_symbol_users_on_real_flask_map(self):
        m = from_bundle(load_bundle(FIX / "flask_49943b5a.zip"))
        [r] = reach(m, ["src/flask/helpers.py"], {"src/flask/helpers.py": [" def get_debug_flag() -> bool:", "    val = 1"]})
        self.assertTrue(r.hub)
        self.assertIn("src/flask/cli.py", r.touched_symbols["get_debug_flag"])


class GateIgnoresDocs(unittest.TestCase):
    def test_docs_with_code_samples_do_not_trigger_upload(self):
        from unvibecode_mapfile.impact import import_changes
        self.assertEqual(import_changes({"docs/quickstart.rst": ["from flask import Flask"],
                                         "src/app.py": ["from .ctx import AppContext"]}), ["src/app.py"])

    def test_mentions_are_not_definitions(self):
        m = from_bundle(load_bundle(FIX / "flask_49943b5a.zip"))
        [r] = reach(m, ["src/flask/helpers.py"], {"src/flask/helpers.py": ["    # see get_debug_flag for details"]})
        self.assertNotIn("get_debug_flag", r.touched_symbols)


class ImportLinePattern(unittest.TestCase):
    def test_languages(self):
        for line in ["from .app import Flask", "import os", "import { a } from './b'",
                     "const x = require('./y')", "use crate::foo;", '    "github.com/x/y"']:
            self.assertTrue(IMPORT_LINE.match(line), line)
        for line in ["return price * 2", "x = 1", "def importer():"]:
            self.assertFalse(IMPORT_LINE.match(line), line)


if __name__ == "__main__":
    unittest.main()


# ---- business workflows (pass 4) -------------------------------------------
from unvibecode_mapfile.changes import changed_definitions, diff_hunks, python_scopes, matches  # noqa: E402
from unvibecode_mapfile.mapfile import parse, render  # noqa: E402
from unvibecode_mapfile.workflows import Workflow, parse_workflow_html, touched_workflows  # noqa: E402


class BusinessWorkflowMap(unittest.TestCase):
    def setUp(self):
        self.wfs = parse_workflow_html((FIX / "django-payments_5607e9e_business-workflows.html").read_text())

    def test_parses_published_sample(self):
        self.assertEqual(len(self.wfs), 7)                      # the sample header says "7 workflows"
        stripe = next(w for w in self.wfs if w.title == "provider-backed payment checkout and callback handling")
        self.assertIn("StripeProviderV3.create_session", stripe.refs["payments/stripe/providers.py"])
        self.assertEqual(stripe.area, "Payment workflows")

    def test_workflows_round_trip_through_the_map_file(self):
        m = from_bundle(load_bundle(FIX / "django-payments_5607e9e.zip"))
        m.workflows = self.wfs
        back = parse(render(m))
        self.assertEqual([(w.title, w.area, w.refs) for w in back.workflows],
                         [(w.title, w.area, w.refs) for w in self.wfs])
        self.assertEqual(back.edges, m.edges)
        self.assertLess(render(m).index("## Business workflows"), render(m).index("## Most-imported files"))


class PythonScopes(unittest.TestCase):
    SRC = ("class Pay:\n    def save(self,\n             x=1,\n    ) -> None:\n        a = 1\n\n"
           "    def capture(self):\n        return 2\n\ndef helper():\n    pass\n")

    def test_qualified_names(self):
        sc = python_scopes(self.SRC)
        self.assertEqual((sc[3], sc[5], sc[8], sc[11]), ("Pay.save", "Pay.save", "Pay.capture", "helper"))

    def test_matches(self):
        self.assertTrue(matches("Pay", {"Pay.save"}))            # change inside a referenced class
        self.assertTrue(matches("Pay.capture()", {"Pay.capture"}))
        self.assertFalse(matches("Pay.capture", {"Pay.save"}))
        self.assertTrue(matches("get_form", {"get_form"}))         # non-Python fallback


class ChangeToWorkflow(unittest.TestCase):
    """Regression for the two errors found by hand on django-payments (d1eea51, ff5082a)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / "pay.py").write_text(
            "class Provider:\n    def get_form(self):\n        return 1\n\n"
            "    def create_session(self, p):\n        return 2\n\n"
            "class Payment:\n    def save(self):\n        tries = {}\n        return tries\n")
        git(self.repo, "init", "-q"); git(self.repo, "add", "."); git(self.repo, "commit", "-qm", "init")
        self.wf_checkout = Workflow("checkout", "Payment", {"pay.py": ("Provider.create_session", "Provider.get_form")})
        self.wf_form = Workflow("form only", "Payment", {"pay.py": ("Provider.get_form",)})
        self.wf_model = Workflow("model", "Payment", {"pay.py": ("Payment",)})

    def tearDown(self):
        self.tmp.cleanup()

    def names(self):
        return changed_definitions(self.repo, diff_hunks(self.repo, "HEAD"), "HEAD")

    def test_editing_a_def_line_is_not_blamed_on_the_previous_function(self):
        text = (self.repo / "pay.py").read_text().replace("def create_session(self, p):", "def create_session(self, p: int):")
        (self.repo / "pay.py").write_text(text)
        hits = touched_workflows([self.wf_checkout, self.wf_form], ["pay.py"], self.names())
        self.assertEqual([(w.title, f) for w, f, strength in hits if strength == "symbol"],
                         [("checkout", [("pay.py", ["Provider.create_session"])])])

    def test_change_inside_a_method_counts_for_its_class(self):
        (self.repo / "pay.py").write_text((self.repo / "pay.py").read_text().replace("tries = {}", "tries = set()"))
        hits = touched_workflows([self.wf_model, self.wf_form], ["pay.py"], self.names())
        self.assertEqual([(w.title, s) for w, f, s in hits], [("model", "symbol"), ("form only", "file")])


class KeepsWorkflowsWhenBusinessAnalysisIsDown(GitRepoCase):
    def test_build_without_workflow_page_keeps_previous_index(self):
        page = FIX / "django-payments_5607e9e_business-workflows.html"
        run("build", "--repository", str(self.repo), "--bundle", str(self.bundle), "--workflows", str(page))
        code, out = run("build", "--repository", str(self.repo), "--bundle", str(self.bundle))
        self.assertIn("kept 7 workflows", out)
        self.assertEqual(len(parse((self.repo / "UNVIBECODE.md").read_text()).workflows), 7)

    def test_unvibe_entry_point_and_oneline(self):
        code, out = run("impact", "--repository", str(self.repo), "--oneline")
        self.assertTrue(out.startswith("UnvibeCode · business map not available"))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(cli.unvibe(["--repository", str(self.repo)]), 0)
        self.assertIn("UnvibeCode business reach", buf.getvalue())
