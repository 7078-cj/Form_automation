import json
from pathlib import Path
from datetime import datetime

from utils.lib import (
    format_period,
    generate_request_letter_content
)

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "data" / "competition.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

competition = data["competition"]

ai = generate_request_letter_content(competition)

today = datetime.today().strftime("%B %d, %Y")

letter = {
    "date": today,

    "subject": f"Request for Approval to Conduct Participation in the {competition['title']}",

    "competition_title": competition["title"],
    "venue": competition["venue"],
    "duration": format_period(
        competition["start_date"],
        competition["end_date"]
    ),

    "purpose": ai["result"]["purpose"],
    "participation": ai["result"]["participation"],

    "participants": data["participants"],

}

print(json.dumps(letter, indent=4, ensure_ascii=False))