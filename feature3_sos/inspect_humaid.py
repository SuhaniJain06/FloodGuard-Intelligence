from datasets import load_dataset
from collections import Counter

dataset = load_dataset(
    "QCRI/HumAID-all",
    verification_mode="no_checks"
)

train = dataset["train"]

print("\nTotal:", len(train))

print("\nCategories:")
counts = Counter(train["class_label"])

for label, count in counts.most_common():
    print(f"{label}: {count}")