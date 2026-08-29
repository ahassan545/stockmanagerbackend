import yfinance as yf
from datetime import datetime, timedelta
import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)

class StockHistoricalDataService:
    def get_data(self, ticker: str, date: datetime, days: int):
        start=self.format_date(date - timedelta(days=days))
        end=self.format_date(date)
        cache_name = f"{ticker}_{start}_{end}.csv"
        data = self.get_cached_data(cache_name)
        if not data.empty:
            return data

        logger.info(f"Fetching stock data for ticker [{ticker}] from [{start}] to [{end}]")

        df = yf.download(ticker, start=start, end=end)
        df.columns = df.columns.droplevel('Ticker')

        logger.info(f"Fetched stock data for ticker [{ticker}] count [{df.count()}]")

        df.to_csv(cache_name)
        
        return df

    def get_cached_data(self, cache_name: str):
        if not os.path.exists(cache_name):
            return pd.DataFrame()

        return pd.read_csv(cache_name)



  
    def format_date(self, date: datetime):
        return date.strftime("%Y-%m-%d")