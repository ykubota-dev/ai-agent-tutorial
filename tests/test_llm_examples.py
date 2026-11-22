"""LLMを利用する教材サンプルを、API通信なしで検証するテスト。"""
import runpy
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from langchain_core.messages import AIMessage

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


@contextmanager
def chapter_imports(chapter_dir: Path):
    """Chapter内のローカルimportを一時的に有効にする。"""
    sys.path.insert(0, str(chapter_dir))
    local_modules = {
        name: module
        for name, module in sys.modules.items()
        if name == "tools" or name.startswith(("tools.", "agents.", "state", "graph"))
    }
    for name in local_modules:
        sys.modules.pop(name, None)
    try:
        yield
    finally:
        sys.path.remove(str(chapter_dir))
        for name in list(sys.modules):
            if name == "tools" or name.startswith(("tools.", "agents.", "state", "graph")):
                sys.modules.pop(name, None)
        sys.modules.update(local_modules)


class LLMExampleTests(unittest.TestCase):
    def test_chapter03_prints_mocked_llm_response(self):
        chapter = EXAMPLES / "chapter03_llm"
        fake_llm = MagicMock()
        fake_llm.invoke.return_value = SimpleNamespace(content="モック回答")

        with patch("langchain_openai.ChatOpenAI", return_value=fake_llm), \
             patch("builtins.print") as mock_print:
            runpy.run_path(str(chapter / "main.py"), run_name="__main__")

        fake_llm.invoke.assert_called_once()
        mock_print.assert_any_call("モック回答")

    def test_chapter05_executes_selected_tool_and_returns_final_answer(self):
        chapter = EXAMPLES / "chapter05_tool_calling"
        first = AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "add",
                    "args": {"a": 10, "b": 20},
                    "id": "call_add",
                    "type": "tool_call",
                }
            ],
        )
        final = AIMessage(content="30です。")
        fake_bound_llm = MagicMock()
        fake_bound_llm.invoke.side_effect = [first, final]
        fake_llm = MagicMock()
        fake_llm.bind_tools.return_value = fake_bound_llm

        with chapter_imports(chapter), \
             patch("langchain_openai.ChatOpenAI", return_value=fake_llm), \
             patch("builtins.print") as mock_print:
            runpy.run_path(str(chapter / "main.py"), run_name="__main__")

        self.assertEqual(fake_bound_llm.invoke.call_count, 2)
        second_messages = fake_bound_llm.invoke.call_args_list[1].args[0]
        self.assertEqual(second_messages[-1].content, "30")
        mock_print.assert_any_call("30です。")

    def test_chapter06_uses_agent_result_without_real_llm(self):
        chapter = EXAMPLES / "chapter06_agent"
        fake_agent = MagicMock()
        fake_agent.invoke.return_value = {
            "messages": [AIMessage(content="90です。")]
        }

        with chapter_imports(chapter), \
             patch("langchain_openai.ChatOpenAI"), \
             patch("langchain.agents.create_agent", return_value=fake_agent), \
             patch("builtins.print") as mock_print:
            runpy.run_path(str(chapter / "main.py"), run_name="__main__")

        fake_agent.invoke.assert_called_once()
        mock_print.assert_any_call("90です。")

    def test_chapter09_orchestrator_returns_mocked_route(self):
        chapter = EXAMPLES / "chapter09_orchestrator"
        fake_router = MagicMock()
        fake_router.invoke.return_value = SimpleNamespace(route="research")
        fake_llm = MagicMock()
        fake_llm.with_structured_output.return_value = fake_router

        with chapter_imports(chapter), \
             patch("langchain_openai.ChatOpenAI", return_value=fake_llm):
            module = runpy.run_path(
                str(chapter / "agents" / "orchestrator.py"),
                run_name="chapter09_orchestrator_test",
            )
            result = module["orchestrator_agent"](
                {
                    "user_request": "東京から大阪への移動方法を調べてください。",
                    "research_result": "",
                    "calculation_result": "",
                    "final_answer": "",
                    "route": "",
                }
            )

        self.assertEqual(result, {"route": "research"})
        fake_router.invoke.assert_called_once()

    def test_chapter09_answer_agent_uses_mocked_response(self):
        chapter = EXAMPLES / "chapter09_orchestrator"
        fake_llm = MagicMock()
        fake_llm.invoke.return_value = SimpleNamespace(content="最終回答")

        with chapter_imports(chapter), \
             patch("langchain_openai.ChatOpenAI", return_value=fake_llm):
            module = runpy.run_path(
                str(chapter / "agents" / "answer.py"),
                run_name="chapter09_answer_test",
            )
            result = module["answer_agent"](
                {
                    "user_request": "依頼",
                    "research_result": "調査済み",
                    "calculation_result": "計算済み",
                    "final_answer": "",
                    "route": "answer",
                }
            )

        self.assertEqual(result, {"final_answer": "最終回答"})
        fake_llm.invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
