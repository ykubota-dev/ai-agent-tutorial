# Chapter 4: Toolを作る

## この章で学ぶこと

この章では、AI Agentが外部の処理を利用するための **Tool** を作成します。

この章を読み終えると、以下のことができるようになります。

- Toolの役割と入出力を理解する
- Python関数をToolとして考えられるようになる
- Python関数をLangChainのToolとして定義する
- LLMとToolの役割の違いを理解する
- LLMだけではできない処理を外部機能に任せる考え方を理解する

---

## 1. 前のChapterのおさらい

Chapter 3では、PythonからLLMを呼び出しました。

```text
User Input
    │
    ▼
  Python
    │
    ▼
   LLM
    │
    ▼
 Response
```

この構成では、ユーザーから受け取った質問をLLMへ渡し、LLMが回答を生成していました。

しかし、実際のAI Agentでは**LLMだけでは実行できない処理**も必要になります。

例えば、次のような処理です。

- 最新の天気を取得する
- Webを検索する
- データベースを検索する
- ファイルを読み込む
- 社内APIを呼び出す
- 正確な計算を行う

このような処理をLLMの外側に任せるために利用するのが **Tool** です。

---

## 2. Toolとは

Toolとは、AI Agentが利用できる**外部機能**です。

例えば、次のようなToolが考えられます。

| Tool | 役割 |
| --- | --- |
| `calculator` | 計算する |
| `search` | Webを検索する |
| `weather` | 天気情報を取得する |
| `search_customer` | 顧客情報を検索する |
| `get_inventory` | 在庫情報を取得する |

例えば、天気を取得する場合を考えてみます。

```text
LLM
 │
 │ 「東京の現在の天気を知りたい」
 ▼
Weather Tool
 │
 ▼
Weather API
 │
 ▼
天気情報
```

LLM自身が天気情報を持っているのではなく、**天気を取得できるToolに処理を任せます。**

> **LLMは「何をするか」を判断し、Toolは「実際の処理」を担当する**

この役割分担が、AI Agentを理解するうえで重要になります。

---

## 3. Toolは特別なプログラムではない

「Tool」という名前を見ると、AI専用の特殊なプログラムに感じるかもしれません。

しかし、Toolの中身は基本的には普通のプログラムです。

例えば、商品を検索するPython関数があるとします。

```python
def search_product(product_name: str):
    # 商品を検索する処理
    ...
```

AI Agentからこの処理を利用できるようにすると、

```text
AI Agent
    │
    ▼
search_product Tool
    │
    ▼
商品検索処理
    │
    ▼
Database
```

という構成になります。

つまりToolは、

> **Python関数などの処理を、AI Agentから利用できる形にしたもの**

と考えることができます。

---

## 4. Toolの基本構造

Toolには主に次の情報があります。

| 要素 | 内容 |
| --- | --- |
| 名前 | 何というToolなのか |
| 説明 | 何をするToolなのか |
| 入力 | Toolへ渡すデータ |
| 処理 | Toolが実際に行う処理 |
| 出力 | Toolから返す結果 |

例えば、2つの数字を足し算するToolなら次のようになります。

```text
Tool名
  add

説明
  2つの整数を足し算する

入力
  a = 10
  b = 20

処理
  10 + 20

出力
  30
```

処理の流れはシンプルです。

```text
入力
 │
 ▼
Tool
 │
 ▼
処理
 │
 ▼
出力
```

これは普通のPython関数とほとんど同じです。

---

## 5. まず普通のPython関数を作る

いきなりToolを作る前に、普通のPython関数を作ってみましょう。

Chapter 4では、次のファイルを使用します。

```text
chapters/
└── chapter04_tool/
    ├── README.md
    └── main.py
```

`main.py`を開いて、次のコードを書きます。

```python
def add(a: int, b: int) -> int:
    return a + b


result = add(10, 20)

print(result)
```

リポジトリのルートディレクトリから実行します。

```bash
python chapters/chapter04_tool/main.py
```

実行結果：

```text
30
```

処理の流れを図にすると次のようになります。

