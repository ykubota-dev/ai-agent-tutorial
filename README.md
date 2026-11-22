# PythonではじめるAI Agent開発

Python初心者が、AI Agentの基本概念を順番に学びながら、最終的に複数のAgentが協調する構成を作るハンズオン教材です。

## 対象読者

Python初心者〜初級者を対象としています。

## 前提知識

基本的なPC操作と、プログラミングの初歩的な考え方を想定しています。PythonやAI Agentの専門知識は必要ありません。

## 学習ロードマップ

1. [Chapter 1: AI Agentとは何か](docs/01_introduction.md)
2. [Chapter 2: VS Code / GitHub Codespacesのセットアップ](docs/02_setup.md)
3. [Chapter 3: PythonからLLMを呼び出す](docs/03_llm.md) ([コード](examples/chapter03_llm/README.md))
4. [Chapter 4: Toolを作る](docs/04_tool.md) ([コード](examples/chapter04_tool/README.md))
5. [Chapter 5: Tool Callingを理解する](docs/05_tool_calling.md) ([コード](examples/chapter05_tool_calling/README.md))
6. [Chapter 6: 単一Agentを作る](docs/06_agent.md) ([コード](examples/chapter06_agent/README.md))
7. [Chapter 7: LangGraphを使う](docs/07_langgraph.md) ([コード](examples/chapter07_langgraph/README.md))
8. [Chapter 8: Multi Agent構成を作る](docs/08_multi_agent.md) ([コード](examples/chapter08_multi_agent/README.md))
9. [Chapter 9: Orchestrator構成を作る](docs/09_orchestrator.md) ([コード](examples/chapter09_orchestrator/README.md))

学習は **LLM → Tool → Tool Calling → Agent → LangGraph → Multi Agent → Orchestrator** の順に進めます。ライブラリ固有APIの暗記ではなく、各段階で必要になる基本概念を理解することを重視します。

## 用語表

この教材では、次の用語を以下の意味で統一して使います。

| 用語 | この教材での意味 |
| --- | --- |
| LLM | 入力を受け取り、文章生成やTool選択などの判断を行うモデル |
| Tool | 計算・検索・API呼び出しなど、プログラムとして実行する機能 |
| Tool Calling | LLMが利用するToolと引数を選ぶ仕組み |
| Agent | LLMがTool等を利用しながら、目的達成まで判断と実行を進める仕組み |
| Single Agent | 1つのAgentが処理を担当する構成。本教材では「単一Agent」と表記 |
| Multi Agent | 複数のAgentまたはAgent役に責務を分けて協調する構成 |
| Orchestrator | 次にどのAgentへ仕事を任せるかを判断し、全体の処理を制御する役割 |
| State | LangGraph上でNode間に共有する処理中のデータ |
| Node | LangGraph上の1つの処理単位 |
| Edge | Nodeから次のNodeへ進む経路 |

「AI Agent」は教材全体を指す一般的な表現として使い、実装上の構成要素を説明するときは原則として「Agent」と表記します。

---

## 最終的に作成するAI Agent

```mermaid
flowchart TD
	User --> Orchestrator
	Orchestrator --> Research[Research Agent]
	Orchestrator --> Calculation[Calculation Agent]
	Orchestrator --> Answer[Answer Agent]
	Research -. Tool Calling .-> Search[Search Tool]
	Calculation -. Tool Calling .-> Calculator[Calculator Tool]
```

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Windowsでは仮想環境の有効化に `.venv\\Scripts\\activate` を使用してください。APIキーなどの値は `.env` に設定し、このファイルを共有・コミットしないでください。

## サンプルコードの実行

サンプルコードは、すべて**リポジトリのルートディレクトリから**実行します。例えばChapter 3は次のように実行します。

```bash
python examples/chapter03_llm/main.py
```

各 `examples/chapterXX_*` ディレクトリのREADMEにも同じ実行方法を記載しています。

## サンプルコードのテスト

リポジトリのルートで、次のコマンドを実行します。

```bash
python -m unittest discover -s tests -v
```

Chapter 3〜9のPython構文、Chapter 4のTool定義重複、Chapter 5の分岐・繰り返し構造、教材内の参照パスとモデル名を検証します。依存ライブラリがインストールされている場合、API通信を行わないChapter 7・8のサンプルも実行します。Chapter 3・5・6・9のLLM APIを使う実行テストは含まれません（APIキーと課金が必要なため）。
