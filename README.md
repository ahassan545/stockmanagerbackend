I think this is one of the best project ideas because it naturally grows with your skills. You can start with a simple summarizer and evolve it into a genuine AI research assistant.

For stock news, I’d combine multiple sources rather than relying on just one.

Source	Best for	API?
NewsAPI	General financial news	✅ Easy
Alpha Vantage	News + market data	✅ Free tier
Finnhub	Company news, earnings, sentiment	✅ Excellent
Polygon.io	Professional market data	✅ Paid/free
Yahoo Finance	Company news	Unofficial libraries
MarketWatch	Articles	RSS/Scraping (check terms)
Reuters	High-quality news	Enterprise API or web search
SEC EDGAR	Company filings	✅ Free
Companies’ investor relations pages	Press releases	Usually RSS

I’d build it in stages

Version 1 (1 weekend)

Input:

AAPL

The app:

* Fetches the latest 10–20 news articles
* Summarises each article
* Produces an overall sentiment
* Highlights recurring themes

Output:

Apple News Summary
Overall sentiment:
Positive
Key themes:
• AI investment
• iPhone demand
• Services growth
Top risks:
• China sales
• Tariffs
Confidence:
Medium

Skills:

* APIs
* Prompting
* Structured outputs

⸻

Version 2

Add market data.

The app also retrieves:

* Current price
* P/E ratio
* Market cap
* 52-week high/low
* Analyst ratings

Then ask the LLM to relate the news to those metrics.

⸻

Version 3

This is where it starts to resemble something used by investment analysts.

The agent:

User:
"Research Nvidia"

Workflow:

1. Get latest news
2. Fetch stock metrics
3. Download latest SEC filing
4. Read earnings transcript
5. Summarise all sources
6. Produce an investment memo

Output:

* Executive summary
* Bull case
* Bear case
* Risks
* Opportunities
* Watch list

Now you're combining RAG with external tools.
---
### Version 4
Add a "research agent."
Instead of hardcoding steps, create tools like:

search_news()

get_stock_price()

get_company_profile()

get_sec_filings()

search_earnings_calls()

web_search()

The LLM decides which tools to call and in what order.
---
## A tech stack I'd recommend
- **LLM:** OpenAI GPT-5.5
- **Framework:** LangGraph (excellent for multi-step agent workflows)
- **News API:** Finnhub
- **Market data:** Alpha Vantage (to start)
- **Storage:** SQLite for saved reports
- **Vector database:** Chroma (when you start indexing filings)
- **Frontend:** Streamlit
- **Evaluation:** LangSmith once you reach the agent stage
## Some extra features that would stand out
- Daily email briefing for a watchlist
- Compare two companies side by side
- Ask questions like "Why did the stock fall yesterday?"
- Display a timeline of major news events
- Detect contradictory reporting across sources
- Estimate whether a news story is likely to be market-moving
- Generate follow-up questions an analyst should investigate
## If I were building this as a learning project
I'd keep the scope manageable and iterate:
1. **News summarizer** (API calls + LLM)
2. **Sentiment analysis** (structured output)
3. **Market data integration**
4. **SEC filing retrieval and RAG**
5. **Multi-tool research agent**
6. **Daily automated research reports**
That progression maps well to the concepts you'll encounter in an AI engineering book and results in a portfolio project that's directly relevant to financial services. It demonstrates practical AI engineering skills—API integration, retrieval, tool use, orchestration, and report generation—rather than just wrapping an LLM in a chat interface.

I actually agree with your instinct. One of the biggest mistakes people make is turning everything into an “agent” because it’s fashionable.

For the first few versions of this project, you don’t need an agent at all. A deterministic workflow is simpler, cheaper, easier to debug, and more reliable.

For example:

User enters ticker
      ↓
Fetch latest news
      ↓
Fetch market data
      ↓
Fetch latest filing
      ↓
Summarise each source
      ↓
Combine into final report

