import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

# Webアプリの概要・操作説明
st.title("専門家LLM質問アプリ")
st.write("""
このWebアプリは、入力フォームに質問を入力し、ラジオボタンで専門家の種類を選択して送信すると、
選択した専門家の視点でLLM（大規模言語モデル）が回答します。
専門家の種類によって、回答の内容や視点が変わります。
""")

# 専門家の種類（自由に追加・変更可能）
expert_types = {
	"医療専門家": "あなたは医療分野の専門家です。専門的かつ分かりやすく回答してください。",
	"法律専門家": "あなたは法律分野の専門家です。法的観点から分かりやすく回答してください。",
	"ITエンジニア": "あなたはIT分野の専門家です。技術的な観点から分かりやすく回答してください。"
}

# ラジオボタンで専門家選択
expert_choice = st.radio("専門家の種類を選択してください", list(expert_types.keys()))

# 入力フォーム
user_input = st.text_area("質問を入力してください", height=100)

# LLM回答関数
def get_llm_answer(input_text, expert_type):
	system_message = expert_types[expert_type]
	prompt = ChatPromptTemplate.from_messages([
		SystemMessage(content=system_message),
		HumanMessage(content=input_text)
	])
	llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
	chain = prompt | llm
	response = chain.invoke({"input": input_text})
	return response.content

# 送信ボタン
if st.button("送信"):
	if user_input.strip():
		answer = get_llm_answer(user_input, expert_choice)
		st.markdown("### LLMの回答")
		st.write(answer)
	else:
		st.warning("質問を入力してください。")
from dotenv import load_dotenv
load_dotenv()


