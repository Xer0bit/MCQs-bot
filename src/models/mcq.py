from pydantic import BaseModel
from typing import List

class MCQ(BaseModel):
    question: str
    question_type: str
    options: List[dict]
    correct_answers: List[int]
    explanation: str
    domain: str
