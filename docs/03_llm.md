# Chapter 3: PythonからLLMを呼び出す

## この章で学ぶこと

この章では、PythonプログラムからLLMを呼び出して、質問に対する回答を取得します。

この章を読み終えると、以下のことができるようになります。

- PythonプログラムからLLMへ入力を渡す
- LLMの応答を受け取る
- LangChainを使ってLLMを呼び出す
- APIキーの役割を理解する
- APIキーを環境変数で安全に管理する
- .envを利用して環境変数を管理する

Chapter 1では、AI Agentについて次のような構成を学びました。

```text
User
  |
  v
LLM
  |
  v
Answer
```

今回は、この最もシンプルな構成をPythonで実装します。
まだToolやAgentは登場しません。
まずは、

```text
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

という最小構成を実際に動かしてみましょう。

## 1. 今回作るプログラム

今回作成するプログラムは非常にシンプルです。

PythonからLLMに、

> AI Agentとは何ですか？

という質問を送ります。

LLMから返ってきた回答をPythonで受け取り、Terminalに表示します。
処理の流れは次のようになります。

```text
main.py
  |
  | 質問
  v
LangChain
  |
  | API Request
  v
LLM
  |
  | Response
  v
LangChain
  |
  v
main.py
  |
  v
Terminal
```

この仕組みが、これから作るAI Agentの最も基本的な部分になります。

## 2. APIとは

LLMをPythonから利用する前に、APIについて簡単に理解しておきましょう。

APIは **Application Programming Interface** の略です。

簡単に表現すると、

> プログラムから別のサービスやプログラムの機能を利用するための窓口

です。
今回の場合、PythonプログラムからLLMを利用します。

```text
Python
   |
   | Request
   v
LLM API
   |
   | Response
   v
Python
```

PythonプログラムがAPIへリクエストを送り、LLMが生成した結果をレスポンスとして受け取ります。
普段ChatGPTを利用するときは画面から文章を入力します。  
今回の教材では、**画面の代わりにPythonプログラムからLLMへ入力を送ります。**

## 3. APIキーとは

LLM APIを利用するときには、APIキーが必要になります。  
APIキーは、

> **「誰がこのAPIを利用しているのか」をサービス側が確認するための認証情報**

の1つです。
イメージとしては次のようになります。

```text
Python
  |
  | API Key
  | Question
  v
LLM API
```

APIキーが正しくなければ、基本的にAPIを利用することはできません。

### 3.1 APIキーをソースコードに書かない

次のような実装は避けてください。

> api_key = "実際のAPIキー"

この状態でGitHubへPushすると、APIキーがGitの履歴に保存されてしまう可能性があります。  
APIキーが外部に漏れると、第三者にAPIを利用される危険があります。  
そのため、

```text
ソースコード
    |
    | APIキーを書かない
    v
環境変数
```

という形で管理します。

### 4. .envファイルを作る

この教材では、APIキーを.envファイルで管理します。  
プロジェクトのルートディレクトリに.envを作成します。

```text
ai-agent-tutorial/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── docs/
└── examples/
```

.envにAPIキーを設定します。

```text
OPENAI_API_KEY=ここに自分のAPIキーを設定
```

例えば次のような形式です。

```text
OPENAI_API_KEY=xxxxxxxxxxxxxxxx
```

実際のAPIキーは他の人に共有しないでください。

## 5. .envをGitHubに登録しない

.envにはAPIキーなどの秘密情報が入っています。  
そのため、GitHubへPushしてはいけません。  
.gitignoreに次の設定が存在することを確認してください。

```text
.env
```

これによって.envはGitの管理対象外になります。  
構成としては、

```text
.env
  |
  | Git管理しない
  X
GitHub
```

となります。

### 5.1 .env.exampleとは

一方で、このリポジトリを利用する別のエンジニアは、  
**どの環境変数を設定すればいいの？**  
ということが分かりません。

そこで利用するのが.env.exampleです。  
.env.exampleには、**値を入れずに必要な環境変数名だけ記載**します。

```text
OPENAI_API_KEY=
```

.env.exampleはGitHubへ登録します。  
整理すると次のようになります。

| ファイル | Git管理 | 内容 |
| --- | --- | --- |
| .env | しない | 実際のAPIキー |
| .env.example | する | 必要な環境変数の名前 |

この方法はAI開発に限らず、Webアプリケーションなどでもよく利用されます。

## 6. 必要なライブラリを確認する

Chapter 2では、次のライブラリをインストールしました。

```text
langchain
langgraph
langchain-openai
python-dotenv
```

今回は、この中から主に、

```text
langchain-openai
python-dotenv
```

を利用します。
仮想環境を有効化します。

macOS / Linux / GitHub Codespacesの場合：

```text
source .venv/bin/activate
```

Windows PowerShellの場合：

```text
.venv\Scripts\Activate.ps1
```

続いて、ライブラリがインストールされていることを確認します。

```text
pip list
```

必要なライブラリがない場合は、requirements.txtからインストールします。

```text
pip install -r requirements.txt
```

## 7. Chapter 3のディレクトリへ移動する

今回使用するプログラムは、次の場所に作成します。

```text
examples/
└── chapter03_llm/
    ├── README.md
    └── main.py
