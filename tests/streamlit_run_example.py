import streamlit as st


def chatbot_response(text):
    responses = {
        "안녕": "안녕하세요! 무엇을 도와드릴까요?",
        "날씨 어때?": "현재 날씨는 모르지만, 인터넷에서 확인할 수 있어요!",
        "이름이 뭐야?": "저는 간단한 챗봇입니다.",
        "잘가": "다음에 또 만나요!"
    }
    return responses.get(text, "죄송해요, 이해하지 못했어요. 다시 말씀해 주세요!")


st.set_page_config(page_title="Simple Chatbot", layout="wide")
st.title("간단한 챗봇")

user_input = st.text_input("질문을 입력하세요:", "")

if user_input:
    response = chatbot_response(user_input)
    st.write("챗봇:", response)
