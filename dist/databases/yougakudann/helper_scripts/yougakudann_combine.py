"""
Small script to combine all json files
"""

import json
from pathlib import Path
from typing import Any

def is_int(txt: str) -> bool:
    """Returns whether input can be seen as int"""
    try:
        int(txt)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    exit() # Avoid using it
    combined_data: dict[int, Any] = {}
    for json_file in Path(__file__).parent.glob('*.json'):
        if not is_int(json_file.stem):
            continue # Keep only xx.json files
        event_num = int(json_file.stem)

        with open(json_file, "r", encoding="utf-8") as f:
            content = json.load(f) 

        combined_data = {**combined_data, **content} 
    
    with open(Path(__file__).parent / "yougakudann.json", "w+", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=4, ensure_ascii=False)
