import streamlit as st
import requests
from streamlit_lottie import st_lottie

API_BASE_URL = "http://127.0.0.1:8001"
LOTTIE_URL = "https://assets5.lottiefiles.com/packages/lf20_t9gkkhz4.json"
TEST_PHRASES = [
    "--- 選択してください ---",
    "明日の朝、通院のため1時間ほど遅れて出社します。",
    "来週の月曜日から3日間、夏季休暇をいただきたいです。",
    "残業申請の承認フローがわかりません。教えてください。",
    "今年の年末調整の書類提出期限はいつまででしょうか？",
    "入館証（セキュリティカード）を紛失しました。どうすればいいですか？",
    "社用スマホを電車の中に置き忘れてしまいました。至急、回線の停止をお願いします。",
    "会議室のプロジェクターの電球が切れています。交換をお願いできますか？"
]

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def show_inquiry_page(lottie_loading):
    st.title("AI お問い合わせ分類システム")

    selected_phrase = st.selectbox("テスト用テンプレートを選択:", TEST_PHRASES)
    default_text = "" if selected_phrase == "--- 選択してください ---" else selected_phrase
    question = st.text_area("問い合わせ内容を入力してください:", value=default_text, height=150)

    if st.button("APIに送信する"):
        if not question:
            st.warning("問い合わせ内容を入力してください。")
            return 

        placeholder = st.empty()
        with placeholder.container():
            if lottie_loading:
                st_lottie(lottie_loading, height=150, key="loading")
            st.markdown("<p style='text-align: center; color: gray;'>AIが分析中です。少々お待ちください...</p>", unsafe_allow_html=True)
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/analyze", 
                json={"question": question}, 
                timeout=60
            )
            placeholder.empty()
            
            if response.status_code == 200:
                result = response.json()
                st.info(f"**回答案:**\n{result['answer']}")
            else:
                st.error("APIエラーが発生しました。")
                
        except requests.exceptions.Timeout:
            placeholder.empty()
            st.error("サーバーからの応答がタイムアウトしました。")
        except Exception as e:
            placeholder.empty()
            st.error(f"接続エラー: {e}")

def show_history_page():
    st.title("お問い合わせ履歴")
    try:
        history_response = requests.get(f"{API_BASE_URL}/history")
        if history_response.status_code == 200:
            history_data = history_response.json()
            
            if not history_data:
                st.info("履歴がまだありません。")
                return

            for item in reversed(history_data):
                with st.expander(f"{item.get('timestamp', 'N/A')} - {item.get('category', 'その他')}"):
                    st.write(f"**質問:** {item.get('question')}")
                    st.write(f"**緊急度:** {item.get('priority')}")
                    st.write(f"**回答案:** {item.get('answer')}")
        else:
            st.error("履歴の取得に失敗しました。")
    except Exception as e:
        st.error(f"履歴読み込みエラー: {e}")

lottie_loading = load_lottieurl(LOTTIE_URL)

st.sidebar.title("メニュー")
menu = st.sidebar.radio("項目を選択してください:", ["お問い合わせ", "過去の履歴"])

if menu == "お問い合わせ":
    show_inquiry_page(lottie_loading)
elif menu == "過去の履歴":
    show_history_page()