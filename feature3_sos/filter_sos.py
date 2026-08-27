from datasets import load_dataset
import re

dataset = load_dataset(
    "QCRI/HumAID-all",
    verification_mode="no_checks"
)

train = dataset["train"]

# Only SOS/request messages
requests = [
    row["tweet_text"]
    for row in train
    if row["class_label"] == "requests_or_urgent_needs"
]

# Information we care about extracting
patterns = {
    "people": r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(people|persons|famil(y|ies)|members|children|kids|adults)\b",
    "injured": r"\b(injur(ed|y)|hurt|wounded|bleeding|ambulance|medical)\b",
    "children": r"\b(child|children|kid|kids|baby|babies|infant)\b",
    "elderly": r"\b(elderly|old|grandmother|grandfather|grandma|grandpa|senior)\b",
    "pregnant": r"\b(pregnant|pregnancy)\b",
    "trapped": r"\b(trapped|stranded|stuck|marooned|surrounded)\b",
    "water": r"\b(water|drinking water|clean water|flood(ed|ing)?)\b",
    "food": r"\b(food|meal|meals|hungry|ration|groceries)\b",
    "medicine": r"\b(medicine|medicines|medication|medical|pharmacy|hospital)\b",
    "rescue": r"\b(rescue|save|evacuate|evacuation|boat|help us)\b",
    "shelter": r"\b(shelter|tent|temporary housing|homeless)\b",
    "location": r"\b(in|at|near|from)\s+[A-Z][A-Za-z-]+",
    "coordinates": r"\b(lat(itude)?|long(itude)?|gps|coordinates?)\b"
}

def information_score(text):
    text_lower = text.lower()
    found = []

    for category, pattern in patterns.items():
        if re.search(pattern, text_lower):
            found.append(category)

    return len(found), found


# Score every request
scored = []

for text in requests:
    score, found = information_score(text)
    scored.append((score, found, text))


# Highest-information messages first
scored.sort(reverse=True, key=lambda x: x[0])


print("Total request messages:", len(requests))
print("\nTop 100 information-rich messages:\n")

for i, (score, found, text) in enumerate(scored[:100], 1):
    print(f"\n--- {i} | SCORE: {score} | FOUND: {found} ---")
    print(text)


# Save them
with open("filtered_sos_messages.txt", "w", encoding="utf-8") as f:
    for i, (score, found, text) in enumerate(scored[:500], 1):
        f.write(f"\n--- {i} | SCORE: {score} | FOUND: {found} ---\n")
        f.write(text + "\n")

print("\nSaved top 500 to filtered_sos_messages.txt")