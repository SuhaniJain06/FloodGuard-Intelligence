from datasets import load_dataset

dataset = load_dataset(
    "QCRI/HumAID-all",
    verification_mode="no_checks"
)

train = dataset["train"]

requests = [
    row["tweet_text"]
    for row in train
    if row["class_label"] == "requests_or_urgent_needs"
]

print("Total request messages:", len(requests))

for i, text in enumerate(requests[:100], 1):
    print(f"\n--- {i} ---")
    print(text)