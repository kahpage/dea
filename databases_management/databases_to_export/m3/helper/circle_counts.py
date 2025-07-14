from pathlib import Path
import json

with Path(__file__).with_name("m3.json").open("r", encoding="utf-8") as f:
    content = json.load(f)

events = content["events"]

for event in events:
    if "circles" in event:
        print(f'{event["aliases"]}: {len(event["circles"])} circles')
    else:
        print(f'{event["aliases"]}: NO circles')