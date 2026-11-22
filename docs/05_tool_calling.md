# Chapter 5: Tool Callingを理解する

## 前のChapterの限界と今回の解決

Chapter 4ではToolを作りました。しかし、どのToolを使うかはまだ開発者が決めています。LLMとToolは存在していても、LLM自身が必要なToolを選ぶ仕組みはありません。

```text
Chapter 4
Toolを実行できる
        ↓
しかしToolを選ぶのは人間
        ↓
Chapter 5
LLMがToolと引数を選ぶ
```

このChapterではTool Callingを使い、「判断するLLM」と「実行するTool」を接続します。

---

## この章で学ぶこと

この章では、Chapter 4で作成したToolをLLMから利用する **Tool Calling** を学びます。

この章を読み終えると、以下のことができるようになります。

- LLMがToolを選択する仕組みを理解する
- LLMがToolへ渡す引数を決める仕組みを理解する
- LLMが出力したTool Callの内容を確認する
- LLMが選択したToolを実行する
- Toolの実行結果をLLMへ返す
- Toolを定義することとTool Callingの違いを説明できる

Chapter 4では、Python関数からToolを作成しました。

今回は、Chapter 3で作った**LLM**と、Chapter 4で作った**Tool**を接続します。

```text
Chapter 3
LLM

       ＋

Chapter 4
Tool

       ↓
Chapter 5

LLM
 │
 │ Tool Calling
 ▼
Tool
```

ここから、AI Agentらしい処理が少しずつ始まります。

---

## 1. Chapter 4のおさらい

Chapter 4では、次のようなToolを作成しました。

```python
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算します。"""
    return a * b
```

そして、Toolを次のように実行しました。

```python
result = add.invoke(
    {
        "a": 10,
        "b": 20
    }
)
```

このとき、

> `add`を使う

と判断しているのは、プログラムを書いた人間です。

```text
Developer
    │
    │ addを使う
    ▼
add Tool
    │
    ▼
   30
```

しかし、AI Agentではユーザーの依頼によって利用するToolが変わります。

例えば、

```text
「10と20を足してください」
```

なら`add`を使い、

```text
「10と20を掛けてください」
```

なら`multiply`を使いたいはずです。

そこで、**どのToolを利用するのかをLLMに判断させます。**

---

## 2. Tool Callingとは

Tool Callingとは、

> **LLMが利用するToolと、そのToolへ渡す引数を判断する仕組み**

です。

例えば、LLMに次の質問を渡します。

```text
10と20を足してください。
```

LLMには、次の2つのToolが利用できることを伝えておきます。

```text
Tools
 │
 ├── add
 │
 └── multiply
```

するとLLMは、ユーザーの入力を見て、

```text
「足し算が必要だ」
        ↓
「addを使おう」
        ↓
「a=10、b=20を渡そう」
```

と判断できます。

概念的には次のような流れです。

```text
User

「10と20を足してください」
        │
        ▼
       LLM
        │
        ├── Tool: add
        │
        ├── a: 10
        │
        └── b: 20
```

ここで重要なのは、

> **LLMがToolを直接実行しているわけではない**

という点です。

LLMは、

```text
addを
a=10
b=20
で実行してください
```

という**Tool Call（Toolの呼び出し要求）**を生成します。

---

## 3. Tool Callingの全体像

最初に、今回実装する処理全体を確認しておきましょう。

```text
① User Input
      │
      ▼
② LLM
      │
      │ Toolを選択
      ▼
③ Tool Call
      │
      │ Tool名 + 引数
      ▼
④ Tool Execution
      │
      ▼
⑤ Tool Result
      │
      ▼
⑥ LLM
      │
      ▼
⑦ Final Answer
```

例えば、

```text
10と20を足してください
```

という入力なら、次のようになります。

```text
User
 │
 │ 「10と20を足してください」
 ▼
LLM
 │
 │ addを使う
 │ a=10
 │ b=20
 ▼
add Tool
 │
 │ 10 + 20
 ▼
30
 │
 │ Tool Result
 ▼
LLM
 │
 ▼
「10と20を足した結果は30です。」
```

この流れを1つずつ実装していきます。

---

## 4. Chapter 5で使用するToolを準備する

Chapter 5では、次の構成を使用します。

```text
examples/
└── chapter05_tool_calling/
    ├── README.md
    ├── main.py
    └── tools.py
```

Chapter 4で作ったToolを`tools.py`へ移します。

```python
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """2つの整数を掛け算します。"""
    return a * b
```

