import re
from pathlib import Path

INPUT_FILE = "filtered_sos_messages.txt"
OUTPUT_FILE = "final_sos_candidates.txt"


# Strong signals that this is an actionable incident/request
POSITIVE_PATTERNS = {
    "people": r"\b\d+\s*(people|persons|families|members|adults|kids|children)\b",
    "stranded": r"\b(stranded|trapped|stuck|marooned|unable to evacuate|surrounded)\b",
    "urgent": r"\b(urgent|urgently|emergency|immediate|asap|immediately|help needed)\b",
    "request": r"\b(need|needs|required|required urgently|seeking|request|please help)\b",
    "food": r"\b(food|meal|meals|ration|hungry|starving)\b",
    "water": r"\b(water|drinking water|clean water)\b",
    "medicine": r"\b(medicine|medicines|medication|medical|oxygen|hospital|ambulance)\b",
    "rescue": r"\b(rescue|evacuat|boat|airlift|helicopter)\b",
    "vulnerable": r"\b(pregnant|pregnancy|baby|babies|infant|child|children|elderly|grandmother|grandfather|old people|disabled)\b",
    "location": r"\b(location|near|road|street|district|school|church|temple|hospital|camp|coordinates|gps)\b",
    "contact": r"\b(contact|phone|call|number)\b",
    "medical_emergency": r"\b(oxygen|critical|serious condition|injured|bleeding|sick|patient)\b",
}


# Things that strongly suggest this isn't an individual actionable report
NEGATIVE_PATTERNS = {
    "retweet": r"^\s*(rt|retweeted)\b",
    "donation": r"\b(donate|donation|donations|fundraising|fundraiser|financial aid|contribute)\b",
    "campaign": r"\b(campaign|appeal campaign|support our campaign)\b",
    "news": r"\b(news|breaking|report|reported|headline|article)\b",
    "general": r"\b(be prepared|learn how|remember to|awareness|in the aftermath)\b",
}


def score_message(text):
    text_lower = text.lower()

    positive = []
    negative = []

    for name, pattern in POSITIVE_PATTERNS.items():
        if re.search(pattern, text_lower):
            positive.append(name)

    for name, pattern in NEGATIVE_PATTERNS.items():
        if re.search(pattern, text_lower):
            negative.append(name)

    score = len(positive)

    # Strong bonus for actual emergency language
    if "stranded" in positive and "request" in positive:
        score += 3

    if "urgent" in positive and "request" in positive:
        score += 2

    if "location" in positive and "contact" in positive:
        score += 2

    if "medical_emergency" in positive:
        score += 2

    # Penalize obvious non-SOS content
    score -= len(negative) * 2

    return score, positive, negative


# Read messages
content = Path(INPUT_FILE).read_text(encoding="utf-8")

# Split our existing file into messages
blocks = re.split(r"\n--- \d+ \| SCORE:.*?---\n", content)

results = []

for block in blocks:
    block = block.strip()

    if not block:
        continue

    # Ignore accidental headers
    if len(block) < 20:
        continue

    score, positive, negative = score_message(block)

    results.append({
        "score": score,
        "positive": positive,
        "negative": negative,
        "text": block
    })


# Highest quality first
results.sort(key=lambda x: x["score"], reverse=True)

# Keep top candidates
final = results[:300]


with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    for i, item in enumerate(final, 1):

        f.write(
            f"\n--- {i} | SCORE: {item['score']} "
            f"| POSITIVE: {item['positive']} "
            f"| NEGATIVE: {item['negative']} ---\n"
        )

        f.write(item["text"] + "\n")


print("Original messages:", len(results))
print("Final candidates:", len(final))
print("Saved:", OUTPUT_FILE)