import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from services.newsservice import NewsService
from services.stockpricingservice import StockPricingService
from models.agentmodel import Agent, Runner, trace
from datetime import datetime
import json
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

app = FastAPI()


@app.get("/news", response_class=JSONResponse)
def get_news():
    service = NewsService()
    data = service.get_news()
    result = [f"{k}: {d_item.summary}" for k, d in data.items() for d_item in d]
    return result


@app.post("/train-stock-prediction", response_class=PlainTextResponse)
async def train_stock_prediction(request: Request):
    data = await request.json()
    service = StockPricingService()

    service.train(datetime.strptime(data["date"], "%Y-%m-%d"))

    return "training completed"


@app.post("/predict", response_class=PlainTextResponse)
async def predict(request: Request):
    data = await request.json()
    service = StockPricingService()

    result = service.predict(
        data["ticker"], datetime.strptime(data["date"], "%Y-%m-%d")
    )

    return json.dumps(result)


@app.get("/news-agent", response_class=JSONResponse)
def run_news_agent():
    message = "Get latest stock news from today. Provide summary of the returned in one sentence."
    news_instructions = (
        "You are a stock news agent, only use provided tools to get stock news."
    )
    news_service = NewsService()

    news_agent = Agent(
        name="News Agent",
        instructions=news_instructions,
        model="gpt-4o-mini",
        tools=[news_service.get_default_news],
    )

    with trace("Stock News Agent"):
        result = Runner.run(news_agent, message)
        print(result)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