Chapter 4ですでにToolの作り方を学んでいるため、このChapterでは詳しい説明は省略します。

今回重要なのは、

> **このToolをLLMからどのように利用するのか**

という部分です。

---

## 5. LLMを準備する

Chapter 3と同じようにLLMを準備します。
`main.py`を作成します。

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from tools import add, multiply


load_dotenv()


llm = ChatOpenAI(
    model="gpt-5.5"
)
```

ここまでの構成は、

```text
LLM

add Tool

multiply Tool
```

という状態です。  
まだLLMは、Toolの存在を知りません。

---

## 6. LLMにToolを教える

LLMからToolを利用するためには、

> **このLLMは、このToolを利用できます**

という情報をLLMへ渡す必要があります。  
LangChainでは`bind_tools()`を利用します。

```python
tools = [
    add,
    multiply
]


llm_with_tools = llm.bind_tools(tools)
```

これによって、

```text
LLM
 │
 │ bind_tools
 ▼
Tools
 │
 ├── add
 └── multiply
```

という関係ができます。

つまり、

```python
llm
```

は通常のLLMですが、

```python
llm_with_tools
```

は、

```text
add
multiply
```

というToolを利用できることを知っているLLMになります。

---

## 7. LLMに質問する

それでは、Toolを登録したLLMへ質問してみましょう。

```python
response = llm_with_tools.invoke(
    "10と20を足してください。"
)
```

Chapter 3では、このあと、

```python
print(response.content)
```

としてLLMの回答を表示していました。  
今回は、少し違います。  
LLMにToolを渡しているため、LLMは、

```text
「この質問にはadd Toolを使えばよい」
```

と判断できます。  
そこで、LLMが生成したTool Callを確認してみましょう。

```python
print(response.tool_calls)
```

実行します。

```bash
python examples/chapter05_tool_calling/main.py
```

Tool Callには、概念的には次のような情報が含まれます。

```text
[
    {
        "name": "add",
        "args": {
            "a": 10,
            "b": 20
        },
        "id": "..."
    }
]
```

LLMは、

```text
Tool
add

Arguments
a = 10
b = 20
```

と判断したことが分かります。

---

## 8. Tool Callの中身を理解する

Tool Callには、主に次のような情報が含まれます。

| 項目 | 内容 |
| --- | --- |
| `name` | 呼び出したいTool |
| `args` | Toolへ渡したい引数 |
| `id` | Tool Callを識別するためのID |

今回の場合、

```text
name
  ↓
add

args
  ↓
a = 10
b = 20
```

となっています。

つまりLLMは、

```text
ユーザーの入力
「10と20を足してください」
        │
        ▼
      判断
        │
        ├── addを使う
        ├── a = 10
        └── b = 20
```

という処理を行ったことになります。

---

## 9. Chapter 4のTool情報がここで使われる

Chapter 4では、Toolに、

- 名前
- 説明
- 型ヒント

があることを学びました。

例えば、

```python
@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b
```

というToolには、

```text
Tool名
add

説明
2つの整数を足し算します。

入力
a: int
b: int
```

という情報があります。

LLMはこのようなToolの情報を参考にして、

```text
どのToolを使うか
```

そして、

```text
どんな引数を渡すか
```

を判断します。

Chapter 4でToolの説明や型を明確にした理由が、ここでつながります。

---

## 10. Tool CallingとTool実行は別の処理

ここは非常に重要です。

LLMが返した、

```text
{
    "name": "add",
    "args": {
        "a": 10,
        "b": 20
    }
}
```

は、

> **add Toolをa=10、b=20で実行したい**

という要求です。  
この時点では、まだ`add`は実行されていません。

```text
LLM
 │
 │ Tool Call
 ▼
「add(a=10, b=20)を使いたい」
```

ここまでが **Tool Calling** です。  
そのあと、実際にToolを実行します。

```text
Tool Call
    │
    ▼
Tool Execution
    │
    ▼
Result
```

つまり、

> **Tool Calling = Toolを選び、呼び出し方を決める**

> **Tool Execution = Toolの処理を実際に実行する**

という違いがあります。

---

## 11. LLMが選んだToolを実行する

それでは、LLMが生成したTool Callを使ってToolを実行してみましょう。  
まず、Toolを名前から取得できるようにします。

```python
tools_by_name = {
    "add": add,
    "multiply": multiply
}
```

次に、LLMが生成したTool Callを取得します。

```python
tool_call = response.tool_calls[0]
```

Tool名を取得します。

```python
tool_name = tool_call["name"]
```

引数を取得します。

```python
tool_args = tool_call["args"]
```

Toolを取得します。

```python
selected_tool = tools_by_name[tool_name]
```

そして実行します。

```python
tool_result = selected_tool.invoke(tool_args)
```

処理全体は次のようになります。

```text
Tool Call

