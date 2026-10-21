
import json


def detect_candidate_ambiguity(candidates):
    if len(candidates) < 2:
        return {
            "is_ambiguous": False,
            "reason": "Fewer than two candidates are available.",
            "clarification_question": None,
        }

    meanings = {}

    for candidate in candidates:
        meaning = candidate["meaning"].strip().lower()
        meanings.setdefault(meaning, []).append(candidate["id"])

    distinct_meanings = list(meanings.keys())

    if len(distinct_meanings) == 1:
        return {
            "is_ambiguous": False,
            "reason": "All candidates describe the same stated interpretation.",
            "clarification_question": None,
        }

    options = [
        candidates[i]["meaning"]
        for i in range(len(candidates))
    ]

    question = (
        "Which interpretation do you intend? "
        + " or ".join(options)
        + "?"
    )

    return {
        "is_ambiguous": True,
        "reason": "Candidates represent different stated interpretations.",
        "clarification_question": question,
        "options": candidates,
    }


if __name__ == "__main__":
    candidates = [
        {
            "id": 1,
            "meaning": "Count unique people",
            "sql": 'SELECT COUNT(DISTINCT "people"."people id") ...',
        },
        {
            "id": 2,
            "meaning": "Count incident records",
            "sql": 'SELECT COUNT(*) ...',
        },
    ]

    result = detect_candidate_ambiguity(candidates)
    print(json.dumps(result, indent=4))
