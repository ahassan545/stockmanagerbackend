import finnhub
import os
import requests
from datetime import datetime, timedelta
from models.newsmodel import News
from agents import Agent, Runner, trace, function_tool
from agents.decorators import tool

class NewsService():
    def __init__(self):
        self.finnhub_client = finnhub.Client(api_key=os.environ.get("FINHUB_API_KEY"))

    def get_default_news(self):
        tickers = os.environ.get("TICKERS").split(",")
        news = {}

        for ticker in tickers:
            date = datetime.utcnow() - timedelta(days=1)
            #data = self._get_advantage_data(ticker, date)
            data = self.get_news(ticker, date)
            news[ticker] = data

        return news        

    @tool(description_override="reads the news of a given ticker for a specific day. Has a default of 5 news items.")
    def get_news(self, ticker: str, date: datetime, limit: int = 5) -> dict[str, News]:
        #data = self._get_advantage_data(ticker, date, limit)
        data = self._get_finhub_data(ticker, date, limit)

        return {ticker: data}

    def _get_advantage_data(self, ticker: str, date: datetime, limit=5) -> list[News]:
        result = []
        date = date.strftime("%Y%m%dT%H%M")
        url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&limit={limit}&relevance_score=1&sort=RELEVANCE&time_from={date}&topics=technology&tickers={ticker}&apikey={os.environ.get("ALPHA_VANTAGE_API_KEY")}'

        try:
            res = requests.get(url)
            data = res.json()
            result = [News(**i) for i in data['feed']]
        except Exception as ex:
            print(f"failed to get alphavantage data with [{ex}]")

        return result

    def _get_finhub_data(self, ticker: str, date: datetime, limit=5) -> list[News]:
        result = []
        from_date = date.strftime("%Y-%m-%d")
        to_date = (date + timedelta(days=1)).strftime("%Y-%m-%d")

        try:
            data = self.finnhub_client.company_news(ticker, _from=from_date, to=to_date)
            result = [News(**i) for i in data][:limit]
        except Exception as ex:
            print(f"failed to get finhub data with [{ex}]")            

        return result