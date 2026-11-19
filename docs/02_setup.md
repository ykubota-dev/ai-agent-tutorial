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

## 3. GitHub Codespacesを利用する場合

ローカルPCにPythonなどをインストールせず、GitHub上に開発環境を作る方法もあります。

それが GitHub Codespaces です。

イメージとしては、

```text
自分のPC
    |
    | ブラウザ
    v
GitHub Codespaces
    |
    +-- VS Code
    +-- Python
    +-- Terminal
    +-- Git
```

という構成です。
ブラウザ上に、自分専用の開発環境を作ることができます。

## 3.1 Codespacesを起動する

GitHubで、この教材のリポジトリを開きます。

リポジトリ画面から、

```text
Code
↓
Codespaces
↓
Create codespace
```

を選択します。

Codespaceの作成が完了すると、ブラウザ上でVS Codeに似た画面が表示されます。
画面下部からTerminalを開きます。
Pythonが利用できるか確認しましょう。

> python --version

または、

> python3 --version

Pythonのバージョンが表示されれば準備完了です。

## 4. Pythonの仮想環境とは

ここから、Python開発で重要になる 仮想環境 を作ります。

Pythonでは、プロジェクトごとに使用するライブラリが異なります。

例えば、

```text
Project A
Python 3.x
LangChain
LangGraph

Project B
Python 3.x
FastAPI
SQLAlchemy
```

という2つのプロジェクトがあるとします。

すべてのライブラリをPC全体にインストールすると、プロジェクト間でライブラリのバージョンが競合することがあります。

そこで、プロジェクトごとにPython環境を分離します。

```text
PC / Codespace
│
├── Project A
│     └── .venv
│          ├── LangChain
│          └── LangGraph
│
└── Project B
      └── .venv
           ├── FastAPI
           └── SQLAlchemy
```

このプロジェクト専用のPython環境が仮想環境です。

## 4.1 なぜ仮想環境が必要なのか

例えばProject Aでは、

> あるライブラリ Version 1

を使っているとします。
一方、Project Bでは、

> あるライブラリ Version 2

が必要かもしれません。
仮想環境を分けておけば、

```text
Project A
└── Version 1

Project B
└── Version 2
```

のように、それぞれ独立して管理できます。

そのためPython開発では、
**プロジェクトを作ったら仮想環境を作る**
と覚えておきましょう。

## 5. 仮想環境を作成する

教材リポジトリのルートディレクトリへ移動します。
例えばリポジトリ名が、

> python-ai-agent-tutorial

の場合、このディレクトリで作業します。
現在いるディレクトリは、次のコマンドで確認できます。

> pwd

続いて、仮想環境を作成します。

> python -m venv .venv

環境によっては、

> python3 -m venv .venv

を使用します。
成功すると、プロジェクト内に.venvディレクトリが作成されます。

```text
python-ai-agent-tutorial/
│
├── .venv/
├── docs/
├── chapters/
├── README.md
└── requirements.txt
```

## 5.1 コマンドの意味

先ほど実行した、

> python -m venv .venv

を分解してみます。

**python**
Pythonを実行します。

**-m**
Pythonのモジュールを実行するオプションです。

**venv**
Python標準の仮想環境作成モジュールです。

**.venv**
作成する仮想環境のディレクトリ名です。

つまり、

> python -m venv .venv

は、
**Pythonのvenv機能を使って、.venvという名前の仮想環境を作成する**
という意味です。

## 6. 仮想環境を有効化する

仮想環境は、作成しただけではまだ利用されません。
作成した仮想環境を**有効化（activate）**します。

### 6.1 Windows

PowerShellの場合は、次のコマンドを実行します。

> .venv\Scripts\Activate.ps1

環境によっては、次の形式を利用する場合もあります。

> .venv\Scripts\activate

### 6.2 macOS / Linux / GitHub Codespaces

次のコマンドを実行します。

> source .venv/bin/activate

### 6.3 有効化できたか確認する

仮想環境が有効になると、Terminalの先頭などに、

> (.venv)

と表示されます。
例えば、

> (.venv) user@machine:~/python-ai-agent-tutorial$

のようになります。

これで、
**現在はこのプロジェクト専用のPython環境を使っている**
状態になりました。

## 7. pipとは

次に、AI Agent開発で使用するライブラリをインストールします。
Pythonでは、ライブラリのインストールに pip を利用します。

例えば、

> pip install langchain

とすると、LangChainをインストールできます。
イメージとしては、

```text
pip
 |
 | install
 v
Python Library
 |
 v
.venv
```

です。
仮想環境を有効にした状態でpip installすることで、ライブラリがその仮想環境にインストールされます。

## 8. 必要なライブラリをインストールする

この教材では、主に次のライブラリを使用します。

| ライブラリ | 用途 |
| --- | --- |
| langchain | LLM・Toolなどを扱う |
| langgraph | Agentの処理フローを構築する |
| langchain-openai | LangChainからOpenAIのモデルを利用する |
| python-dotenv | .envから環境変数を読み込む |

仮想環境が有効になっていることを確認して、次のコマンドを実行します。

