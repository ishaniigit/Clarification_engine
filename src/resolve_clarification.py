
def resolve_clarification(candidates, user_choice):
    choice = str(user_choice).strip()

    for candidate in candidates:
        if str(candidate["id"]) == choice:
            return {
                "selected_meaning": candidate["meaning"],
                "selected_sql": candidate["sql"],
            }

    return {
        "error": "Invalid choice. Please select an available candidate ID."
    }
