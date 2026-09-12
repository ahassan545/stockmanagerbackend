import os
from datetime import datetime
import pandas as pd
import logging
from machinelearning.models.modelmetrics import ModelR2, ModelMetrics
from machinelearning.stockpricemodel import LinearRegressionModel
from services.stockhistoricaldataservice import StockHistoricalDataService

logger = logging.getLogger(__name__)


class StockPricingService:
    def __init__(self):
        self.model = LinearRegressionModel("stock_pricer")
        self.historical_data_service = StockHistoricalDataService()

    def predict(self, ticker: str, date: datetime):
        data, _ = self._get_data(ticker, date=date, days=30)

        return self.model.predict(data)

    def train(self, date: datetime = None) -> None:
        date = date if date else datetime.now()
        tickers = os.environ.get("TICKERS").split(",")

        logger.info(f"Started training for tickers [{",".join(tickers)}].")

        data = []
        for ticker in tickers:
            X, y = self._get_data(ticker, date=date)
            data.append((ticker, X, y))

        self.model.train(data)

        logger.info("Completed training.")

    def _get_data(self, ticker: str, date: datetime, days: int = 90):
        result = {}
        data = self.historical_data_service.get_data(ticker, date=date, days=days)

        result["return_1d"] = data["Close"].pct_change()
        result["return_5d"] = data["Close"].pct_change(5).fillna(0).to_numpy().flatten()
        result["return_10d"] = (
            data["Close"].pct_change(10).fillna(0).to_numpy().flatten()
        )
        result["volatility_5d"] = (
            result["return_1d"].rolling(5).std().fillna(0).to_numpy().flatten()
        )
        result["volatility_10d"] = (
            result["return_1d"].rolling(10).std().fillna(0).to_numpy().flatten()
        )
        result["return_1d"] = result["return_1d"].fillna(0).to_numpy().flatten()
        df = pd.DataFrame(result)

        return (
            df[
                [
                    "return_1d",
                    "return_5d",
                    "return_10d",
                    "volatility_5d",
                    "volatility_10d",
                ]
            ],
            data[["Close"]].to_numpy().flatten(),
        )
