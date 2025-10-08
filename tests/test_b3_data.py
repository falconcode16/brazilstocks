import pandas as pd
from src.data.b3_data import B3Data

def test_fetch_two_tickers():
    b3_data = B3Data()
    # Changed period to "2mo" to ensure enough data for MACD(26) calculation
    df = b3_data.get_stock_data(["PETR4","VALE3"], period="2mo", interval="1d")
    assert isinstance(df, pd.DataFrame)
    assert {"ticker","date"}.issubset(df.columns)
    assert {"PETR4.SA","VALE3.SA"}.issubset(set(df["ticker"].unique()))
    assert len(df) > 0
    assert "RSI_14" in df.columns
    assert "MACD_12_26_9" in df.columns
    assert "MACDh_12_26_9" in df.columns
    assert "MACDs_12_26_9" in df.columns