name = add

args
├── a = 10
└── b = 20

      │
      ▼

tools_by_name["add"]

      │
      ▼

add Tool

      │
      ▼

add.invoke({
    "a": 10,
    "b": 20
})

      │
      ▼

30
```

これで、LLMが選択したToolをPython側で実行できました。

---

## 12. Toolの実行結果を確認する

Toolの結果を表示してみましょう。

```python
print(tool_result)
```

実行結果：

```text
30
```

ここまでで、

```text
User
 │
 ▼
LLM
 │
 │ Tool Call
 ▼
add Tool
 │
 ▼
30
```

まで実装できました。  
しかし、まだ処理は終わりではありません。

---

## 13. なぜToolの結果をLLMへ戻すのか

Toolから、

```text
30
```

という結果を取得できました。  
このまま`30`をユーザーへ返すこともできます。

しかし、実際のAI AgentではToolの結果を利用してLLMに最終回答を作らせたい場合があります。

例えば、

```text
Tool Result

30
```

だけではなく、

```text
10と20を足した結果は30です。
```

と回答したい場合です。

そのため、

```text
Tool
 │
 │ Result
 ▼
LLM
 │
 │ 回答を生成
 ▼
User
```

という流れを作ります。

---

## 14. Toolの結果をLLMへ戻す

Tool Callingでは、Toolを実行した結果をLLMへ返します。  
概念的には次のような流れです。

```text
User Message
     │
     ▼
    LLM
     │
     │ Tool Call
     ▼
    Tool
     │
     │ Tool Result
     ▼
    LLM
     │
     ▼
Final Answer
```

ここでは、会話の履歴を`messages`として管理します。  
まずユーザーのメッセージを作ります。

```python
from langchain_core.messages import HumanMessage


messages = [
    HumanMessage(
        content="10と20を足してください。"
    )
]
```

LLMへ渡します。

```python
response = llm_with_tools.invoke(messages)
```

LLMから返されたメッセージも履歴へ追加します。

```python
messages.append(response)
```

---

## 15. Toolの結果をメッセージとして追加する

Toolを実行します。

```python
tool_call = response.tool_calls[0]

selected_tool = tools_by_name[
    tool_call["name"]
]

tool_result = selected_tool.invoke(
    tool_call["args"]
)
```

次に、この結果をLLMへ返すためのメッセージを作ります。

```python
from langchain_core.messages import ToolMessage
```

Toolの結果を`ToolMessage`として追加します。

```python
messages.append(
    ToolMessage(
        content=str(tool_result),
        tool_call_id=tool_call["id"]
    )
)
```

ここで`tool_call_id`を指定することで、

> **どのTool Callに対する実行結果なのか**

をLLM側へ伝えます。  
処理の関係は次のようになります。

```text
Tool Call
id = abc123
     │
     ▼
add Tool
     │
     ▼
30
     │
     ▼
ToolMessage
tool_call_id = abc123
```

Tool CallとTool Resultを対応付けています。

---

## 16. Toolの結果を使って最終回答を生成する

Tool Resultまで追加した`messages`を、もう一度LLMへ渡します。

```python
final_response = llm_with_tools.invoke(messages)
```

最後に回答を表示します。

```python
print(final_response.content)
```

例えば、

```text
10と20を足した結果は30です。
```

のような回答が生成されます。

これで、

```text
User
 │
 ▼
LLM
 │
 │ Tool Call
 ▼
Tool
 │
 │ Tool Result
 ▼
LLM
 │
 ▼
Answer
```

というTool Callingの基本的な流れが完成しました。

---

## 17. 完成したコードを確認する

ここまでの処理を1つにつなげてみましょう。  
`main.py`は次のようになります。

```python
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

from tools import add, multiply


load_dotenv()


# LLMを作成
llm = ChatOpenAI(
    model="gpt-5.5"
)


# 利用できるTool
tools = [
    add,
    multiply
]


# LLMへToolを登録
llm_with_tools = llm.bind_tools(tools)


# Tool名からToolを取得するための辞書
tools_by_name = {
    tool.name: tool
    for tool in tools
}


# User Message
messages = [
    HumanMessage(
        content="10と20を足してください。"
    )
]


# LLMへ質問
response = llm_with_tools.invoke(messages)

messages.append(response)


