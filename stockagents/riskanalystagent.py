from models.agentmodel import AgentState


class RiskAnalystAgent:
    def __init__(
        self,
        fraud_weight: float = 0.50,
        fundamental_weight: float = 0.20,
        technical_weight: float = 0.20,
        sentiment_weight: float = 0.10,
    ):
        self.fraud_weight = fraud_weight
        self.fundamental_weight = fundamental_weight
        self.technical_weight = technical_weight
        self.sentiment_weight = sentiment_weight

    def analyze(self, state: AgentState) -> None:
        fraud_score = self._get_fraud_score(state.m_score)
        fundamental_score = self._get_fundamental_score(state.operating_margin)
        technical_score = self._get_technical_score(state.market_beta)
        final_score = self._get_final_score(
            fraud_score, fundamental_score, technical_score, state.sentiment_score
        )

        state.risk_matrix = {
            "final_score": final_score,
            "break_down": {
                "fraud": fraud_score,
                "fundamental": fundamental_score,
                "technical": technical_score,
                "sentiment": state.sentiment_score,
            },
            "risk_tier": self._get_final_risk_tier(final_score),
        }

    def _get_fraud_score(self, m_score: float) -> int:
        # (Beneish M-Score threshold is typically -1.78)
        # Scores closer to 0 or positive indicate high manipulation risk
        if m_score < -1.78:
            return 10
        else:
            return 1

    def _get_fundamental_score(self, operating_margin: float) -> int:
        if operating_margin >= 0.1:
            return 10
        else:
            return 1

    def _get_technical_score(self, market_beta: float) -> int:
        if market_beta <= 1.5:
            return 10
        else:
            return 1

    def _get_verdict(self, final_score: float) -> str:
        if final_score >= 7.5:
            return "BUY"
        elif final_score >= 4.0:
            return "HOLD"
        else:
            return "SELL"

    def _get_final_score(
        self, fraud_score: int, fundamental_score: int, technical_score: int, sentiment_score: int
    ) -> float:
        final_score = (
            (fraud_score * self.fraud_weight)
            + (fundamental_score * self.fundamental_weight)
            + (technical_score * self.technical_weight)
            + (sentiment_score * self.sentiment_weight)
        )
        return round(final_score, 2)
