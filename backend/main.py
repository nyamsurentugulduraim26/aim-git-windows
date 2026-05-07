import os
import json
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

app = FastAPI()

DATA_PATH = Path("data/inquiries.json")

class InquiryRequest(BaseModel):
    question: str

def load_inquiries():
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_inquiry(question, category, priority, answer):
    inquiries = load_inquiries()
    new_id = len(inquiries) + 1
    item = {
        "id": new_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": question,
        "category": category,
        "priority": priority,
        "answer": answer,
    }
    inquiries.append(item)
    DATA_PATH.parent.mkdir(exist_ok=True)
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(inquiries, f, ensure_ascii=False, indent=2)
    return item

def analyze_with_gemini(question: str) -> str:
    prompt = f"""
あなたは総務部門の問い合わせ一次回答担当です。
社員からの問い合わせを読み、以下の3点を日本語で返してください。

1. カテゴリ:
2. 緊急度:（高・中・低）
3. 回答案:

問い合わせ:
{question}
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/inquiries")
def get_inquiries():
    return load_inquiries()

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):
    gemini_response = analyze_with_gemini(request.question)
    
    item = save_inquiry(
        question=request.question,
        category="未分類", 
        priority="不明",   
        answer=gemini_response
    )
    
    return item