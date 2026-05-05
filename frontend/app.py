import streamlit as st

st.title("総務問い合わせ入力")
st.write("社員から総務への問い合わせを入力してください。")

question = st.text_area("問い合わせ内容", height=160)

if st.button("確認する"):
    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")
    else:
        st.success("入力内容を受け付けました。")
        st.subheader("入力された内容")
        st.write(question)