```

Terminalから移動します。

```text
cd examples/chapter03_llm
```

現在のディレクトリを確認します。

```text
pwd
```

## 8. PythonからLLMを呼び出す

main.pyを開き、次のコードを書きます。

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# .envファイルから環境変数を読み込む
load_dotenv()


# LLMを準備する
llm = ChatOpenAI(
    model="gpt-5.5"
)


# LLMへ質問を送る
response = llm.invoke(
    "AI Agentとは何ですか？初心者向けに簡単に説明してください。"
)


# LLMから返ってきた回答を表示する
print(response.content)
```

ここでは、まずプログラム全体を動かしてみます。

Terminalから次のコマンドを実行します。

```bash
python main.py
```

環境によっては、

```bash
python3 main.py
```

を使用します。  
正常に実行できれば、TerminalにLLMからの回答が表示されます。

```text
AI Agentとは、AIが目的に応じて...
```

回答内容は毎回完全に同じになるとは限りません。  
これで、

```text
Python
  |
  v
LLM
  |
  v
Response
```

という最初のLLMアプリケーションが完成しました。

## 9. コードを理解する

動かすことができたら、先ほどのコードを1つずつ確認していきます。

### 9.1 load_dotenv

```python
from dotenv import load_dotenv
```

python-dotenvからload_dotenvを読み込んでいます。  
そして、

```python
load_dotenv()
```

を実行することで、.envに設定した値を環境変数として読み込めるようにします。  
今回の場合、

```python
OPENAI_API_KEY=...
```

が読み込まれます。  
ChatOpenAIはこの環境変数を利用してAPIへ接続します。  
そのため、PythonコードにAPIキーを直接書く必要がありません。  

## 9.2 ChatOpenAI

次に、

```python
from langchain_openai import ChatOpenAI
```

を確認します。  
**ChatOpenAIは、LangChainからOpenAIのLLMを利用するためのクラス**です。  
今回のコードでは、

```python
llm = ChatOpenAI(
    model="gpt-5.5"
)
```

として、LLMを利用するためのオブジェクトを作成しています。  
イメージとしては、

```text
main.py
   |
   v
ChatOpenAI
   |
   v
OpenAI API
```

です。  
このllmを使って、PythonからLLMへリクエストを送ります。

## 9.3 invoke

LLMを呼び出しているのが次の部分です。

```python
response = llm.invoke(
    "AI Agentとは何ですか？初心者向けに簡単に説明してください。"
)
```

invokeには「呼び出す」という意味があります。  
LangChainでは、

```python
llm.invoke(...)
```

とすることで、LLMへ入力を渡して結果を取得できます。  
処理のイメージは次の通りです。

```text
"AI Agentとは何ですか？"
           |
           v
      llm.invoke()
           |
           v
         LLM
           |
           v
       response
```

responseには、LLMから返された結果が格納されます。

### 9.4 response.content

最後に、

```python
print(response.content)
```

を実行しています。  
LLMから返ってくるresponseには、回答本文以外の情報も含まれています。  
今回は回答本文だけを表示したいため、

```python
response.content
```

を利用します。

```text
response
   |
   +-- content
   |
   +-- その他の情報
```

そして、

```python
print()
```

でTerminalに表示しています。

## 10. 処理全体をもう一度確認する

ここまでの処理を整理してみましょう。

```text
main.py
  |
  | load_dotenv()
  v
.envからAPIキーを読み込む
  |
  v
ChatOpenAIを作成
  |
  v
llm.invoke()
  |
  | Prompt
  v
OpenAI API
  |
  | Response
  v
response
  |
  v
response.content
  |
  v
Terminal
```

今回のコードで重要なのは、次の3行です。

```python
llm = ChatOpenAI(model="gpt-5.5")
response = llm.invoke("AI Agentとは何ですか？")
print(response.content)
```

非常にシンプルですが、この、

```text
入力
 ↓
LLM
 ↓
出力
```

がAI Agentの土台になります。

## 11. 自分で質問を変更してみる

プログラムが動いたら、質問を変更してみましょう。  
例えば、

```python
response = llm.invoke(
    "Pythonの特徴を3つ教えてください。"
)
```

として実行します。

```python
python main.py
```

次に、

```python
response = llm.invoke(
    "LangChainとは何ですか？"
)
```

などに変更してみます。  
質問を変更すると回答も変わることを確認してください。

## 12. 演習