# Tool Callが存在する場合だけ実行する
if response.tool_calls:
    # 複数のTool Callにも対応する
    for tool_call in response.tool_calls:
        selected_tool = tools_by_name[tool_call["name"]]
        tool_result = selected_tool.invoke(tool_call["args"])
        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

    final_response = llm_with_tools.invoke(messages)
    print(final_response.content)
else:
    # Toolが不要なら最初の回答を表示する
    print(response.content)
```

---

## 18. 処理全体をもう一度確認する

コードだけを見ると少し複雑に感じるかもしれません。  
しかし、処理自体は次の7ステップです。

```text
① User Input
      │
      ▼
② LLMへ入力
      │
      ▼
③ Tool Callを取得
      │
      ▼
④ Toolを選択
      │
      ▼
⑤ Toolを実行
      │
      ▼
⑥ Tool ResultをLLMへ返す
      │
      ▼
⑦ Final Answer
```

今回の場合は、

```text
「10と20を足してください」
        │
        ▼
       LLM
        │
        │ add
        │ a=10
        │ b=20
        ▼
     add Tool
        │
        ▼
        30
        │
        ▼
       LLM
        │
        ▼
「10と20を足した結果は30です。」
```

となります。

この流れを理解することが、このChapterの最大の目的です。

---

## 19. Toolを定義することとTool Callingの違い

Chapter 4とChapter 5の違いを整理しましょう。

| | Toolを定義する | Tool Calling |
| --- | --- | --- |
| 学ぶChapter | Chapter 4 | Chapter 5 |
| 目的 | 利用できる機能を作る | 利用する機能をLLMが判断する |
| 主な処理 | Python関数をToolにする | LLMがToolと引数を選ぶ |
| 主役 | Python | LLM |
| 例 | `add`を作る | LLMが`add`を選択する |

一言で表すと、

```text
Tool
= できることを定義する


Tool Calling
= どのToolをどう使うか判断する
```

という違いです。

---

## 20. Toolを使わない質問もある

LLMにToolを登録したからといって、必ずToolを利用するわけではありません。

例えば、

```text
10と20を足してください。
```

という質問なら、

```text
LLM
 │
 ▼
add Tool
```

と判断する可能性があります。

一方、

```text
こんにちは。
```

という質問なら、計算Toolを使う必要はありません。

```text
User

「こんにちは」
     │
     ▼
    LLM
     │
     │ Tool不要
     ▼
「こんにちは！」
```

つまり、LLMは、

```text
Toolが必要
   ↓
Tool Calling


Toolが不要
   ↓
そのまま回答
```

という判断も行います。

---

## 21. Tool Callが存在するか確認する

そのため、実際のプログラムでは、

```python
response.tool_calls[0]
```

と必ずTool Callが存在すると決めつけるのではなく、

```python
if response.tool_calls:
```

として確認する必要があります。

例えば、

```python
response = llm_with_tools.invoke(messages)

messages.append(response)


if response.tool_calls:
    tool_call = response.tool_calls[0]

    selected_tool = tools_by_name[
        tool_call["name"]
    ]

    tool_result = selected_tool.invoke(
        tool_call["args"]
    )

    messages.append(
        ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"]
        )
    )

    final_response = llm_with_tools.invoke(messages)

    print(final_response.content)

else:
    print(response.content)
```

これによって、

```text
Toolが必要？
    │
    ├── YES → Toolを実行
    │
    └── NO  → LLMの回答を表示
```

という処理ができます。

---

## 22. 演習

ここからは、自分でTool Callingを試してみましょう。

### 演習1：addを選択させる

次の質問をLLMへ渡してください。

```text
30と15を足してください。
```

LLMが、

```text
add
```

を選択することを確認してください。

さらに、

```python
print(response.tool_calls)
```

を使って、引数がどのようになっているか確認してください。

---

### 演習2：multiplyを選択させる

次の質問へ変更してください。

```text
12と8を掛けてください。
```

LLMが、

```text
multiply
```

を選択することを確認してください。

---

### 演習3：Toolを使わない質問

次の質問を入力してください。

```text
こんにちは。
```

`response.tool_calls`を確認してください。

Toolを利用しない場合に、プログラムがどのように動くか確認しましょう。

---

### 演習4：少し複雑な質問をしてみる

次の質問を試してみましょう。

```text
10と20を足して、その結果に3を掛けてください。
```

どのようなTool Callが生成されるか観察してください。

> **Note**
>
> この処理では、Toolを複数回利用する必要があります。
>
> 現在のプログラムは、基本的に1回のTool Callingを扱う構成です。
>
> Tool Callingを繰り返しながら処理を進める仕組みは、今後Agentを作るChapterで学びます。

---

### 演習の確認ポイント

次を確認できれば、このChapterの演習は完了です。

- 足し算の依頼で `add` のTool Callを確認できる
- 掛け算の依頼で `multiply` のTool Callを確認できる
- Toolが不要な質問ではTool Callが生成されない場合があることを確認できる
- Tool Callingは「Toolの選択と引数の決定」であり、Tool実行そのものではないと説明できる
- 複数段階の処理では、現在の手動制御が複雑になることを確認できる

LLMによるTool選択は非決定的なため、実行結果が毎回完全に同じになることを合格条件にはしません。


## 23. よくある勘違い

### Tool CallingをするとLLMがToolを実行してくれる？

Tool Callingは、

```text
Toolを選択
+
引数を決定
```

する仕組みです。

Toolの実行自体は、Pythonプログラム側で行います。

```text
LLM
 │
 │ Tool Call
 ▼