That’s just orchestration. You know exactly what happens every time.

Where RAG fits

RAG only comes into play if you’re searching over a corpus of documents.

For example:

SEC filings
10-Ks
10-Qs
Annual reports
Earnings transcripts

The user asks:

“What risks has Microsoft mentioned around AI?”

You retrieve the relevant chunks and feed them to the model. That’s classic RAG.

Where an agent becomes useful

An agent is valuable when the workflow isn’t known ahead of time.

Imagine the user asks:

“Should I be worried about HSBC after today’s news?”

The system might need to decide:

* Search today’s news
* Check the share price reaction
* Look at analyst downgrades
* Read the latest earnings transcript
* Search previous similar events
* Compare with peers
* Decide whether to fetch regulatory announcements

You don’t know beforehand which tools are needed or in what order.

That’s where an agent shines—it plans its own sequence of actions.

Another example

Suppose someone asks:

“Find three UK banks with improving margins that haven’t mentioned commercial real estate risk recently.”

Now the system has to:

1. Find candidate companies
2. Read multiple filings
3. Compare financial metrics
4. Search recent news
5. Filter results
6. Produce a ranked answer

A fixed pipeline becomes awkward because every question could require a different path.

What I’d build instead

If your goal is to learn AI engineering, I’d deliberately avoid agents initially.

1. REST API (FastAPI)
2. News ingestion
3. Financial data API
4. RAG over filings
5. LLM summarisation
6. Evaluation (Are the summaries accurate? Are citations correct?)
7. Caching
8. Observability and logging
9. Deploy to the cloud

Those are the skills you’ll use every day in production AI systems.

Only after that would I experiment with an agent, and even then I’d ask whether it genuinely improves the product. In many enterprise applications—especially in regulated industries like financial services—a deterministic workflow is preferred because it’s predictable, testable, and easier to audit.

So I think your intuition is good: for this project, I’d frame it as an AI research pipeline rather than an AI agent. If later you identify user requests that can’t be handled well by a fixed workflow, that’s the point where introducing an agent becomes a design decision rather than a default choice.

#Sample Finhub response
{'category': 'company', 'datetime': 1785809636, 'headline': 'NYU Professor Says Watch Smaller AI Stocks When The Shakeout Hits', 'id': 141105543, 'image': 'https://s.yimg.com/rz/stage/p/yahoo_finance_en-US_h_p_finance_2.png', 'related': 'AAPL', 'source': 'Yahoo', 'summary': "Aswath Damodaran warns smaller AI stocks face a shakeout as Big Tech's cash flow protects Magnificent Seven giants.", 'url': 'https://finnhub.io/api/news?id=025d1b60c8656ec9ef57f2765f75d81a6a113ae49811fa2d9b30a35287ac98f7'}

#Sample vantage response
{'title': 'Apple Files New Challenge Against UK Effort to Access User Files', 'url': 'https://www.bloomberg.com/news/articles/2026-08-03/apple-files-new-challenge-against-uk-effort-to-access-user-files', 'time_published': '20260803T181300', 'authors': ['Ryan Gallagher'], 'summary': "Apple Inc. has filed a new legal challenge against the UK government's efforts to access encrypted user data, including that of iPhone users, stored in the cloud. A UK court, which oversees secret surveillance activities, confirmed Apple's latest filing, with a hearing scheduled for September. The details of Apple's specific arguments in the filing are not yet public due to the confidentiality of the proceedings.", 'banner_image': None, 'source': 'Bloomberg.com', 'category_within_source': 'General', 'source_domain': 'Bloomberg.com', 'topics': [{'topic': 'technology', 'relevance_score': '0.931358'}], 'overall_sentiment_score': 0.117207, 'overall_sentiment_label': 'Neutral', 'ticker_sentiment': [{'ticker': 'AAPL', 'relevance_score': '1.000000', 'ticker_sentiment_score': '0.116312', 'ticker_sentiment_label': 'Neutral'}]}