import streamlit as st
import requests

API_URL = "http://localhost:8000"


if "page" not in st.session_state:
    st.session_state.page = "input"

if "selected_id" not in st.session_state:
    st.session_state.selected_id = None


# =========================
# SIDEBAR
# =========================
page = st.sidebar.radio("メニュー", ["問い合わせ入力", "問い合わせ一覧"])


# =========================
# INPUT
# =========================
if page == "問い合わせ入力":

    st.title("AI問い合わせ管理アプリ")

    question = st.text_area("問い合わせ内容", height=150)

    if st.button("送信する"):

        if question.strip() == "":
            st.error("入力してください")

        else:
            res = requests.post(
                f"{API_URL}/inquiries",
                json={"question": question}
            )

            if res.ok:
                data = res.json()

                st.success("送信成功")
                st.write("カテゴリ:", data["category"])
                st.write("緊急度:", data["urgency"])
                st.write("回答:", data["answer"])

            else:
                st.error("送信失敗")


# =========================
# LIST
# =========================
elif page == "問い合わせ一覧":

    st.title("問い合わせ一覧")

    res = requests.get(f"{API_URL}/inquiries")

    if res.ok:

        data = res.json()

        for item in data:

            st.write("----")
            st.write("日時:", item["created_at"])
            st.write("内容:", item["question"])

            if st.button("詳細", key=item["id"]):

                st.session_state.selected_id = item["id"]
                st.session_state.page = "detail"
                st.rerun()


# =========================
# DETAIL
# =========================
if st.session_state.page == "detail":

    st.title("詳細画面")

    res = requests.get(
        f"{API_URL}/inquiries/{st.session_state.selected_id}"
    )

    if res.ok:

        d = res.json()

        st.write("内容:", d["question"])
        st.write("日時:", d["created_at"])
        st.write("カテゴリ:", d["category"])
        st.write("緊急度:", d["urgency"])
        st.write("回答:", d["answer"])

        if st.button("戻る"):
            st.session_state.page = "list"
            st.rerun()