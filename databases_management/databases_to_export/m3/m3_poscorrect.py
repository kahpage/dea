import json
from pathlib import Path

if False:
    with Path(__file__).with_name("m3-02.json").open("r", encoding="utf-8") as file:
        data = json.load(file)
    
    circles = data["circles"]
    for circle in circles:
        if "media" not in circle:
            circle["position"] = "@"
        else:
            circle["position"] = circle["media"][0]["path"].split("_")[-1].replace(".jpg", "")
            circle["position"] = circle["position"][0].upper() + circle["position"][1:] # Capitalize the first letter
    
    with Path(__file__).with_name("m3-02.json").open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
