import dspy

from models.agentmodel import AgentState
from services.newsservice import NewsService
import os
from stockagents.evalagent import EvalAgent
from models.newsmodel import News


class NewsSentimentAnalyzer(dspy.Signature):
    """
    Analyze the sentiment of news articles and provide the sentiment score.
    """

    news_articles: list = dspy.InputField()
    sentiment_score: int = dspy.OutputField(
        desc="value between -1 and 1, where -1 is negative sentiment, 0 is neutral, and 1 is positive sentiment."
    )


class NewsAgent:
    def __init__(self, news_service: NewsService):
        self.news_service = news_service
        lm = dspy.LM(
            model=os.environ.get("MODEL"),
            api_base=os.environ.get("OPEN_ROUTER_BASE_API"),
            api_key=os.environ.get("OPEN_ROUTER_API_KEY"),
        )
        dspy.configure(lm=lm)

    def get_sentiment(self, state: AgentState) -> None:
        news: dict[str, News] = self.news_service.get_news(
            state.ticker, state.start_date
        )

        result = self.analyze_sentiment(list(news.values()))
        state.news_data = {"sentiment_score": result.sentiment_score}
        print(f"Sentiment Score for {state.ticker}: {result.sentiment_score}")

    @EvalAgent.evaluate
    def analyze_sentiment(self, news: list[News]) -> dict[str, str]:
        predict = dspy.Predict(NewsSentimentAnalyzer)
        return predict(news_articles=news)
