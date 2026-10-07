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
python-ai-agent-tutorial/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── docs/
└── chapters/
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