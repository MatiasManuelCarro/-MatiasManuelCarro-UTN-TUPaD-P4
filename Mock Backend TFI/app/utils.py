import json
from pathlib import Path

DATA_DIR = Path("data")

def load_json(name: str) -> list[dict[str, object]]:
    path = DATA_DIR / f"{name}.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(name: str, data: list[dict[str, object]]) -> None:
    path = DATA_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_by_id(data: list[dict[str, object]], obj_id: int) -> dict[str, object] | None:
    return next((item for item in data if item.get("id") == obj_id), None)
