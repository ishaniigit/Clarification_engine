
from typing import Optional
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)
    db_id: str = Field(min_length=1)


class SQLCandidate(BaseModel):
    id: int
    meaning: str
    sql: str


class ClarificationResponse(BaseModel):
    question: str
    is_ambiguous: bool
    candidates: list[SQLCandidate] = Field(default_factory=list)
    clarification_question: Optional[str] = None


class ClarificationRequest(BaseModel):
    candidates: list[SQLCandidate]
    user_choice: int


class SQLResult(BaseModel):
    selected_meaning: str
    selected_sql: str
    rows: list[dict] = Field(default_factory=list)

class ClarificationChoice(BaseModel):
    question: str
    db_id: str
    user_choice: int
