# Chapter 9: Orchestrator

## このChapterの目的

Orchestratorが次に実行するAgentを判断する動的なMulti Agent構成を学びます。

教材本文：[Chapter 9: Orchestrator構成を作る](../../docs/09_orchestrator.md)

## 学習する内容

- Orchestratorによる振り分け
- Conditional Edgeによる動的分岐
- Toolを持つAgentの組み込み

## ファイル

- `main.py`：Orchestrator構成を実行する
- `graph.py`：Conditional Edgeを含むGraphを定義する
- `state.py`：処理状況とrouteを共有する
- `agents/`：Orchestratorと各Agentを定義する
- `tools/`：Agentが利用するToolを定義する

## 実行方法

リポジトリのルートディレクトリから実行します。

```bash
python examples/chapter09_orchestrator/main.py
```
