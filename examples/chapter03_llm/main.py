from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# .envファイルから環境変数を読み込む
load_dotenv()


# LLMを作成する
llm = ChatOpenAI(
    model="gpt-5.5"
)


# LLMへ質問する
question = "AI Agentとは何ですか？初心者向けに簡単に説明してください。"

response = llm.invoke(question)


# LLMの回答を表示する
print(response.content)