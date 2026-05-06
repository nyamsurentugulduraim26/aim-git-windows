import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie

# --- Lottie дүрсийг интернэтээс татаж авах функц ---
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Минималист, цэвэрхэн Loading дүрсийн URL
LOTTIE_URL = "https://lottie.host/5a09e1f3-64ed-4c3f-9fa6-f06c2ba18db6/jKFT51PPyF.lottie"
lottie_loading = load_lottieurl(LOTTIE_URL)

st.title("AI 問い合わせ分類システム")

question = st.text_area("問い合わせ内容を入力してください:", height=150)

if st.button("APIに送信する"):
    if question:
        # 1. Бичлэг гарах "хоосон зай" (placeholder) үүсгэх
        placeholder = st.empty()
        
        # 2. Хариу хүлээх хугацаанд Lottie дүрс харуулах
        with placeholder.container():
            if lottie_loading:
                st_lottie(lottie_loading, height=150, key="loading")
            st.markdown("<p style='text-align: center; color: gray;'>AIが分析中です。少々お待ちください...</p>", unsafe_allow_html=True)
        
        try:
            # 3. Backend рүү хүсэлт илгээх (Хугацааг 60 секунд болгох)
            response = requests.post(
                "http://127.0.0.1:8001/analyze", 
                json={"question": question}, 
                timeout=60
            )
            
            # 4. Хариу амжилттай ирмэгц түр хүлээлгийн дүрсийг дэлгэцээс устгах
            placeholder.empty()
            
            if response.status_code == 200:
                result = response.json()
                
                # Үр дүнг дэлгэцэнд хэвлэх
                st.success(f"**カテゴリ:** {result['category']}")
                st.warning(f"**緊急度:** {result['priority']}")
                st.info(f"**回答案:**\n{result['answer']}")
            else:
                st.error("APIエラーが発生しました。")
                
        except requests.exceptions.Timeout:
            placeholder.empty()
            st.error("サーバーからの応答がタイムアウトしました。もう一度お試しください。")
        except Exception as e:
            placeholder.empty()
            st.error(f"接続エラー: {e}")
    else:
        st.warning("問い合わせ内容を入力してください。")