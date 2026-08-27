from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_sos():
    data = {
        "incident_id": "TEST_001",
        "source_type": "INDIVIDUAL_SOS",

        "location": {
            "text": "Kerala",
            "latitude": None,
            "longitude": None
        },

        "people": {
            "total": "4",
            "children": None,
            "elderly": None,
            "pregnant": "1",
            "injured": None,
            "missing": None,
            "mobility_impaired": None
        },

        "situation": "Flooded house",

        "request": {
            "type": "RESCUE",
            "resources": ["BOAT"]
        },

        "needs": {
            "food": False,
            "water": True,
            "medicine": True,
            "shelter": False,
            "rescue": True,
            "medical_transfer": False
        },

        "contact_info": [],

        "original_message": "4 people trapped in flooded house. Need a boat."
    }

    response = client.post("/extract-sos", json=data)

    assert response.status_code == 200