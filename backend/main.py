from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InquiryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):
    return {
        "category": "その他",
        "priority": "低",
        "answer": f"問い合わせ内容を受け付けました: {request.question}"
    }