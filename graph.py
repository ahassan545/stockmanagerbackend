from langgraph.graph import StateGraph, END
from models.agentmodel import AgentState
from stockagents.newsagent import NewsAgent
from stockagents.riskanalystagent import RiskAnalystAgent


class StockStateGraph:
    def __init__(
        self,
        news_agent: NewsAgent,
        fundamentals_agent,
        technical_agent,
        fraud_agent,
        structuring_agent,
        risk_analyst_agent: RiskAnalystAgent,
    ):
        self.graph = StateGraph(AgentState)
        self._build_graph(
            news_agent=news_agent,
            fundamentals_agent=fundamentals_agent,
            technical_agent=technical_agent,
            fraud_agent=fraud_agent,
            structuring_agent=structuring_agent,
            risk_analyst_agent=risk_analyst_agent,
        )

    def _build_graph(
        self,
        news_agent: NewsAgent,
        fundamentals_agent,
        technical_agent,
        fraud_agent,
        structuring_agent,
        risk_analyst_agent: RiskAnalystAgent,
    ):
        self.graph.add_node("news", news_agent.get_sentiment)
        self.graph.add_node("fundamentals", fundamentals_agent)
        self.graph.add_node("technical", technical_agent)
        self.graph.add_node("fraud", fraud_agent)
        self.graph.add_node("structuring", structuring_agent)
        self.graph.add_node("risk_analyst", risk_analyst_agent.analyze)

        self.graph.set_entry_point("news")

        self.graph.add_edge("news", "structuring")
        self.graph.add_edge("fraud", "structuring")
        self.graph.add_edge("fundamentals", "structuring")
        self.graph.add_edge("technical", "structuring")
        self.graph.add_edge("structuring", "risk_analyst")
        self.graph.add_edge("risk_analyst", END)

    def get_compiled_graph(self):
        return self.graph.compile()
