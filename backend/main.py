from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import google.generativeai as genai
import os
import json
import re

# Gemini API тохиргоо
genai.configure(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()

class InquiryRequest(BaseModel):
    question: str

# 1. Таны өгсөн Японы ерөнхий хэрэгцээний ангилал
CATEGORY_LIST = [
    "勤怠", "休暇", "給与", "年末調整", "社会保険", "福利厚生", 
    "交通費", "出張", "備品", "入退社手続き", "異動手続き", 
    "社員情報変更", "社内ルール", "証明書発行", "オフィス設備", 
    "安全衛生", "慶弔", "社内イベント", "郵送・宅配", 
    "セキュリティ", "個人情報", "その他"
]

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
async def analyze_inquiry(request: InquiryRequest):
    # 2. AI-д зориулсан зааварчилгаа (Prompt)
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
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # JSON хэсгийг шүүж авах
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
        else:
            data = json.loads(response_text)

        return {
            "category": data.get("category", "その他"),
            "priority": data.get("priority", "低"),
            "answer": data.get("answer", "AI回答の生成に失敗しました。")
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "category": "エラー",
            "priority": "緊急",
            "answer": f"エラーが発生しました: {str(e)}"
        }
      