ここからは、自分でコードを変更してみましょう。

### 演習1：質問を変更する

LLMへの質問を、

```text
PythonとJavaの違いを3つ教えてください。
```

に変更してください。

### 演習2：回答方法を指定する

次のような質問に変更してください。

```text
PythonとJavaの違いを、初心者向けに表形式で説明してください。
```

入力する文章によって、LLMの回答方法を制御できることを確認してください。

## 演習3：変数に分ける

現在は、

```python
response = llm.invoke(
    "AI Agentとは何ですか？"
)
```

と直接質問を書いています。  
質問をquestionという変数に分けてみましょう。

```python
question = "AI Agentとは何ですか？"

response = llm.invoke(question)

print(response.content)
```

最終的に次の流れになっていればOKです。

```text
question
   |
   v
llm.invoke()
   |
   v
response
   |
   v
response.content
```

## 13. よくあるエラー

### ModuleNotFoundError

例えば次のエラーが発生することがあります。

```text
ModuleNotFoundError: No module named 'langchain_openai'
```

#### 原因候補

- 仮想環境が有効になっていない
- langchain-openaiがインストールされていない
- VS Codeが別のPython Interpreterを利用している

#### 確認方法

```bash
pip list
```

を実行して、
**langchain-openai**  
が存在することを確認します。

#### 修正方法

必要であれば、

```bash
pip install -r requirements.txt
```

を実行してください。

### APIキーに関するエラー

認証に関するエラーが発生した場合は、APIキーを確認します。

#### 原因候補

- .envが存在しない
- OPENAI_API_KEYが設定されていない
- APIキーが間違っている
- .envを読み込めていない

#### 確認方法

プロジェクトのルートディレクトリに、

```text
.env
```

確認方法

プロジェクトのルートディレクトリに、

.env

が存在することを確認します。  
さらに、

```python
OPENAI_API_KEY=...
```

という形式になっていることを確認します。　　
修正後、APIキーを正しく設定して、再度プログラムを実行します。

### .envが読み込まれない

今回の構成では、

```text
ai-agent-tutorial/
├── .env
│
└── examples/
    └── chapter03_llm/
        └── main.py
```

なっています。  
実行場所によっては、.envを想定通りに読み込めないことがあります。  
まずは教材リポジトリのルートディレクトリから、

```bash
python examples/chapter03_llm/main.py
```

として実行してみてください。  
この教材では、基本的にリポジトリのルートディレクトリからプログラムを実行する方針とします。

## 14. APIキーをGitへCommitしていないか確認する

最後に、非常に重要な確認をします。  
次のコマンドを実行してください。

```bash
git status
```

.envが表示されていないことを確認します。

例えば、

```text
Untracked files:
    .env
```

のように.envがGit管理対象として表示されている場合は、.gitignoreを確認してください。
```text
.env
```
APIキーなどの秘密情報は、GitHubへPushしないように注意してください。

## 15. このChapterで作ったもの

今回作成したものを整理します。

```text
ai-agent-tutorial/
│
├── .env
├── .env.example
├── .gitignore
│
├── docs/
│   └── 03_llm.md
│
└── examples/
    └── chapter03_llm/
        ├── README.md
        └── main.py
```

main.pyは次のようになりました。

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


llm = ChatOpenAI(
    model="gpt-5.5"
)

question = "AI Agentとは何ですか？初心者向けに簡単に説明してください。"

response = llm.invoke(question)

print(response.content)
```

これが、この教材で最初に作成したLLMアプリケーションです。


## 16. まとめ

このChapterでは、PythonからLLMを呼び出しました。
今回の重要なポイントは3つです。

### 1. PythonからLLMを呼び出せる

LangChainのChatOpenAIを利用して、PythonからLLMを呼び出しました。
```python
response = llm.invoke(question)
```

### 2. LLMの応答を取得できる

LLMから返された回答は、
```text
response.content
```
から取得できます。

### 3. APIキーは環境変数で管理する

APIキーをPythonコードへ直接記述せず、
```text
.env
```
で管理しました。

.envはGitHubへPushしません。

今回作った構成は、
```text
User Input
    |
    v
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
です。

まだAI Agentとは呼べない非常にシンプルなプログラムです。  
しかし、ここが重要なスタート地点です。  
次のChapterでは、LLMが外部の処理を利用するためのToolを作成します。

## 次のChapter

### Chapter 4：Toolを作ってみよう

次のChapterでは、Python関数からToolを作成します。  
例えば、
**Calculator Tool**  
を作り、
```text
Python関数
    |
    v
Tool
```
という関係を理解します。

その次のChapterでは、今回作ったLLMとToolを組み合わせます。
```text
LLM
 |
 | Tool Calling
 v
Tool
```
これによって、AI Agentらしい仕組みへ一歩進んでいきます。