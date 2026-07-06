import json
from pathlib import Path

from docx import Document

from utils.insert import replace_text
from utils.lib import format_period
from utils.compliance_form_libs import (
    fill_medical_information_table,
    fill_participants_table,
    fill_itinerary_table,
    fill_risk_assessment_table,
    generate_itinerary,
    generate_risk_assessment,
    generate_executive_summary,
    fill_students_table,
)

# ============================================
# Paths
# ============================================

BASE_DIR = Path(__file__).resolve().parent

COMPETITION_FILE = BASE_DIR / "data" / "competition.json"
COMPLIANCE_FILE = BASE_DIR / "data" / "Compliance_form.json"

TEMPLATE = BASE_DIR / "templates" / "Compliance_Form.docx"
OUTPUT = BASE_DIR / "output" / "Compliance_Form.docx"

# ============================================
# Load JSON
# ============================================

with open(COMPETITION_FILE, encoding="utf-8") as f:
    competition_json = json.load(f)

with open(COMPLIANCE_FILE, encoding="utf-8") as f:
    compliance = json.load(f)

competition = competition_json["competition"]
participants = compliance["participants"]

# ============================================
# Generate AI Content
# ============================================

itinerary_response = generate_itinerary(competition)
risk_response = generate_risk_assessment(competition)
executive_summary_response = generate_executive_summary(competition)

itinerary = itinerary_response["result"]["itinerary"]
risks = risk_response["result"]["risks"]
executive_summary = executive_summary_response["result"]["executive_summary"]

# ============================================
# Open Template
# ============================================

doc = Document(TEMPLATE)

# ============================================
# Replace Text Placeholders
# ============================================

replace_text(
    doc,
    {
        "activity_title": competition["title"],
        "schedule_dates": format_period(
            competition["start_date"],
            competition["end_date"]
        ),
        "venue": competition["venue"],
        "course_subject": "BS Information System",
        "faculty_in_charge": "Sir Gian Carlo Gallon",
        "executive_summary": executive_summary
    }
)

# ============================================
# Fill Tables
# ============================================

fill_participants_table(doc, participants)
fill_students_table(doc, participants)
fill_medical_information_table(doc, participants)

fill_itinerary_table(
    doc,
    itinerary
)

fill_risk_assessment_table(
    doc,
    risks
)


# ============================================
# Save
# ============================================

OUTPUT.parent.mkdir(exist_ok=True)

doc.save(OUTPUT)

print(f"Compliance form generated successfully!\n{OUTPUT}")