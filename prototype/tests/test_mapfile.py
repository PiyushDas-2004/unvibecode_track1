"""Tests on real UnvibeCode 0.4.0 bundles from the 13 Nov 2026 trial (source text removed)."""
import unittest
from pathlib import Path

from unvibecode_mapfile.bundle import load_bundle
from unvibecode_mapfile.mapfile import delta, from_bundle, parse, render, suspicious

FIX = Path(__file__).resolve().parent.parent / "fixtures"


def build(name):
    return from_bundle(load_bundle(FIX / f"{name}.zip"))


class RenderAndParse(unittest.TestCase):
    def test_render_is_deterministic(self):
        self.assertEqual(render(build("flask_49943b5a")), render(build("flask_49943b5a")))

    def test_parse_round_trip_keeps_every_connection(self):
        m = build("flask_49943b5a")
        back = parse(render(m))
        self.assertEqual(back.edges, m.edges)
        self.assertEqual(back.source_files, 102)
        self.assertEqual(render(back).split("## Connections")[1], render(m).split("## Connections")[1])

    def test_no_timestamps_or_job_ids_in_file(self):
        text = render(build("flask_49943b5a"))
        self.assertNotRegex(text, r"20\d\d-\d\d-\d\d|[0-9a-f]{32}")

    def test_known_correct_connection_present(self):
        m = build("flask_49943b5a")
        self.assertIn("get_debug_flag", m.edges[("src/flask/cli.py", "src/flask/helpers.py")])


class StabilityAcrossCommits(unittest.TestCase):
    """Chunk ids move with line numbers; the map must not."""

    def test_non_structural_commits_render_identically(self):
        # 3596b1ab -> d73fa1cd: 6 files, +19/-7 lines, 97 chunk ids changed.
        a, b = build("flask_3596b1ab"), build("flask_d73fa1cd")
        self.assertEqual(delta(a, b), ([], []))
        self.assertEqual(render(a).split("-->", 1)[1], render(b).split("-->", 1)[1])

    def test_head_matches_d73fa1cd_structurally(self):
        self.assertEqual(delta(build("flask_d73fa1cd"), build("flask_49943b5a")), ([], []))

    def test_refactor_commit_delta_is_exact(self):
        # c2705ffd "merge app and request context" against its parent.
        added, removed = delta(build("flask_33012325_parent_of_c2705ff"), build("flask_c2705ffd"))
        self.assertEqual(added, [
            ("src/flask/helpers.py", "tests/conftest.py", "app_ctx"),
            ("tests/test_reqctx.py", "tests/conftest.py", "app_ctx"),
            ("tests/test_session_interface.py", "tests/conftest.py", "app_ctx"),
        ])
        self.assertEqual(removed, [
            ("src/flask/app.py", "src/flask/ctx.py", "RequestContext"),
            ("src/flask/app.py", "src/flask/sansio/scaffold.py", ""),
        ])


class SuspiciousConnections(unittest.TestCase):
    def test_flags_package_shadowing_fixture(self):
        texts = [t for k, t in suspicious(build("flask_49943b5a")) if k == "shadowing"]
        self.assertTrue(any("tests/test_apps/cliapp/inner1/inner2/flask.py" in t and t.startswith("43 files")
                            for t in texts), texts)

    def test_flags_wrong_new_edge_from_refactor(self):
        texts = [t for _, t in suspicious(build("flask_c2705ffd"))]
        self.assertTrue(any("`src/flask/helpers.py` → `tests/conftest.py`" in t for t in texts))

    def test_test_to_test_edges_are_not_flagged(self):
        texts = [t for _, t in suspicious(build("flask_c2705ffd"))]
        self.assertFalse(any(t.startswith("`tests/test_reqctx.py`") for t in texts))


class Coverage(unittest.TestCase):
    def test_typescript_repo_is_marked_sparse(self):
        m = build("realworld_30b68e1e")
        text = render(m)
        self.assertEqual(len(m.edges), 2)
        self.assertGreaterEqual(m.unresolved_relative_imports, 40)
        self.assertIn("**Sparse map:**", text)

    def test_go_multiservice_repo_builds(self):
        m = build("microservices_c7cb6d5b")
        self.assertIn(("src/frontend/handlers.go", "src/frontend/rpc.go"), m.edges)


if __name__ == "__main__":
    unittest.main()