```text
10, 20
  │
  ▼
add()
  │
  ▼
 30
```

---

## 6. 関数の入力と出力を確認する

先ほど作った関数をもう一度確認します。

```python
def add(a: int, b: int) -> int:
    return a + b
```

この関数には、**入力・処理・出力**があります。

```text
入力
a = 10
b = 20

  │
  ▼

処理
a + b

  │
  ▼

出力
30
```

Toolも基本的な考え方は同じです。

```text
Tool Input
    │
    ▼
   Tool
    │
    ▼
Tool Output
```

そのため、

> **Toolを作る = 入力と出力を持つ処理を作る**

と考えると理解しやすくなります。

---

## 7. Python関数をToolにする

それでは、先ほどのPython関数をLangChainのToolにしてみましょう。

LangChainでは、`@tool`を利用できます。

```python
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b
```

普通のPython関数から変わった部分は主に2つです。

```python
@tool
```

を追加したことと、

```python
"""2つの整数を足し算します。"""
```

という説明を追加したことです。

---

## 8. `@tool`とは

`@tool`はPythonの**デコレータ**という仕組みを利用しています。

```python
@tool
def add(a: int, b: int) -> int:
    ...
```

デコレータそのものの仕組みは、この教材では深く扱いません。

まずは、

> **Python関数をLangChainのToolとして扱えるようにするもの**

と理解しておけば問題ありません。

イメージすると次のようになります。

```text
Python関数

def add(...)

    │
    │ @tool
    ▼

LangChain Tool

add
```

---

## 9. Toolの説明を書く

次の部分に注目してください。

```python
"""2つの整数を足し算します。"""
```

これはPythonの **docstring** と呼ばれるものです。

関数が何をするためのものなのかを説明しています。

今回のToolは、次のような情報を持つことになります。

```text
名前
add

説明
2つの整数を足し算します。

入力
a: int
b: int
```

この**説明**はAI Agentを作るときに重要になります。

なぜなら、後のChapterではLLMが、

> 「このToolは何をするものなのか？」

を確認して、利用するToolを判断するからです。

そのため、

```python
"""処理します。"""
```

のような曖昧な説明より、

```python
"""2つの整数を足し算します。"""
```

のように、**Toolの役割を具体的に書くこと**が重要です。

---

## 10. 型ヒントもToolの情報になる

今回の関数には型ヒントがあります。

```python
def add(a: int, b: int) -> int:
```

それぞれ次の意味になります。

| 記述 | 意味 |
| --- | --- |
| `a: int` | `a`は整数 |
| `b: int` | `b`は整数 |
| `-> int` | 戻り値は整数 |

Toolとして考えると、

```text
add Tool

入力
├── a: integer
└── b: integer

出力
└── integer
```

という仕様になります。

AI AgentからToolを利用するときは、**Toolがどのような入力を受け取るのか**を明確にすることが重要です。

---

## 11. Toolの情報を確認する

作成したToolがどのような情報を持っているのか、実際に確認してみましょう。

```python
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b


print(add.name)
print(add.description)
print(add.args)
```

実行します。

```bash
python chapters/chapter04_tool/main.py
```

ここでは、Toolが持っている次の情報を確認できます。

- Tool名
- Toolの説明
- 引数の情報

つまり、

```text
関数名
+
docstring
+
型ヒント
```

から、

```text
Tool
├── 名前
├── 説明
└── 入力情報
```

が作られていることが分かります。

---

## 12. Toolを実行する

作成したToolを実際に実行してみましょう。

LangChainのToolは`invoke()`を使って実行できます。

```python
from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b


result = add.invoke(
    {
        "a": 10,
        "b": 20
    }
)

print(result)
```

実行します。

```bash
python chapters/chapter04_tool/main.py
```

実行結果：

```text
30
```

Toolには、次のように入力を渡しています。

```python
{
    "a": 10,
    "b": 20
}
```

処理の流れは次の通りです。

```text
{
  "a": 10,
  "b": 20
}
      │
      ▼
   add Tool
      │
      ▼
    10 + 20
      │
      ▼
      30
```

