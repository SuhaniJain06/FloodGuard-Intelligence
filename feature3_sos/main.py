from fastapi import FastAPI
from schemas import SOSIncident
from extractor_llm import extract_sos_llm


app = FastAPI(title="FloodGuard SOS Extraction API")


@app.get("/")
def home():
    return {
        "status": "running",
        "service": "Feature 3 - SOS Intelligence"
    }


@app.post("/extract-sos")
def extract_sos_endpoint(message: str):

    extracted = extract_sos_llm(message)

    incident = SOSIncident(
        incident_id="INC_AUTO",
        source_type=extracted["source_type"],
        location=extracted["location"],
        people=extracted["people"],
        situation=extracted["situation"],
        request=extracted["request"],
        needs=extracted["needs"],
        contact_info=extracted["contact_info"],
        original_message=extracted["original_message"]
    )

    return {
        "status": "success",
        "incident": incident.model_dump()
    }