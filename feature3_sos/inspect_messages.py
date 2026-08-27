from datasets import load_dataset
import random

dataset = load_dataset(
    "QCRI/HumAID-all",
    verification_mode="no_checks"
)

train = dataset["train"]

useful_labels = [
    "requests_or_urgent_needs",
    "injured_or_dead_people",
    "displaced_people_and_evacuations",
    "missing_or_found_people",
    "rescue_volunteering_or_donation_effort"
]

messages = [
    row for row in train
    if row["class_label"] in useful_labels
]

print("Useful messages:", len(messages))

for i, row in enumerate(random.sample(messages, 50), 1):
    print(f"\n--- {i} ---")
    print("LABEL:", row["class_label"])
    print("TEXT :", row["tweet_text"])