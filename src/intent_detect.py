
import re


def detect_intent(question):
    text = question.lower()
    tokens = set(re.findall(r"[a-z]+", text))

    if re.search(r"\bhow many\b|\bcount\b|\bnumber of\b", text):
        intent = "count"
    elif tokens.intersection({"average", "avg", "mean"}):
        intent = "average"
    elif tokens.intersection({"maximum", "highest", "largest", "most"}):
        intent = "maximum"
    elif tokens.intersection({"minimum", "lowest", "smallest", "least"}):
        intent = "minimum"
    elif tokens.intersection({"show", "list", "find", "display", "get"}):
        intent = "list"
    else:
        intent = "unknown"

    if "incidents" in tokens or "incident" in tokens:
        entity = "incidents"
    elif "people" in tokens or "person" in tokens or "individuals" in tokens:
        entity = "people"
    else:
        entity = "unknown"

    filters = []

    if tokens.intersection({"injured", "injuries", "wounded"}):
        filters.append({"column": "injured", "operator": ">", "value": 0})

    if tokens.intersection({"killed", "deaths", "fatalities"}):
        filters.append({"column": "killed", "operator": ">", "value": 0})

    country_match = re.search(r"\bin\s+([A-Z][a-zA-Z-]*)\b", question)
    if country_match:
        filters.append({
            "column": "country",
            "operator": "=",
            "value": country_match.group(1)
        })

    return {
        "intent": intent,
        "entity": entity,
        "filters": filters,
    }


if __name__ == "__main__":
    examples = [
        "How many people were involved in incidents in India?",
        "Show the names of people who were injured in India.",
        "Find incidents where people were killed.",
        "List people in India.",
    ]

    for question in examples:
        print(question)
        print(detect_intent(question))
        print()
