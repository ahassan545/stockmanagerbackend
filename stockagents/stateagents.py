from models.agentmodel import AgentState


def news_agent(state: AgentState):
    print("🤖 Running News Agent Mock...")
    return {"news_data": {"sentiment_score": 0.75, "geopolitical_risk": "low"}}


def fundamentals_agent(state: AgentState):
    print("📊 Running Fundamentals Agent Mock...")
    return {"fundamental_data": {"pe_ratio": 15.4, "margin_growth": 0.08}}


def technical_agent(state: AgentState):
    print("📈 Running Technical Agent Mock...")
    return {"technical_data": {"beta": 1.2, "trend_slope": "bullish"}}


def fraud_agent(state: AgentState):
    print("🔍 Running Fraud Agent Mock...")
    return {"fraud_data": {"beneish_m_score": -2.45, "flagged": False}}


def structuring_agent(state: AgentState):
    # This node compiles the mock data into your exact clean JSON format
    print("📦 Formatting data for Open-Weights...")
    return state


def risk_analyst_agent(state: AgentState):
    print("🧠 Running Risk Analyst Mock (DeepSeek-R1 simulation)...")
    return {"risk_matrix": {"market_risk": "Medium", "fraud_risk": "Low"}}


def market_analyst_agent(state: AgentState):
    print("✍️ Running Market Analyst Mock...")
    return {
        "final_report": f"Investment thesis report for {state.ticker} based on mock data.",
        "iterations": state.iterations + 1,
    }


# The Gatekeeper Router
def gatekeeper_router(state: AgentState):
    print("🛡️ Verifier Gatekeeper evaluating...")
    # Simulate a loop once to test your conditional routing path
    if state.iterations < 2:
        print("❌ Fails Threshold! Looping back to Market Analyst.")
        return "loop_back"
    print("✅ Passes Threshold! Proceeding to Telemetry.")
    return "exit"
