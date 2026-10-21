import json

from src.generate_candidates import generate_candidates
from src.ambiguity_engine import detect_candidate_ambiguity


def detect_ambiguity(question, db_id):
    question_lower = question.lower()

    is_count_question = (
        "how many" in question_lower
        and "people" in question_lower
        and "incident" in question_lower
        and "india" in question_lower
    )

    if is_count_question and db_id == "perpetrator":
        candidates = [
            {
                "id": 1,
                "meaning": "Count unique people",
                "sql": '''
SELECT COUNT(DISTINCT "people"."people id")
FROM "people"
JOIN "perpetrator"
  ON "people"."people id" = "perpetrator"."people id"
WHERE "perpetrator"."country" = 'India';
'''.strip()
            },
            {
                "id": 2,
                "meaning": "Count incident records",
                "sql": '''
SELECT COUNT(*)
FROM "perpetrator"
WHERE "country" = 'India';
'''.strip()
            }
        ]

        # Let the ambiguity engine compare the candidates.
        result = detect_candidate_ambiguity(candidates)
        result["question"] = question
        return result

    # For other supported questions, use the existing SQL generator.
    result = generate_candidates(question, db_id)

    if "candidate_sql" not in result:
        return {
            "question": question,
            "status": "unsupported",
            "details": result
        }

    return {
        "question": question,
        "is_ambiguous": False,
        "candidate_sql": result["candidate_sql"],
        "status": "No ambiguity detected by current rules"
    }


if __name__ == "__main__":
    question = "How many people were involved in incidents in India?"

    result = detect_ambiguity(question, "perpetrator")
    print(json.dumps(result, indent=4))
