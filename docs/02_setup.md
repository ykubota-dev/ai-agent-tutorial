# Chapter 2: Python開発環境のセットアップ

## この章で学ぶこと

- VS CodeまたはGitHub Codespacesの準備
- Python仮想環境の作成と有効化
- 必要なライブラリのインストール

Chapter 3から、実際にPythonコードを書いてLLMを呼び出します。
そのため、このChapterではコードを書くための開発環境を完成させることを目標にします。

### 1. 今回作る開発環境

この教材では、次のような環境でAI Agentを開発します。

```text
VS Code / GitHub Codespaces
        |
        v
      Python
        |
        v
   Python仮想環境
        |
        v
LangChain / LangGraph
        |
        v
      LLM API
```

それぞれの役割を簡単に整理すると、次のようになります。


| 技術 | 役割 |
| --- | --- |
| VS Code | プログラムを書くためのエディタ |
| GitHub Codespaces | ブラウザから利用できるクラウド開発環境 |
| Python | AI Agentを実装するプログラミング言語 |
| venv | プロジェクトごとにPython環境を分離する |
| pip | Pythonライブラリをインストールする |
| LangChain | LLMやToolを扱うためのライブラリ |
| LangGraph |Agentの処理フローを構築するライブラリ |

すべてを一度に理解する必要はありません。
このChapterでは、まずAI Agentを動かせる状態を作ることを優先します。

## 2. 開発環境を準備する

この教材では、次のどちらかを利用します。

- VS Code
- GitHub Codespaces

どちらを利用しても、Chapter 3以降の内容は基本的に同じです。

### 2.1 VS Codeを利用する場合

VS Code（Visual Studio Code）は、プログラムを書くためのエディタです。
Pythonだけでなく、Java、JavaScript、TypeScriptなど、さまざまな言語の開発で利用されています。

### 必要なもの

ローカルPCで開発する場合は、次の2つを準備します。

- VS Code
- Python

### Pythonがインストールされているか確認する

VS Codeを起動して、メニューからターミナルを開きます。

```text
ターミナル
↓
新しいターミナル
```

ターミナルで次のコマンドを実行します。

> python --version

環境によっては、次のコマンドを使用します。

> python3 --version

例えば、次のようにPythonのバージョンが表示されれば準備できています。

> Python 3.x.x

この教材では **Python 3.11以上** を推奨します。

### VS CodeのPython拡張機能

VS Codeでは、Python開発を便利にするためのPython拡張機能を利用できます。
VS Code左側の「Extensions」を開き、

> Python

と検索して、Microsoftが提供しているPython拡張機能をインストールします。

これによって、

- Pythonコードの補完
- エラー表示
- Python Interpreterの選択
- デバッグ

などが利用しやすくなります。