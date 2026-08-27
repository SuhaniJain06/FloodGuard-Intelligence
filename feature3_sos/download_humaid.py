from datasets import load_dataset

dataset = load_dataset(
    "QCRI/HumAID-all",
    verification_mode="no_checks"
)

print(dataset)
print(dataset["train"][0])