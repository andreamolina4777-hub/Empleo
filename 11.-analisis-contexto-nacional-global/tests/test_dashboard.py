import json
from pathlib import Path

def test_demo_json_is_valid():
    path = Path(__file__).parents[1] / "public/data/indicators.json"
    assert isinstance(json.loads(path.read_text(encoding="utf-8")), list)
