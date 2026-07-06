from datetime import datetime
from docx import Document

from utils.generate import generate
from utils.lib import format_period


# ==========================================================
# Generic Helpers
# ==========================================================

def find_table_by_headers(doc: Document, expected_headers):
    """
    Find a table by matching its first-row headers.
    """
    expected = [h.strip().lower() for h in expected_headers]

    for table in doc.tables:
        if not table.rows:
            continue

        headers = [
            cell.text.strip().lower()
            for cell in table.rows[0].cells
        ]

        if headers == expected:
            return table

    raise ValueError(
        f"Could not find table with headers: {expected_headers}"
    )


def fill_table(doc: Document, headers, data, column_mapping):
    """
    Generic table filler.

    Parameters
    ----------
    headers : list[str]
        Header row used to locate the table.

    data : list[dict]
        Data to insert.

    column_mapping : list[str | None]
        Dictionary keys corresponding to each column.

        Example:
        [
            "Student_Full_Name",
            "Student ID Number",
            None,
            None
        ]

        None leaves the column blank.
    """

    table = find_table_by_headers(doc, headers)

    while len(table.rows) - 1 < len(data):
        table.add_row()

    for row_index, item in enumerate(data, start=1):
        for col_index, key in enumerate(column_mapping):

            value = ""

            if key is not None:
                value = str(item.get(key, ""))

            table.cell(row_index, col_index).text = value


# ==========================================================
# Participants
# ==========================================================

def fill_participants_table(doc: Document, participants):
    fill_table(
        doc,
        headers=[
            "Student Full Name",
            "Student ID Number",
            "Year & Section",
            "Emergency Contact Number"
        ],
        data=participants,
        column_mapping=[
            "Student_Full_Name",
            "Student ID Number",
            "Year & Section",
            "Emergency Contact Number"
        ]
    )


# ==========================================================
# Attendance
# ==========================================================

def fill_students_table(doc: Document, participants):
    fill_table(
        doc,
        headers=[
            "Student Name",
            "Time-In Signature (Departure)",
            "Time-Out Signature (Return)"
        ],
        data=participants,
        column_mapping=[
            "Student_Full_Name",
            None,
            None
        ]
    )


# ==========================================================
# Medical Information
# ==========================================================

def fill_medical_information_table(doc: Document, participants):
    fill_table(
        doc,
        headers=[
            "Student Name",
            "Blood Type",
            "Known Medical Allergies",
            "Chronic Conditions / Maintenance Meds"
        ],
        data=participants,
        column_mapping=[
            "Student_Full_Name",
            None,
            None,
            None
        ]
    )


# ==========================================================
# Itinerary
# ==========================================================

def fill_itinerary_table(doc: Document, itinerary):
    fill_table(
        doc,
        headers=[
            "Activity Segment / Itinerary Stop",
            "Target Curriculum Competency / LO",
            "Method of Evaluation / Assessment"
        ],
        data=itinerary,
        column_mapping=[
            "activity",
            "competency",
            "assessment"
        ]
    )


# ==========================================================
# Risk Assessment
# ==========================================================

def fill_risk_assessment_table(doc: Document, risks):
    fill_table(
        doc,
        headers=[
            "Identified Hazard Area",
            "Risk Level",
            "Preventative Protocol",
            "Emergency Contingency Strategy"
        ],
        data=risks,
        column_mapping=[
            "hazard",
            "risk_level",
            "preventative_protocol",
            "contingency_strategy"
        ]
    )


# ==========================================================
# AI Generation
# ==========================================================

def generate_itinerary(details):
    prompt = f"""
You are preparing an academic educational visit itinerary.

Competition Information

Title:
{details['title']}

Description:
{details['description']}

Venue:
{details['venue']}

Duration:
{format_period(details['start_date'], details['end_date'])}

Return ONLY valid JSON.

Schema:

{{
    "itinerary":[
        {{
            "activity":"...",
            "competency":"...",
            "assessment":"..."
        }}
    ]
}}

Rules:

- Generate between 3 and 6 activities.
- Activities should follow the chronological flow.
- First activity should be registration/orientation.
- Last activity should be closing, awarding, or reflection.
- Competencies should be measurable.
- Assessments should be realistic.
"""

    return generate(prompt)


def generate_risk_assessment(details):
    prompt = f"""
You are preparing a Risk Assessment Matrix.

Competition Information

Title:
{details['title']}

Description:
{details['description']}

Venue:
{details['venue']}

Duration:
{format_period(details['start_date'], details['end_date'])}

Return ONLY valid JSON.

Schema:

{{
    "risks":[
        {{
            "hazard":"...",
            "risk_level":"...",
            "preventative_protocol":"...",
            "contingency_strategy":"..."
        }}
    ]
}}

Rules:

- Generate between 3 and 6 risks.
- Risk Level must be Low, Moderate, High,
  Low / Moderate or Moderate / High.
- Keep each field concise.
"""

    return generate(prompt)


def generate_executive_summary(details):
    prompt = f"""
You are preparing an Executive Summary and Operational Justification.

Competition Information

Title:
{details['title']}

Description:
{details['description']}

Venue:
{details['venue']}

Duration:
{format_period(details['start_date'], details['end_date'])}

Return ONLY valid JSON.

Schema:

{{
    "executive_summary":"..."
}}

Rules:

- One professional paragraph.
- Explain the activity.
- Explain learning outcomes.
- Explain academic relevance.
- Mention supervision.
- Mention risk mitigation.
"""

    return generate(prompt)