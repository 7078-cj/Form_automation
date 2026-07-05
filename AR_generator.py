import json
from datetime import datetime
from pathlib import Path
import json

from utils.lib import (
    format_period,
    generate_activity_report_objectives
)

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "data/AR.json"
competition_FILE = BASE_DIR / "data/competition.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(competition_FILE, "r", encoding="utf-8") as c:
    competition_json = json.load(c)

print(data)

competition = competition_json

print(competition)

res = generate_activity_report_objectives(competition)

today = datetime.today().strftime("%B %d, %Y")

report = {
    "club_name": "Association of ICT Majors",
    "prepared_by": "Ceejay Santos",
    "position": "VP for External Affairs",

    "activity_title": competition["competition"]["title"],
    "venue": competition["competition"]["venue"],

    "activity_date": format_period(
        competition["competition"]["start_date"],
        competition["competition"]["end_date"]
    ),

    "report_period": format_period(
        competition["competition"]["start_date"],
        competition["competition"]["end_date"]
    ),

    "date_prepared": today,
    "date_submitted": today,

    
    "objectives": res["result"]["objectives"],

    "participants": competition["participants"],
    "issues": data["issues"],
    "recommendations": data["recommendations"]
}

print(json.dumps(report, indent=4, ensure_ascii=False))