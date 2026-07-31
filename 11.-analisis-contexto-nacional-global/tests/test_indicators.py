import pandas as pd

def test_growth_rate():
    s = pd.Series([100.0, 110.0])
    assert round(s.pct_change().iloc[1] * 100, 6) == 10
