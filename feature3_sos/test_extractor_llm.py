import json
from pathlib import Path

from extractor_llm import extract_sos_llm


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
GOLDEN_FILE = BASE_DIR / "benchmark" / "golden_test.json"


# ---------------------------------------------------------
# LOAD GOLDEN TESTS
# ---------------------------------------------------------

with open(GOLDEN_FILE, "r", encoding="utf-8") as f:
    benchmark = json.load(f)

tests = benchmark["cases"]


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

print("=" * 80)
print("LLM SOS EXTRACTOR BENCHMARK")
print("=" * 80)

print(f"Total test cases: {len(tests)}")
print()


# ---------------------------------------------------------
# RUN TESTS
# ---------------------------------------------------------

passed = 0
failed = 0
errors = 0


for i, test in enumerate(tests, start=1):

    case_id = test["case_id"]
    message = test["message"]

    print("-" * 80)
    print(f"TEST {i}/{len(tests)}")
    print(f"CASE ID: {case_id}")
    print(f"MESSAGE: {message}")

    try:

        result = extract_sos_llm(message)

        print("\nLLM OUTPUT:")
        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

        if result:
            passed += 1
            print("\nSTATUS: OUTPUT RECEIVED")

    except NotImplementedError:

        print("\nSTATUS: LLM NOT CONNECTED YET")

        errors += 1

        print(
            "\nLyzr is not connected yet.\n"
            "Benchmark will run after extractor_llm.py "
            "is connected to an LLM."
        )

        break

    except Exception as e:

        errors += 1

        print("\nSTATUS: ERROR")
        print(f"ERROR: {e}")


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

print()
print("=" * 80)
print("BENCHMARK SUMMARY")
print("=" * 80)

print(f"Total tests : {len(tests)}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")
print(f"Errors      : {errors}")

if errors == 0:
    print("\nBenchmark completed.")

else:
    print("\nLLM benchmark is waiting for provider connection.")