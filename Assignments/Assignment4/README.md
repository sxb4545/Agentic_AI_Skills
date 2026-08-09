# Assignment 4: Smart Travel Planning Multi-Agent System

A LangGraph-based multi-agent project where specialized agents collaborate to:

- Search flights and hotels from live web data
- Perform deeper travel research
- Build a complete itinerary
- Handle multiple user queries in parallel
- Return a single unified recommendation

## Multi-Agent Design

1. FlightSearchAgent
- Uses SerpApi (Google Flights engine)
- Summarizes best value, premium, and budget options

2. HotelSearchAgent
- Uses SerpApi (Google Hotels engine)
- Summarizes best location/value and comfort-focused stays

3. ResearchAgent
- Uses Tavily deep web search
- Answers travel questions with practical tips and source URLs

4. ItineraryPlannerAgent
- Merges all specialist outputs
- Produces a day-by-day itinerary plus booking priorities

5. Coordinator: TravelPlannerMultiAgentSystem
- Uses a LangGraph StateGraph workflow
- Runs flight, hotel, and research specialist nodes in parallel branches
- Merges specialist outputs in a planner node
- Supports handling multiple travel requests in parallel

## Project Structure

```text
Assignment4/
  README.md
  requirements.txt
  .env.example
  demo.py
  src/
    __init__.py
    config.py
    models.py
    tools.py
    agents.py
    orchestrator.py
```

## Setup

1. Create and activate venv (PowerShell):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create env file:

```powershell
Copy-Item .env.example .env
```

4. Fill keys in .env:

```env
OPENAI_API_KEY=...
SERPAPI_API_KEY=...
TAVILY_API_KEY=...
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0
```

## Run Demo

From Assignment4 directory:

```powershell
python demo.py
```

Demo includes:
- One complete travel planning run
- One parallel batch run with 2 simultaneous user requests

## Can We Use SerpApi Key and Tavily Key?

Yes. This project is built to use both:

- SERPAPI_API_KEY drives flight and hotel search tools
- TAVILY_API_KEY powers deep travel research

If either key is missing, that specialist agent returns a graceful message, while the rest of the system continues.

## Notes

- OPENAI_API_KEY is required because the specialist and planner agents are LLM-driven.
- This template is intentionally modular so you can swap APIs, add tools, or extend the LangGraph workflow with new nodes.
