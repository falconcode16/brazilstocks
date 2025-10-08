import yfinance as yf
import pandas as pd
from typing import List, Optional


class B3Data:
    """
    A class to fetch and process B3 stock data using yfinance.
    """

    def __init__(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ):
        """
        Initializes the B3Data class.
        Args:
            start_date (str, optional): The start date for fetching data
                in 'YYYY-MM-DD' format. Defaults to None.
            end_date (str, optional): The end date for fetching data in
                'YYYY-MM-DD' format. Defaults to None.
        """
        self.start_date = start_date
        self.end_date = end_date

    def get_stock_data(
        self,
        tickers: List[str],
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetches historical data for a list of stock tickers.
        Args:
            tickers (List[str]): A list of stock tickers
                (e.g., ['PETR4.SA', 'VALE3.SA']).
            period (str, optional): The period to fetch data for (e.g., '1d',
                '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd',
                'max'). Defaults to "1y".
            interval (str, optional): The data interval (e.g., '1m', '2m',
                '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk',
                '1mo', '3mo'). Defaults to "1d".
        Returns:
            pd.DataFrame: A DataFrame containing the historical data for the
                given tickers.
        """
        if not isinstance(tickers, list) or not all(
            isinstance(ticker, str) for ticker in tickers
        ):
            raise ValueError("Tickers must be a list of strings.")

        try:
            data = yf.download(
                tickers,
                period=period,
                interval=interval,
                start=self.start_date,
                end=self.end_date
            )
            if data.empty:
                return pd.DataFrame()

            # Restructure dataframe for better readability
            data.columns = data.columns.swaplevel(0, 1)
            data.sort_index(axis=1, level=0, inplace=True)

            return data
        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def calculate_technical_indicators(
        self, data: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculates technical indicators for the given stock data.
        Args:
            data (pd.DataFrame): A DataFrame with stock data,
                multi-indexed by ticker.
        Returns:
            pd.DataFrame: A DataFrame with the technical indicators.
        """
        if data.empty:
            return pd.DataFrame()

        df_with_indicators = data.copy()

        # Example: Calculate SMA for each stock
        for ticker in df_with_indicators.columns.levels[0]:
            df_with_indicators[(ticker, 'SMA_20')] = (
                df_with_indicators[(ticker, 'Close')]
                .rolling(window=20)
                .mean()
            )

        return df_with_indicators
