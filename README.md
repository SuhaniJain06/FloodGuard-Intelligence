# 🌊 FloodGuard Intelligence

## AI-Powered Multi-Modal Flood Emergency Intelligence Backend

FloodGuard Intelligence is an AI-powered backend system designed to support faster and more informed decision-making during flood emergencies.

The system combines **environmental sensor data, drone/aerial imagery, and emergency SOS messages** to identify flood risk, detect affected people, extract critical information from SOS messages, and calculate an overall emergency priority.

> **Current scope:** Backend implementation of Features 1–4.  
> Frontend/dashboard integration is planned as the next stage.

---

## 🚨 Overview

Flood emergencies generate information from multiple sources:

- 🌧️ Environmental and geographical sensor data
- 🚁 Drone/aerial imagery
- 📱 Emergency SOS messages
- 📍 Location information

Individually, these sources provide only partial information.

FloodGuard Intelligence combines these sources into a unified multi-modal emergency intelligence pipeline.

```text
Environmental Data
        │
        ▼
┌─────────────────────┐
│      Feature 1      │
│    Flood Risk AI    │
└──────────┬──────────┘
           │
           │ Flood Severity
           │
           ▼
┌─────────────────────┐
│      Feature 4      │◄──────────────┐
│  Priority Engine    │               │
└──────────┬──────────┘               │
           │                          │
           │ Priority + Actions       │
           │                          │
           │                  ┌───────┴────────┐
           │                  │                │
           │           Feature 2         Feature 3
           │           Drone AI           SOS AI
           │                │                │
           │                │                │
           │           Person Count    Structured SOS
           │                │                │
           └────────────────┴────────────────┘

Features
1️⃣ Feature 1 — Flood Risk Prediction

Feature 1 predicts flood severity using environmental and geographical parameters.

Input Parameters
Parameter	Description
water_level_cm	Current water level in centimeters
water_level_rate_cm_per_min	Rate at which the water level is rising
rainfall_mm_per_hr	Rainfall intensity
soil_moisture_pct	Soil moisture percentage
elevation_m	Elevation of the affected location
Risk Classes

The model predicts one of four risk levels:

LOW
MEDIUM
HIGH
CRITICAL
Output

Feature 1 returns:

Risk class
Risk label
Prediction confidence
Model Files
feature1_flood_risk/
├── best_flood_risk_model.joblib
├── feature_names.joblib
├── label_mapping.joblib
├── flood_risk.py
└── test_feature1.py
Example
Water level: 130.0 cm
Water level rate: 15.0 cm/min
Rainfall: 250.0 mm/hr
Soil moisture: 90.0 %
Elevation: 10.0 m

Risk: CRITICAL
Confidence: 1.0
2️⃣ Feature 2 — Drone Person Detection

Feature 2 processes aerial/drone imagery to detect people in flood-affected areas.

The system uses a custom YOLO-based person detection model.

Capabilities
Aerial image processing
Tiled inference
Overlapping tiles
Person-only detection
Confidence filtering
Non-Maximum Suppression (NMS)
Bounding-box visualization
Total person counting
Model
floodguard_person_v2.pt
Example Output
Feature 2 detected people: 12

The detector also produces an annotated image showing detected people and confidence scores.

Feature 2 Structure
feature2_drone/
├── feature2_detector.py
├── floodguard_person_v2.pt
├── test_feature2.py
├── test_img2.jpg
└── FloodGuard_Person_Model_Documentation.docx
3️⃣ Feature 3 — SOS Intelligence

Feature 3 converts unstructured emergency SOS messages into structured emergency information.

It uses Lyzr-based LLM processing to extract actionable information from emergency messages.

Example Input
20-30 people are stuck with no contact for the last
3 days near Maramon, Thottapuzha. They urgently need
food, water and rescue. Contact 9876543210.
Information Extracted

Feature 3 can extract:

Source type
Location
Number of people
Children
Elderly people
Pregnant people
Injured people
Missing people
Mobility-impaired people
Current situation
Requested resources
Food requirement
Water requirement
Medicine requirement
Shelter requirement
Rescue requirement
Medical transfer requirement
Contact information
Example Structured Output
{
  "source_type": "GROUP_SOS",
  "location": {
    "text": "near Maramon, Thottapuzha",
    "latitude": null,
    "longitude": null
  },
  "people": {
    "total": "20-30",
    "children": null,
    "elderly": null,
    "pregnant": null,
    "injured": null,
    "missing": null,
    "deceased": null,
    "mobility_impaired": null
  },
  "situation": "20-30 people are stuck with no contact for the last 3 days near Maramon, Thottapuzha.",
  "request": {
    "type": "RESCUE",
    "resources": [
      "FOOD",
      "WATER",
      "RESCUE"
    ]
  },
  "needs": {
    "food": true,
    "water": true,
    "medicine": false,
    "shelter": false,
    "rescue": true,
    "medical_transfer": false
  },
  "contact_info": [
    "9876543210"
  ]
}
4️⃣ Feature 4 — Multi-Modal Emergency Priority

Feature 4 combines the outputs of Features 1, 2, and 3 to determine the overall urgency of an emergency incident.

Instead of relying on a single source, the priority engine considers multiple signals.

Inputs
Feature 1
    ↓
Flood severity

Feature 2
    ↓
Detected people

Feature 3
    ↓
Structured SOS information
Priority Factors

Feature 4 considers:

Number of affected people
Vulnerability indicators
Emergency needs
Requested resources
Request type
Flood severity
Location information
Output

Feature 4 produces:

Overall priority
Priority score
Score breakdown
Recommended emergency actions
Example
FEATURE 4 RESULT

Priority: CRITICAL
Priority Score: 76

Score Breakdown:
  people_score: 10
  vulnerability_score: 0
  needs_score: 29
  request_score: 10
  flood_score: 25
  location_score: 2

Recommended Actions:
  - RESCUE
  - WATER_SUPPLY
  - FOOD_SUPPLY
🔗 Multi-Modal Integration

The current backend successfully connects Features 1–4.

                    FLOODGUARD INTELLIGENCE
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
 Environmental          Drone Image          SOS Message
     Data                    │                    │
        │                    │                    │
        ▼                    ▼                    ▼
 ┌──────────────┐     ┌──────────────┐    ┌──────────────┐
 │  Feature 1   │     │  Feature 2   │    │  Feature 3   │
 │ Flood Risk   │     │ Person       │    │ SOS          │
 │ Prediction   │     │ Detection    │    │ Intelligence  │
 └──────┬───────┘     └──────┬───────┘    └──────┬───────┘
        │                    │                    │
        │ Flood Severity     │ People Count      │ SOS Data
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Feature 4    │
                    │ Priority Engine │
                    └────────┬────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │ Emergency Priority   │
                  │ + Recommended Actions│
                  └──────────────────────┘
📂 Repository Structure
FloodGuard-Intelligence/
│
├── feature1_flood_risk/
│   ├── best_flood_risk_model.joblib
│   ├── feature_names.joblib
│   ├── label_mapping.joblib
│   ├── flood_risk.py
│   └── test_feature1.py
│
├── feature2_drone/
│   ├── feature2_detector.py
│   ├── floodguard_person_v2.pt
│   ├── test_feature2.py
│   ├── test_img2.jpg
│   └── FloodGuard_Person_Model_Documentation.docx
│
├── feature3_sos/
│   ├── extractor_llm.py
│   ├── extraction_results_v2.json
│   └── .env
│
├── feature4_priority/
│   ├── priority_engine.py
│   ├── run_feature4.py
│   ├── test_priority.py
│   ├── benchmark_feature4.py
│   └── ...
│
├── .gitignore
└── README.md

Note: .env is used locally for API credentials and should never be committed to the repository.

⚙️ Requirements
Software
Python 3.9+
Git
pip
Main Python Libraries
torch
torchvision
ultralytics
opencv-python
numpy
pandas
joblib

Feature 3 additionally requires the Lyzr dependencies used by extractor_llm.py.

A CUDA-enabled GPU is optional.

Feature 2 automatically falls back to CPU when CUDA is unavailable.

🚀 Installation
1. Clone the Repository
git clone https://github.com/SuhaniJain06/FloodGuard-Intelligence.git

Enter the repository:

cd FloodGuard-Intelligence
2. Create a Virtual Environment
Windows
python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1
Linux / macOS
python3 -m venv venv

Activate it:

source venv/bin/activate
3. Install Dependencies
pip install torch torchvision
pip install ultralytics
pip install opencv-python
pip install numpy pandas joblib

Install the Lyzr dependencies required by Feature 3 according to the Lyzr configuration being used.

▶️ Running Feature 1

Navigate to the Feature 1 directory:

cd feature1_flood_risk

Run the Feature 1 test:

python test_feature1.py

The test evaluates multiple flood conditions, including:

Normal conditions
Rising water
Heavy rainfall
Extreme flood conditions
Boundary values

Example:

Risk label: CRITICAL
Confidence: 1.0
▶️ Running Feature 2

Navigate to Feature 2:

cd feature2_drone

Run:

python test_feature2.py

The detector loads:

floodguard_person_v2.pt

and processes:

test_img2.jpg

The result includes:

Detected person count
Bounding boxes
Detection confidence
Annotated output image
▶️ Running Feature 3

Feature 3 uses Lyzr for live SOS extraction.

Create a local .env file inside:

feature3_sos/

Add:

LYZR_API_KEY=your_api_key_here

Then run the Feature 3 extraction script used by the project.

Security

Never commit your .env file or API key to GitHub.

The repository .gitignore excludes environment files.

▶️ Running Feature 4

Feature 4 integrates Features 1, 2, and 3.

Navigate to:

cd feature4_priority

Run:

python run_feature4.py

The pipeline performs:

1. Process SOS message using Feature 3
2. Detect people from drone imagery using Feature 2
3. Predict flood risk using Feature 1
4. Convert flood risk into severity
5. Combine information from all features
6. Calculate emergency priority
7. Generate recommended response actions
🔄 Feature 4 Testing Modes

Inside:

feature4_priority/run_feature4.py

the following configuration controls SOS processing:

USE_LIVE_LYZR = True
Live Lyzr Mode
USE_LIVE_LYZR = True

Uses Lyzr to process the SOS message in real time.

An active LYZR_API_KEY is required.

Dataset Mode
USE_LIVE_LYZR = False

Uses previously extracted Feature 3 data from:

feature3_sos/extraction_results_v2.json

This mode is useful for testing without making a live Lyzr request.

🧪 End-to-End Example

A demonstration SOS message:

20-30 people are stuck with no contact for the last
3 days near Maramon, Thottapuzha. They urgently need
food, water and rescue. Contact 9876543210.
Feature 3
People reported: 20-30
Location: Maramon, Thottapuzha
Needs: Food, Water, Rescue
Feature 2
Detected people: 12
Feature 1

Example sensor values:

Water level: 130.0 cm
Water level rate: 15.0 cm/min
Rainfall: 250.0 mm/hr
Soil moisture: 90.0 %
Elevation: 10.0 m

Prediction:

Risk: CRITICAL
Confidence: 1.0
Feature 4
Effective people: 25

Priority: CRITICAL
Priority Score: 76

Recommended actions:

RESCUE
WATER_SUPPLY
FOOD_SUPPLY
🧠 How Feature 4 Uses Multi-Modal Information

Feature 4 does not depend solely on the number of people reported in an SOS message.

For example:

Feature 3
20-30 people reported
        │
        ▼
Feature 4 converts range to an
effective numerical estimate
        │
        │
Feature 2
12 people detected in drone image
        │
        ▼
Feature 4 compares the available
people estimates
        │
        ▼
Effective people = 25

At the same time, Feature 1 contributes environmental severity:

Feature 1
     │
     ▼
CRITICAL flood risk
     │
     ▼
Flood severity = 1.0

These signals are combined by Feature 4 to produce a unified emergency priority.

🖥️ Current Scope

The current repository contains the backend intelligence layer for Features 1–4.

Currently implemented:

✅ Feature 1 — Flood Risk Prediction
✅ Feature 2 — Drone Person Detection
✅ Feature 3 — SOS Intelligence
✅ Feature 4 — Multi-Modal Emergency Priority

The frontend/dashboard is planned as the next integration layer.

🔮 Future Integration

The backend is designed to be connected to a centralized emergency-response dashboard.

Future integration can provide:

🌧️ Live Sensor Inputs

Real-time environmental sensor values can be sent to Feature 1.

🚁 Live Drone Processing

Incoming aerial imagery can be processed automatically by Feature 2.

📱 Live SOS Processing

Incoming emergency messages can be processed by Feature 3.

🧠 Unified Emergency API

Features 1–4 can be exposed through a common API for frontend consumption.

🖥️ Emergency Dashboard

The frontend can display:

Flood risk
Sensor values
Drone detections
Number of affected people
SOS information
Emergency location
Priority level
Priority score
Recommended actions
🔐 Security

API keys and other secrets must never be committed to version control.

Use environment variables for credentials.

Example:

LYZR_API_KEY=your_api_key_here

The .gitignore file excludes:

.env
.env.*
__pycache__/
*.pyc
💻 CPU / GPU Support

Feature 2 automatically checks whether CUDA is available.

If a compatible GPU is available:

Device: GPU

Otherwise:

Device: CPU

Feature 1 can run on standard CPU systems.

📊 Design Philosophy

FloodGuard Intelligence follows a multi-modal decision-support approach.

Instead of relying on a single source:

Sensor Data
     +
Drone Intelligence
     +
SOS Intelligence
     ↓
Unified Emergency Priority

This allows emergency situations to be evaluated using both:

Environmental severity
Human impact

The objective is to help emergency responders identify situations requiring immediate attention and recommend appropriate response actions.

🌊 FloodGuard Intelligence
Detect. Understand. Prioritize. Respond.

An AI-driven approach to intelligent flood emergency management.
