from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AgentState(BaseModel):
    ticker: str
    start_date: datetime
    end_date: datetime
    news_data: Optional[dict] = None
    fundamental_data: Optional[dict] = None
    technical_data: Optional[dict] = None
    operating_margin: Optional[float] = 0.0
    risk_matrix: Optional[dict] = None
    final_report: str = ""
    iterations: int = 0
    feedback: Optional[str] = None
    m_score: Optional[float] = -100.0
    market_beta: Optional[float] = 0.0
    sentiment_score: Optional[float] = 0.0