> pip install langchain langgraph langchain-openai python-dotenv

インストールには少し時間がかかる場合があります。

## 9. requirements.txtを使う

実際の開発では、毎回、

> pip install langchain langgraph langchain-openai python-dotenv

と入力するのは不便です。
そこで、プロジェクトで必要なライブラリをrequirements.txtに記載します。

```text
langchain
langgraph
langchain-openai
python-dotenv
```

このファイルがあれば、

> pip install -r requirements.txt

だけで必要なライブラリをまとめてインストールできます。

### 9.1 requirements.txtはなぜ必要なのか

例えば、あなたが作ったAI Agentを別のエンジニアが動かすとします。
必要なライブラリが分からなければ、

> 何をインストールすれば動くの？

という状態になります。
requirements.txtがあれば、

> pip install -r requirements.txt

を実行することで、必要なライブラリをインストールできます。

つまり、
**このPythonプロジェクトを動かすために必要なライブラリを共有する**
ためのファイルです。

## 10. インストールされたライブラリを確認する

現在の仮想環境にインストールされているライブラリは、次のコマンドで確認できます。

> pip list

一覧の中に、

```text
langchain
langgraph
langchain-openai
python-dotenv
```

などが表示されていればOKです。

## 11. 仮想環境を終了する

作業が終わったら、仮想環境を終了できます。

> deactivate

Terminalの、

> (.venv)

という表示が消えます。
再び開発するときは、仮想環境を有効化します。

- macOS / Linux / GitHub Codespacesの場合：

> source .venv/bin/activate

- Windowsの場合：

> .venv\Scripts\Activate.ps1

## 12. .venvはGitHubにアップロードしない

.venvにはインストールしたPythonライブラリなどが保存されています。
そのため、ファイルサイズが大きくなります。
また、他の開発者はrequirements.txtから自分の環境を作ることができます。
したがって、.venv自体をGitHubにアップロードする必要はありません。

.gitignoreに次の設定を追加します。

> .venv/

これによって、Gitの管理対象から.venvを除外できます。


## 13. 開発環境を確認する

ここまでできたら、最後に環境を確認しましょう。

**Python**
```text
python --version
```

**仮想環境**

Terminalに、
```text
(.venv)
```
が表示されていることを確認します。

**pip**

```text
pip --version
```

**インストール済みライブラリ**
```text
pip list
```

すべて確認できれば、AI Agent開発環境の準備は完了です。


## 14. 今回作った環境

ここまでの作業を整理すると、次のようになります。

```text
VS Code / GitHub Codespaces
        |
        v
      Python
        |
        v
      .venv
        |
        +-- langchain
        +-- langgraph
        +-- langchain-openai
        +-- python-dotenv
```

プロジェクト側は次のような状態になっています。

```text
python-ai-agent-tutorial/
│
├── .venv/
├── docs/
├── chapters/
├── .gitignore
├── .env.example
├── README.md
└── requirements.txt
```

これでPythonからAI Agentを作る準備が整いました。



## 15. よくあるエラー

> python: command not found

Pythonがインストールされていない、またはpythonというコマンド名で登録されていない可能性があります。
次を試してください。

```text
python3 --version
```

それでも実行できない場合は、Pythonのインストール状況を確認してください。

```text
No module named venv
```

Pythonのvenvモジュールが利用できない環境です。
特に一部のLinux環境では、別途venv関連パッケージが必要になる場合があります。

利用しているPython環境を確認してください。

```text
ModuleNotFoundError
```

例えば、

```text
ModuleNotFoundError: No module named 'langchain'
```

と表示された場合、主に次の2点を確認します。

- 仮想環境が有効になっているか
- 必要なライブラリがインストールされているか

まず、

```text
pip list
```

で確認しましょう。

### 仮想環境を作ったのにライブラリが見つからない

VS Codeが別のPython Interpreterを利用している可能性があります。
VS CodeでPython Interpreterを選択するときは、今回作成した.venv内のPythonを選択します。

イメージとしては、

```text
VS Code
  |
  v
Python Interpreter
  |
  v
.venv
```

となっている必要があります。

## 16. まとめ

このChapterでは、AI AgentをPythonで開発するための環境を構築しました。

今回学んだ重要なポイントは3つです。

### 1. VS Code / GitHub Codespaces

Pythonコードを書くための開発環境です。

### 2. Python仮想環境

プロジェクトごとにPythonとライブラリの環境を分離します。
```text
python -m venv .venv
```
作成した仮想環境は、有効化してから使用します。

### 3. Pythonライブラリ

pipを利用して必要なライブラリをインストールします。
```text
pip install -r requirements.txt
```
今回準備した環境は、今後のChapterでも継続して使用します。


## 次のChapter

次のChapterから、いよいよPythonコードを書き始めます。

### Chapter 3：PythonからLLMを呼び出してみよう

最初の目標は非常にシンプルです。

```
Python
  |
  v
LangChain
  |
  v
LLM
  |
  v
Response
```

PythonプログラムからLLMへ質問を送り、回答を取得するところまで実装します。