Python
 │
 │ Tool Execution
 ▼
Tool
```

---

### Toolを登録すれば必ず利用される？

必ず利用されるわけではありません。

LLMが、

```text
この質問にはToolが必要
```

と判断した場合にTool Callが生成されます。

そのため、

```python
if response.tool_calls:
```

のようにTool Callの有無を確認します。

---

### Toolの結果はそのままユーザーへ返せばいい？

システムによっては、それでも問題ありません。  
しかし、Toolの結果を使って自然な回答を生成したい場合は、

```text
Tool Result
    │
    ▼
   LLM
    │
    ▼
Final Answer
```

という処理を行います。

---

## 24. このChapterで作ったもの

今回作成した構成は次の通りです。

```text
ai-agent-tutorial/
│
├── docs/
│   └── 05_tool_calling.md
│
└── examples/
    └── chapter05_tool_calling/
        ├── README.md
        ├── main.py
        └── tools.py
```

Chapter 3からの流れを整理すると、

```text
Chapter 3

LLMを呼び出す

User
 │
 ▼
LLM
 │
 ▼
Answer
```

Chapter 4では、

```text
Chapter 4

Toolを作る

Python
 │
 ▼
Tool
```

Chapter 5では、この2つを接続しました。

```text
Chapter 5

User
 │
 ▼
LLM
 │
 │ Tool Calling
 ▼
Tool
 │
 │ Tool Result
 ▼
LLM
 │
 ▼
Answer
```

---

## 25. まとめ

このChapterでは、Tool Callingの基本的な仕組みを実装しました。

重要なポイントは3つです。

### 1. LLMがToolと引数を選択する

ユーザーから、

```text
10と20を足してください。
```

と入力された場合、LLMは、

```text
Tool
add

Arguments
a = 10
b = 20
```

のようなTool Callを生成できます。

---

### 2. Tool CallingとTool実行は別

Tool Callingは、

```text
どのToolを使う？
どんな引数を渡す？
```

を決める処理です。

実際のTool実行はPython側で行います。

```text
LLM
 │
 │ Tool Calling
 ▼
Python
 │
 │ Tool Execution
 ▼
Tool
```

---

### 3. Tool ResultをLLMへ戻せる

Toolの結果をLLMへ戻すことで、その結果を利用した最終回答を生成できます。

```text
User
 │
 ▼
LLM
 │
 │ Tool Call
 ▼
Tool
 │
 │ Tool Result
 ▼
LLM
 │
 ▼
Final Answer
```

Chapter 5までで、

```text
LLM
+
Tool
+
Tool Calling
```

というAI Agentを作るための主要な部品が揃いました。

しかし、現在のプログラムでは、

```text
Tool Callを確認する
      ↓
Toolを探す
      ↓
Toolを実行する
      ↓
結果をLLMへ戻す
```

という制御を、自分たちでPythonコードとして書いています。

---

## 次のChapter

**Chapter 6：Agentを作る**

次のChapterでは、これまで学んだ、

```text
LLM
+
Tool
+
Tool Calling
```

を組み合わせて、**Agentとして処理を進める仕組み**を学びます。

```text
User
 │
 ▼
Agent
 │
 ├── LLMで判断
 │
 ├── Toolを選択
 │
 ├── Toolを実行
 │
 └── 結果を見て再び判断
 │
 ▼
Answer
```

Chapter 5ではTool Callingの仕組みを理解するために、処理を1つずつ自分で実装しました。

次のChapterでは、この仕組みをAgentとしてまとめていきます。