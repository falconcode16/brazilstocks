import pandas as pd
from src.data.b3_data import B3Data


def test_fetch_two_tickers():
    b3_data = B3Data()
    df = b3_data.get_stock_data(
        ["PETR4.SA", "VALE3.SA"], period="2mo", interval="1d"
    )
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns.levels[0]) == 2
