from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List

from langchain_openai import ChatOpenAI

from .config import Settings
from .models import TravelRequest
from .tools import deep_research, search_flights, search_hotels


class BaseAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.llm = ChatOpenAI(
            model=settings.openai_chat_model,
            temperature=settings.openai_temperature,
            api_key=settings.openai_api_key,
        )


class FlightSearchAgent(BaseAgent):
    def run(self, request: TravelRequest) -> str:
        raw = search_flights(
            self.settings,
            query=(
                f"Round trip from {request.origin} to {request.destination} "
                f"departing {request.departure_date} returning {request.return_date} "
                f"for {request.travelers} traveler(s)"
            ),
        )

        prompt = f"""You are a flight specialist agent.
Summarize the flight options below for a traveler.

Trip details:
- Origin: {request.origin}
- Destination: {request.destination}
- Budget (USD): {request.budget_usd}
- Preferences: {request.preferences}

Raw flight data:
{raw}

Return:
1) Best value option
2) Premium option
3) Budget-conscious recommendation
4) Important trade-offs (duration, carbon, price)
"""
        return self.llm.invoke(prompt).content


class HotelSearchAgent(BaseAgent):
    def run(self, request: TravelRequest) -> str:
        raw = search_hotels(
            self.settings,
            query=f"Best hotels in {request.destination}",
            check_in=request.departure_date,
            check_out=request.return_date,
        )

        prompt = f"""You are a hotel specialist agent.
Summarize the hotel options below for a traveler.

Trip details:
- Destination: {request.destination}
- Nights: {request.hotel_nights}
- Budget (USD): {request.budget_usd}
- Preferences: {request.preferences}

Raw hotel data:
{raw}

Return:
1) Best location/value option
2) Comfort-focused option
3) Budget option
4) Any red flags
"""
        return self.llm.invoke(prompt).content


class ResearchAgent(BaseAgent):
    def run_one(self, question: str, destination: str) -> str:
        raw = deep_research(
            self.settings,
            question=f"{question} in {destination}. Provide current practical guidance.",
        )

        prompt = f"""You are a travel research analyst.
Question: {question}
Destination: {destination}

Research snippets:
{raw}

Return concise guidance with:
- direct answer
- 3 practical tips
- citation URLs from the sources
"""
        return self.llm.invoke(prompt).content

    def run_parallel(self, questions: Iterable[str], destination: str) -> str:
        question_list: List[str] = [q for q in questions if q.strip()]
        if not question_list:
            return "No research questions were supplied."

        with ThreadPoolExecutor(max_workers=min(4, len(question_list))) as pool:
            results = list(pool.map(lambda q: self.run_one(q, destination), question_list))

        merged = []
        for idx, result in enumerate(results, start=1):
            merged.append(f"Research {idx}:\n{result}")
        return "\n\n".join(merged)


class ItineraryPlannerAgent(BaseAgent):
    def run(
        self,
        request: TravelRequest,
        flight_summary: str,
        hotel_summary: str,
        research_summary: str,
    ) -> str:
        prompt = f"""You are the itinerary planner agent that merges specialist outputs.
Create one unified recommendation.

Traveler request:
- Origin: {request.origin}
- Destination: {request.destination}
- Departure: {request.departure_date}
- Return: {request.return_date}
- Travelers: {request.travelers}
- Budget (USD): {request.budget_usd}
- Preferences: {request.preferences}

Flight specialist summary:
{flight_summary}

Hotel specialist summary:
{hotel_summary}

Research specialist summary:
{research_summary}

Output format:
1) Recommended flight + hotel combination with total estimated cost
2) Day-by-day itinerary
3) Risk checklist and how to mitigate each risk
4) Final booking priority order (what to book first)
"""
        return self.llm.invoke(prompt).content
