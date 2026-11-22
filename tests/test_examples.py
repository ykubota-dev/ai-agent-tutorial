"""教材サンプルの構文・参照・ローカル実行を検証するテスト。API通信は行わない。"""
import ast
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
DOCS = ROOT / "docs"


class ExampleTests(unittest.TestCase):
    def test_all_python_examples_compile(self):
        files = sorted(EXAMPLES.rglob("*.py"))
        self.assertGreater(len(files), 0)
        for path in files:
            with self.subTest(path=str(path.relative_to(ROOT))):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_all_chapters_have_entrypoint(self):
        for chapter in range(3, 10):
            matches = list(EXAMPLES.glob(f"chapter{chapter:02d}_*/main.py"))
            self.assertEqual(len(matches), 1, f"Chapter {chapter} のmain.pyが必要です")

    def test_documentation_references_existing_examples(self):
        for path in [ROOT / "README.md", *DOCS.glob("*.md")]:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("chapters/", content)

    def test_model_names_match(self):
        expected = 'gpt-5.5'
        for path in [*DOCS.glob("*.md"), *EXAMPLES.rglob("*.py")]:
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertNotIn("gpt-4.1-mini", content)
                if 'ChatOpenAI(' in content:
                    self.assertIn(expected, content)

    def test_chapter04_tool_definitions_not_duplicated(self):
        path = EXAMPLES / "chapter04_tool" / "main.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        names = [node.name for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        self.assertEqual(len(names), len(set(names)))

    def test_chapter05_handles_multiple_tool_calls(self):
        path = EXAMPLES / "chapter05_tool_calling" / "main.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        self.assertTrue(any(isinstance(node, ast.For) for node in ast.walk(tree)))
        self.assertTrue(any(isinstance(node, ast.If) for node in ast.walk(tree)))

    def test_example_readmes_use_root_execution_and_link_docs(self):
        for chapter in range(3, 10):
            folder = next(EXAMPLES.glob(f"chapter{chapter:02d}_*"))
            readme = folder / "README.md"
            content = readme.read_text(encoding="utf-8")
            with self.subTest(chapter=chapter):
                expected_command = f"python {folder.relative_to(ROOT).as_posix()}/main.py"
                self.assertIn(expected_command, content)
                self.assertIn("../../docs/", content)

    def test_chapter07_uses_graph_state_name(self):
        state_path = EXAMPLES / "chapter07_langgraph" / "state.py"
        graph_path = EXAMPLES / "chapter07_langgraph" / "graph.py"
        self.assertIn("class GraphState", state_path.read_text(encoding="utf-8"))
        self.assertIn("GraphState", graph_path.read_text(encoding="utf-8"))
        self.assertNotIn("AgentState", state_path.read_text(encoding="utf-8"))

    def test_requirements_are_version_pinned(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        packages = [line for line in requirements if line and not line.startswith("#")]
        self.assertTrue(packages)
        for package in packages:
            with self.subTest(package=package):
                self.assertIn("==", package)

    def test_local_graph_examples(self):
        # Chapter 7/8はAPIキー不要。依存関係が未導入ならスキップする。
        try:
            import langgraph  # noqa: F401
        except ImportError:
            self.skipTest("langgraph未インストール")
        for chapter in (7, 8):
            folder = next(EXAMPLES.glob(f"chapter{chapter:02d}_*"))
            with self.subTest(chapter=chapter):
                result = subprocess.run(
                    [sys.executable, str((folder / "main.py").relative_to(ROOT))],
                    cwd=ROOT, capture_output=True, text=True, timeout=30,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.strip())


if __name__ == "__main__":
    unittest.main()
