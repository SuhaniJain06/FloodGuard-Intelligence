from extractor_llm import extract_sos_llm
import json


message = """
almost 20-30 people stuck with no contact for last 3 days.
Thottapuzha cherry, maramon near Marthoma church Sunday school.
Need Food n Water n rescue.
Contact 9876543210.
"""


result = extract_sos_llm(message)

print(json.dumps(
    result,
    indent=2,
    ensure_ascii=False
))