これで最初のToolが完成しました。

---

## 13. 普通のPython関数とToolの違い

ここまでの内容を整理してみましょう。

### 普通のPython関数

```python
def add(a: int, b: int) -> int:
    return a + b
```

Pythonプログラムから直接呼び出します。

```python
add(10, 20)
```

### LangChainのTool

```python
@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b
```

Toolとして、

- 名前
- 説明
- 入力情報
- 実行する処理

を持つようになります。

```text
Python関数
    │
    │ @tool
    ▼
LangChain Tool
    │
    ├── name
    ├── description
    ├── args
    └── 処理
```

この情報があることで、後のChapterではLLMからToolを利用できるようになります。

---

## 14. LLMとToolの役割の違い

ここが、このChapterで特に重要なポイントです。

LLMとToolには、それぞれ異なる役割があります。

例えば、ユーザーから、

```text
10と20を足してください。
```

という依頼を受けたとします。

AI Agentでは、次のような役割分担ができます。

```text
LLM
 │
 │ 「計算が必要だ」
 │
 │ 「add Toolを使おう」
 ▼
add Tool
 │
 │ 10 + 20
 ▼
30
```

整理すると、

| 要素 | 主な役割 |
| --- | --- |
| LLM | 何をするべきか判断する |
| Tool | 実際の処理を実行する |

つまり、

> **LLM = 判断**
>
> **Tool = 実行**

という関係です。

今後AI Agentを作っていくうえで、この役割分担を意識してください。

---

## 15. 実際にはどんなToolを作るのか

今回は学習のために、足し算を行うToolを作りました。

実際のシステムでは、さまざまな機能をToolとして利用できます。

例えば、社内システムで利用するAI Agentなら次のようなToolが考えられます。

```text
AI Agent
    │
    ├── search_customer
    │      └── 顧客DBを検索
    │
    ├── search_product
    │      └── 商品DBを検索
    │
    ├── get_inventory
    │      └── 在庫APIを呼び出す
    │
    ├── create_report
    │      └── レポートを作成
    │
    └── send_email
           └── メールを送信
```

例えば、

```text
「商品Aの在庫を調べて」
```

という依頼なら、

```text
User
 │
 ▼
LLM
 │
 │ 「在庫確認が必要」
 ▼
get_inventory Tool
 │
 ▼
Inventory API
 │
 ▼
在庫：20個
```

という処理が考えられます。

Toolを利用することで、LLMと実際のシステムを接続できるようになります。

---

## 16. Toolをもう1つ作る

足し算だけではToolの違いが分かりにくいため、もう1つ作ってみましょう。

今回は掛け算を行う`multiply` Toolを追加します。

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

これで2つのToolができました。

```text
Tools
 │
 ├── add
 │
 └── multiply
```

`multiply`を実行してみましょう。

```python
result = multiply.invoke(
    {
        "a": 10,
        "b": 20
    }
)

print(result)
```

実行結果：

```text
200
```

---

## 17. 現在は誰がToolを選んでいるのか

ここで1つ考えてみましょう。

今回のコードでは、

```python
result = multiply.invoke(
    {
        "a": 10,
        "b": 20
    }
)
```

と書いています。

つまり、

> **multiplyを使う**

と決めたのは誰でしょうか？

答えは、**プログラムを書いた人間**です。

現在の構成は次のようになっています。

```text
Developer
    │
    │ multiplyを指定
    ▼
multiply Tool
    │
    ▼
  Result
```

まだLLMはToolを選んでいません。

AI Agentらしい構成にするには、

```text
User
 │
 ▼
LLM
 │
 │ どのToolを使う？
 │
 ├── add
 │
 └── multiply
```

のように、**LLMに利用するToolを判断させる**必要があります。

この仕組みを **Tool Calling** と呼びます。

Tool Callingは次のChapterで実装します。

---

## 18. 演習

ここからは、自分でToolを作ってみましょう。

### 演習1：引き算Toolを作る

