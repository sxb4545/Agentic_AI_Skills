from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class TravelRequest:
    """Normalized user travel request consumed by the coordinator."""

    origin: str
    destination: str
    departure_date: str
    return_date: str
    travelers: int = 1
    budget_usd: int = 2500
    hotel_nights: int = 5
    preferences: str = "Balanced comfort and cost"
    research_questions: List[str] = field(default_factory=list)


@dataclass
class TravelPlan:
    """Unified output produced by the multi-agent system."""

    flight_summary: str
    hotel_summary: str
    research_summary: str
    itinerary: str
