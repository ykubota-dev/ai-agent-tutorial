# Chapter 8: Multi Agent

## このChapterの目的

複数の役割を持つNodeをLangGraphで接続し、Stateで情報を共有する構成を学びます。

教材本文：[Chapter 8: Multi Agent構成を作る](../../docs/08_multi_agent.md)

## 学習する内容

- 役割ごとの処理分割
- Stateを使った情報共有
- 固定順序のMulti Agent構成

## ファイル

- `main.py`：Multi Agent構成を実行する
- `graph.py`：各Agent役のNodeを接続する
- `state.py`：Agent間で共有するStateを定義する
- `agents/`：役割ごとの処理を定義する

## 実行方法

リポジトリのルートディレクトリから実行します。

```bash
python examples/chapter08_multi_agent/main.py
```
