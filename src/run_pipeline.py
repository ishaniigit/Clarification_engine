
from detect_ambiguity import detect_ambiguity
from resolve_clarification import resolve_clarification


question = "How many people were involved in incidents in India?"
db_id = "perpetrator"

result = detect_ambiguity(question, db_id)

if result.get("is_ambiguous"):
    print("\nYour question has multiple interpretations:")

    for candidate in result["options"]:
        print(f'{candidate["id"]}. {candidate["meaning"]}')

    print("\n" + result["clarification_question"])

    choice = input("Enter your choice: ")

    resolved = resolve_clarification(result["options"], choice)

    if "error" in resolved:
        print(resolved["error"])
    else:
        print("\nSelected interpretation:", resolved["selected_meaning"])
        print("\nSQL query:\n", resolved["selected_sql"])

elif "candidate_sql" in result:
    print("SQL query:\n", result["candidate_sql"])

else:
    print("Could not process question:", result)
