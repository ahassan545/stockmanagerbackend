import os
from deepeval import settings
from datetime import datetime
from graph import StockStateGraph
from services.newsservice import NewsService
from stockagents.newsagent import NewsAgent
from stockagents.riskanalystagent import RiskAnalystAgent
from stockagents.stateagents import (
    fundamentals_agent,
    technical_agent,
    fraud_agent,
    structuring_agent,
)


def main():


    stock_graph = StockStateGraph(
        news_agent=NewsAgent(news_service=NewsService()),
        risk_analyst_agent=RiskAnalystAgent(),
        fundamentals_agent=fundamentals_agent,
        technical_agent=technical_agent,
        fraud_agent=fraud_agent,
        structuring_agent=structuring_agent,
    )

    final_output = stock_graph.get_compiled_graph().invoke(
        {
            "ticker": "AAPL",
            "iterations": 0,
            "start_date": datetime.strptime("2026-04-23", "%Y-%m-%d"),
            "end_date": datetime.strptime("2026-07-22", "%Y-%m-%d"),
        }
    )
    print("Final Output:", final_output)


if __name__ == "__main__":
    main()
