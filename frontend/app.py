import streamlit as st
import time

st.title("総務問い合わせ入力")
st.write("社員から総務への問い合わせを入力してください。")

question = st.text_area("問い合わせ内容", height=160)
category = st.selectbox("カテゴリ", ["休暇", "給与", "福利厚生", "その他"])
priority = st.radio("緊急度", ["高", "中", "低"])

if st.button("確認する"):
    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")
    else:
        st.success("入力内容を受け付けました。")
        st.subheader("入力された内容")
        st.write(question)

import pandas as pd

inquiries = [
    {"id": 1, "question": "有給の申請方法は？", "category": "休暇"},
    {"id": 2, "question": "健康保険証を紛失した", "category": "保険"},
]
df = pd.DataFrame(inquiries)

st.dataframe(df)   # 操作可能なテーブル（列幅調整・ソートができる）
st.table(df)       # 静的なテーブル

# 列分割（入力フォームと結果を横並びにするときなど）
col1, col2 = st.columns(2)
with col1:
    st.write("左側：入力フォーム")
with col2:
    st.write("右側：回答結果")

# 折りたたみ（詳細情報を隠しておくときなど）
with st.expander("回答の詳細を見る"):
    st.write("ここに詳細内容が入ります。")

# サイドバー（ページ切り替えメニューなど）
st.sidebar.title("メニュー")
page = st.sidebar.radio("ページ", ["問い合わせ入力", "履歴一覧"])

if st.button("Тест хийх"):
    with st.spinner("Хариуг боловсруулж байна (3 секунд хүлээгээрэй)..."):
        time.sleep(3)  # Энд зориудаар 3 секунд хүлээлгэж байна (Удаан үйлдлийг дуурайлгаж байна)
    st.success("Амжилттай дууслаа!")