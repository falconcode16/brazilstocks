from __future__ import annotations
from typing import Iterable, List, Union
import pandas as pd
import yfinance as yf
import pandas_ta as ta

_COLMAP = {"Open": "open", "High": "high", "Low": "low", "Close": "close", "Volume": "volume"}

class B3Data:
    def _norm(self, t: str) -> str:
        t = t.strip().upper()
        return t if t.endswith(".SA") else f"{t}.SA"

    def get_stock_data(
        self,
        ticker_list: Union[str, Iterable[str]],
        period: str = "1y",
        interval: str = "1d",
        auto_adjust: bool = True,
    ) -> pd.DataFrame:
        """
        Return OHLCV for B3 tickers using yfinance.
        Columns: ['ticker','date','open','high','low','close','volume']
        """
        tickers = [ticker_list] if isinstance(ticker_list, str) else list(ticker_list)
        if not tickers:
            raise ValueError("ticker_list must not be empty")
        tickers = [self._norm(t) for t in tickers]

        frames: List[pd.DataFrame] = []
        for t in tickers:
            hist = yf.Ticker(t).history(period=period, interval=interval, auto_adjust=auto_adjust)
            if hist.empty:
                continue
            hist = hist.rename(columns=_COLMAP)
            keep = [c for c in ["open", "high", "low", "close", "volume"] if c in hist.columns]
            hist = hist[keep]
            hist["ticker"] = t
            hist = hist.reset_index().rename(columns={"Date": "date"})
            frames.append(hist)

        if not frames:
            return pd.DataFrame(columns=["ticker", "date", "open", "high", "low", "close", "volume"])

        df = pd.concat(frames, ignore_index=True)
        df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
        return self.calculate_indicators(df)

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates RSI and MACD for each ticker in the dataframe.
        """
        df = df.copy()
        df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
        
        indicator_frames = []
        for ticker in df["ticker"].unique():
            ticker_df = df[df["ticker"] == ticker].copy()
            rsi = ticker_df.ta.rsi(close="close", length=14)
            ticker_df['RSI_14'] = rsi
            macd = ticker_df.ta.macd(close="close", fast=12, slow=26, signal=9)
            ticker_df['MACD_12_26_9'] = macd['MACD_12_26_9']
            ticker_df['MACDh_12_26_9'] = macd['MACDh_12_26_9']
            ticker_df['MACDs_12_26_9'] = macd['MACDs_12_26_9']
            indicator_frames.append(ticker_df)
            
        return pd.concat(indicator_frames).reset_index(drop=True)

    def __init__(self):
        pass