次の仕様で`subtract` Toolを作成してください。

| 項目 | 内容 |
| --- | --- |
| Tool名 | `subtract` |
| 入力 | `a`, `b` |
| 処理 | `a - b` |
| 出力 | 計算結果 |

ヒント：

```python
@tool
def subtract(a: int, b: int) -> int:
    """ここにToolの説明を書く"""
    ...
```

作成できたら、

```text
100 - 30
```

を計算してください。

期待する結果：

```text
70
```

---

### 演習2：割り算Toolを作る

次に、割り算を行う`divide` Toolを作成してください。

```text
100 / 20
```

を実行して、次の結果になることを確認してください。

```text
5.0
```

余裕があれば、

```text
100 / 0
```

を実行するとどうなるのかも確認してみましょう。

---

### 演習3：Toolの情報を確認する

作成した`subtract` Toolについて、次のコードを実行してください。

```python
print(subtract.name)
print(subtract.description)
print(subtract.args)
```

自分が書いた、

- 関数名
- docstring
- 型ヒント

がToolの情報として利用されていることを確認してください。

---

## 19. よくあるエラー

### Toolの説明がない

例えば、次のようにToolを作成したとします。

```python
@tool
def add(a: int, b: int) -> int:
    return a + b
```

Toolとして利用する場合は、何をするToolなのか分かるように説明を付けます。

```python
@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b
```

後のChapterでは、LLMがこの説明を参考にToolを選択します。

---

### 入力の型が分かりにくい

次の定義では、

```python
def add(a, b):
```

`a`と`b`に何を渡せばよいのか分かりにくくなります。

Toolでは、

```python
def add(a: int, b: int) -> int:
```

のように型を明示して、入力仕様を分かりやすくしておきましょう。

---

### `add(10, 20)`と実行してしまう

`@tool`を付けた後の`add`は、LangChainのToolとして扱われます。

この教材では、

```python
add.invoke(
    {
        "a": 10,
        "b": 20
    }
)
```

として実行します。

---

## 20. このChapterで作ったもの

今回作成した構成は次の通りです。

```text
python-ai-agent-tutorial/
│
├── docs/
│   └── 04_tool.md
│
└── chapters/
    └── chapter04_tool/
        ├── README.md
        └── main.py
```

`main.py`の最終形は次のようになります。

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


result = add.invoke(
    {
        "a": 10,
        "b": 20
    }
)

print(result)
```

これまで作ったものを整理すると、

### Chapter 3

```text
Python
 │
 ▼
LLM
```

### Chapter 4

```text
Python
 │
 ▼
Tool
```

となります。

現時点では、**LLMとToolはまだ接続されていません。**

---

## 21. まとめ

このChapterでは、AI Agentが利用するToolを作成しました。

重要なポイントは次の3つです。

### 1. Toolは外部処理を担当する

LLMだけですべての処理を行うのではなく、

```text
LLM  = 判断
Tool = 実行
```

という役割分担を行います。

### 2. Python関数をToolにできる

LangChainでは`@tool`を利用して、Python関数をToolとして定義できます。

```python
@tool
def add(a: int, b: int) -> int:
    """2つの整数を足し算します。"""
    return a + b
```

Toolには、

```text
Tool
├── 名前
├── 説明
├── 入力
├── 処理
└── 出力
```

があります。

### 3. 現在は人間がToolを選択している

Chapter 4の段階では、

```text
Developer
    │
    ▼
  Tool
```

という構成です。

まだLLM自身はToolを選択していません。

---

## 次のChapter

次のChapterでは、Chapter 3で作った**LLM**と、Chapter 4で作った**Tool**を接続します。

**Chapter 5：Tool Callingを使ってみよう**

目標となる構成は次の通りです。

```text
User
 │
 ▼
LLM
 │
 │ Toolを選択
 ▼
Tool
 │
 │ 実行結果
 ▼
LLM
 │
 ▼
Answer
```

ここで初めて、

> **LLMがユーザーの入力を見て、必要なToolを判断する**

というAI Agentの重要な仕組みを実装します。