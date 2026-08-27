import re
import json

from extractor_v2 import extract_sos_v2


INPUT_FILE = "final_sos_candidates.txt"
OUTPUT_FILE = "extraction_results_v2.json"

def load_messages(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    pattern = re.compile(
        r"---\s*(\d+)\s*\|.*?---\n(.*?)(?=\n---\s*\d+\s*\||\Z)",
        re.S
    )

    messages = []

    for match in pattern.finditer(text):
        message_id = int(match.group(1))
        message = match.group(2).strip()

        if message:
            messages.append({
                "id": message_id,
                "message": message
            })

    return messages


messages = load_messages(INPUT_FILE)

print("Messages found:", len(messages))

results = []

for item in messages:

    extracted = extract_sos_v2(item["message"])

    results.append({
        "id": item["id"],
        "input": item["message"],
        "extracted": extracted
    })


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        results,
        f,
        indent=2,
        ensure_ascii=False
    )

print("Extraction completed.")
print("Saved:", OUTPUT_FILE)