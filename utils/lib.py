from datetime import datetime
from utils.generate import generate


def format_date(date_str):
    """
    Converts YYYY-MM-DD to 'July 1, 2026'
    """
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %-d, %Y")


def format_period(start_date, end_date):
    """
    Converts:
    2026-07-01
    2026-07-03

    into

    July 1-3, 2026
    """

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start.month == end.month and start.year == end.year:
        return f"{start.strftime('%B')} {start.day}-{end.day}, {start.year}"

    return f"{format_date(start_date)} - {format_date(end_date)}"

def generate_activity_report_objectives(details):
    """
    Generates objectives.
    """

    prompt = f"""
You are writing an academic activity report.

Competition Information

Title:
{details['competition']['title']}

Description:
{details['competition']['description']}

Venue:
{details['competition']['venue']}

Duration:
{format_period(details['competition']['start_date'], details['competition']['end_date'])}

Generate ONLY valid JSON.

Schema:

{{
    "objectives":[
        "...",
        "...",
        "...",
        "..."
    ]
}}

Rules:

- Write exactly four objectives.
- Objectives should begin with action verbs such as:
    - To expose
    - To enhance
    - To develop
    - To broaden
- Return JSON only.
"""

    return generate(prompt)

def generate_request_letter_content(details):
    prompt = f"""
You are writing the body of a formal request letter for a college administrator.

Competition Information

Title:
{details['title']}

Description:
{details['description']}

Organizer:
{details['organizer']}

Venue:
{details['venue']}

Duration:
{format_period(details['start_date'], details['end_date'])}

Return ONLY valid JSON.

Schema:

{{
    "purpose": "...",
    "participation": "..."
}}

Rules:

- Write professionally.
- Do not include greetings or closing remarks.
- Do not mention names of recipients.
- Use third-person institutional language.
- The introduction should explain the request for approval.
- The purpose should explain how the competition benefits students academically and professionally.
- The participation section should describe how the students will participate based on the competition description.
- If the competition is onsite, mention onsite participation.
- If the competition is online, mention the official online platform if provided.
- Return JSON only.
"""

    return generate(prompt)
