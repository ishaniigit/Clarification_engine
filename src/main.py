
from fastapi import FastAPI
from src.models import QuestionRequest
from src.detect_ambiguity import detect_ambiguity
from src.models import ClarificationChoice
from src.resolve_clarification import resolve_clarification

app = FastAPI(title="Text-to-SQL with Clarification Engine")


@app.get("/")
def home():
    return {
        "message": "Text to SQL with Clarification Engine API is running"
    }


@app.post("/question")
def process_question(request: QuestionRequest):
    result = detect_ambiguity(
        request.question,
        request.db_id
    )
    return result

@app.post("/clarification")
def clarify_question(request: ClarificationChoice):
    result = detect_ambiguity(
        request.question,
        request.db_id
    )

    if not result.get("is_ambiguous"):
        return {
            "error": "No clarification options are available.",
            "details": result
        }

    resolved = resolve_clarification(
        result["options"],
        request.user_choice
    )

    return resolved
