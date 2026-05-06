from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
import json
import re
from datetime import datetime

# 1. Тохиргоо болон Орчин
genai.configure(api_key=os.environ.get("OPENAI_API_KEY"))
app = FastAPI()

# Өгөгдөл хадгалах хавтас болон файлын зам
DATA_FOLDER = "data"
DB_FILE = os.path.join(DATA_FOLDER, "inquiries.json")

# Хавтас байхгүй бол үүсгэх
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

class InquiryRequest(BaseModel):
    question: str

CATEGORY_LIST = [
    "勤怠", "休暇", "給与", "年末調整", "社会保険", "福利厚生", 
    "交通費", "出張", "備品", "入退社手続き", "異動手続き", 
    "社員情報変更", "社内ルール", "証明書発行", "オフィス設備", 
    "安全衛生", "慶弔", "社内イベント", "郵送・宅配", 
    "セキュリティ", "個人情報", "その他"
]

# 2. Туслах функц: JSON хадгалах
def save_to_json(data):
    # Файл байхгүй бол хоосон жагсаалттай үүсгэх
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            items = json.load(f)
        except json.JSONDecodeError:
            items = []

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    items.append(data)

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

# 3. API Замууд
@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze_inquiry(request: InquiryRequest):
    categories_str = ", ".join(CATEGORY_LIST)
    prompt = f"""
    あなたは会社の総務部のAIアシスタントです。
    ユーザーからの問い合わせ内容を分析し、以下の要件に従って回答してください。

    【要件】
    1. カテゴリは必ず以下のリストから最も適切なものを1つ選択してください：
       [{categories_str}]
    2. 緊急度（priority）は「低」「中」「高」「緊急」の4段階から選択してください。
    3. 回案（answer）は、総務担当者として丁寧で親切な日本語で作成してください。
    4. 出力は必ず以下のJSON形式のみとし、他のテキストは含めないでください：
       {{
           "category": "選択したカテゴリ",
           "priority": "選択した緊急度",
           "answer": "作成した回答案"
       }}

    問い合わせ内容：
    {request.question}
    """

    try:
        # Gemini 1.5 Flash ашиглах (2.5 хувилбар байхгүй тул засварлав)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            ai_data = json.loads(json_match.group(0))
        else:
            ai_data = json.loads(response_text)

        result = {
            "question": request.question,
            "category": ai_data.get("category", "その他"),
            "priority": ai_data.get("priority", "低"),
            "answer": ai_data.get("answer", "AI回答の生成に失敗しました。")
        }

        # JSON файлд түүхийг хадгалах[cite: 1]
        save_to_json(result)

        return result

    except Exception as e:
        print(f"Error occurred during analysis: {e}")
        return {
            "question": request.question,
            "category": "エラー",
            "priority": "緊急",
            "answer": f"AI分析中にエラーが発生しました: {str(e)}"
        }

# Боломжит моделуудыг шалгах
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Боломжит модел: {m.name}")
except Exception as e:
    print(f"Could not list models: {e}")