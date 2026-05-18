from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import google.generativeai as genai
from dotenv import load_dotenv

from backend.storage import load_data, save_data

# =========================
# INIT
# =========================
app = FastAPI()
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


# =========================
# MODEL
# =========================
class InquiryRequest(BaseModel):
    question: str


# =========================
# GEMINI CALL
# =========================
def call_gemini(question: str):

    prompt = f"""
あなたは社内問い合わせAIです。

必ずJSONのみ返してください：

{{
  "category": "勤怠/休暇/給与/経費精算/社員情報変更/その他",
  "urgency": "高/中/低",
  "answer": "簡潔な回答"
}}

問い合わせ：
{question}
"""

    response = model.generate_content(prompt)
    return response.text


# =========================
# SAFE JSON PARSE
# =========================
import json

def parse_json(text: str):

    try:
        return json.loads(text)
    except:
        clean = text.replace("```json", "").replace("```", "")
        return json.loads(clean)


# =========================
# POST
# =========================
@app.post("/inquiries")
def create_inquiry(req: InquiryRequest):

    try:
        raw = call_gemini(req.question)
        result = parse_json(raw)

    except Exception:
        raise HTTPException(status_code=500, detail="Gemini Error")

    data = load_data()

    new_item = {
        "id": len(data) + 1,
        "created_at": datetime.now().isoformat(),
        "question": req.question,
        "category": result["category"],
        "urgency": result["urgency"],
        "answer": result["answer"]
    }

    data.append(new_item)
    save_data(data)

    return new_item


# =========================
# GET ALL
# =========================
@app.get("/inquiries")
def get_all():
    data = load_data()
    return sorted(data, key=lambda x: x["id"], reverse=True)


# =========================
# GET ONE
# =========================
@app.get("/inquiries/{id}")
def get_one(id: int):

    data = load_data()

    for item in data:
        if item["id"] == id:
            return item

    raise HTTPException(status_code=404, detail="Not found")