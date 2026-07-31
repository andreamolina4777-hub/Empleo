import pandas as pd

def test_required_schema():
    df = pd.DataFrame([{"country": "Ecuador", "year": 2025, "indicator": "demo", "value": 1.0}])
    assert {"country", "year", "indicator", "value"}.issubset(df.columns)
