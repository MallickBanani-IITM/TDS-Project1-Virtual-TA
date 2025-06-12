from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
import base64

from app.utils import get_answer_from_knowledge_base  # You'll create this

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "TDS Virtual TA is running!"}

# Input model
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64-encoded image (optional)

# Output model
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

@app.post("/api/", response_model=AnswerResponse)
def answer_question(req: QuestionRequest):
    try:
        answer, links = get_answer_from_knowledge_base(req.question, req.image)
        return AnswerResponse(answer=answer, links=links)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
