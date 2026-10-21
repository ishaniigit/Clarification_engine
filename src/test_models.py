
from models import QuestionRequest, SQLCandidate

request = QuestionRequest(
    question="How many people were involved in incidents in India?",
    db_id="perpetrator"
)

candidate = SQLCandidate(
    id=1,
    meaning="Count unique people",
    sql='SELECT COUNT(DISTINCT "people id") FROM "people";'
)

print(request.model_dump())
print(candidate.model_dump())
