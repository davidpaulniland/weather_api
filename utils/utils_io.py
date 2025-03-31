import json
from pathlib import Path

DATA_PATH = Path("data/sensors.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]")

def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2, default=str)
