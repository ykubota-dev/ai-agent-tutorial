from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from tools import add, multiply


# .envファイルから環境変数を読み込む
load_dotenv()


# LLMを作成する
llm = ChatOpenAI(
    model="gpt-4.1-mini"
)


# Agentが利用できるTool
tools = [
    add,
    multiply
]


# Agentを作成する
agent = create_agent(
    model=llm,
    tools=tools
)


# Agentへ依頼する
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "10と20を足して、"
                    "その結果に3を掛けてください。"
                )
            }
        ]
    }
)


# 最終回答を表示する
print(result["messages"][-1].content)