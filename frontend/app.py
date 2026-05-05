import streamlit as st
import requests

st.title("総務問い合わせ入力")
question = st.text_area("問い合わせ内容", height=160)

if st.button("APIに送信する"):
    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")
    else:
        # FastAPI-руу POST хүсэлт илгээж байна
        response = requests.post(
            "http://127.0.0.1:8001/analyze",
            json={"question": question},
            timeout=30
        )
        result = response.json()
        st.write("カテゴリ:", result["category"])
        st.write("緊急度:", result["priority"])
        st.write("回答案:", result["answer"])