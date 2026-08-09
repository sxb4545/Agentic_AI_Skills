from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict
from typing import Iterable, List
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph

from .agents import (
    FlightSearchAgent,
    HotelSearchAgent,
    ItineraryPlannerAgent,
    ResearchAgent,
)
from .config import Settings
from .models import TravelPlan, TravelRequest


class TravelGraphState(TypedDict, total=False):
    request: TravelRequest
    flight_summary: str
    hotel_summary: str
    research_summary: str
    itinerary: str


class TravelPlannerMultiAgentSystem:
    """Coordinator that orchestrates specialized agents."""

    def __init__(self, settings: Settings):
        self.flight_agent = FlightSearchAgent(settings)
        self.hotel_agent = HotelSearchAgent(settings)
        self.research_agent = ResearchAgent(settings)
        self.itinerary_agent = ItineraryPlannerAgent(settings)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(TravelGraphState)

        workflow.add_node("flight_agent", self._flight_node)
        workflow.add_node("hotel_agent", self._hotel_node)
        workflow.add_node("research_agent", self._research_node)
        workflow.add_node("itinerary_agent", self._itinerary_node)

        workflow.add_edge(START, "flight_agent")
        workflow.add_edge(START, "hotel_agent")
        workflow.add_edge(START, "research_agent")
        workflow.add_edge("flight_agent", "itinerary_agent")
        workflow.add_edge("hotel_agent", "itinerary_agent")
        workflow.add_edge("research_agent", "itinerary_agent")
        workflow.add_edge("itinerary_agent", END)

        return workflow.compile()

    def _flight_node(self, state: TravelGraphState) -> Dict[str, Any]:
        request = state["request"]
        return {"flight_summary": self.flight_agent.run(request)}

    def _hotel_node(self, state: TravelGraphState) -> Dict[str, Any]:
        request = state["request"]
        return {"hotel_summary": self.hotel_agent.run(request)}

    def _research_node(self, state: TravelGraphState) -> Dict[str, Any]:
        request = state["request"]
        return {
            "research_summary": self.research_agent.run_parallel(
                request.research_questions,
                destination=request.destination,
            )
        }

    def _itinerary_node(self, state: TravelGraphState) -> Dict[str, Any]:
        request = state["request"]
        return {
            "itinerary": self.itinerary_agent.run(
                request,
                flight_summary=state["flight_summary"],
                hotel_summary=state["hotel_summary"],
                research_summary=state["research_summary"],
            )
        }

    def plan_trip(self, request: TravelRequest) -> TravelPlan:
        """Run specialist agents and produce a unified travel recommendation."""

        result = self.graph.invoke({"request": request})

        return TravelPlan(
            flight_summary=result.get("flight_summary", ""),
            hotel_summary=result.get("hotel_summary", ""),
            research_summary=result.get("research_summary", ""),
            itinerary=result.get("itinerary", ""),
        )

    def plan_multiple_trips(self, requests: Iterable[TravelRequest]) -> List[TravelPlan]:
        """Handle multiple user travel requests in parallel."""

        request_list = list(requests)
        if not request_list:
            return []

        with ThreadPoolExecutor(max_workers=min(4, len(request_list))) as pool:
            return list(pool.map(self.plan_trip, request_list))
