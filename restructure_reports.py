"""score_records.py creates a JSON file whose root object is a dictionary;
this is so that it is easily resumable (can check if an id exists in the keys).
But we want a simple list of reports, so this file just flattens flattened_reports.json"""

import json


with open("json/flattened_reports_tmp.json", "r") as file:
    reports = json.load(file)


new_reports = []

for k, v in reports.items():
    new_report = {
        "id": k,
        **v,
    }
    new_reports.append(new_report)

with open("json/reports.json", "w") as file:
    json.dump(new_reports, file, indent=2)
print(f"Flattened {len(new_reports)} reports from {len(reports)} records.")
