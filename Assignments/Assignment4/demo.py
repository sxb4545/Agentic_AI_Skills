from __future__ import annotations

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from src import TravelPlannerMultiAgentSystem, TravelRequest, get_settings


def print_plan(console: Console, title: str, plan_text: str) -> None:
    console.print(Panel(plan_text, title=title, expand=False))


def main() -> None:
    load_dotenv()
    console = Console()
    settings = get_settings()

    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required. Add it to .env before running demo.py")

    planner = TravelPlannerMultiAgentSystem(settings)

    # Single user request demo
    request = TravelRequest(
        origin="New York",
        destination="Tokyo",
        departure_date="2026-10-12",
        return_date="2026-10-19",
        travelers=2,
        budget_usd=4200,
        hotel_nights=7,
        preferences="Nonstop if possible, central hotel, vegetarian-friendly nearby food",
        research_questions=[
            "Do US travelers need a visa for short tourism stays",
            "What local transit pass is best for a 7-day visit",
            "What weather and packing advice applies in mid-October",
        ],
    )

    console.rule("Single Multi-Agent Travel Plan")
    plan = planner.plan_trip(request)
    print_plan(console, "Flight Agent", plan.flight_summary)
    print_plan(console, "Hotel Agent", plan.hotel_summary)
    print_plan(console, "Research Agent", plan.research_summary)
    print_plan(console, "Unified Itinerary", plan.itinerary)

    # Parallel multi-query demo
    batch_requests = [
        TravelRequest(
            origin="San Francisco",
            destination="Paris",
            departure_date="2026-09-05",
            return_date="2026-09-12",
            travelers=1,
            budget_usd=2800,
            hotel_nights=7,
            preferences="Walkable neighborhoods and museum access",
            research_questions=["What city pass gives best value for museums"],
        ),
        TravelRequest(
            origin="Chicago",
            destination="Dubai",
            departure_date="2026-11-02",
            return_date="2026-11-08",
            travelers=2,
            budget_usd=5000,
            hotel_nights=6,
            preferences="Modern hotel with easy metro access",
            research_questions=["Any local etiquette tips travelers should know"],
        ),
    ]

    console.rule("Parallel User Query Demo")
    plans = planner.plan_multiple_trips(batch_requests)
    for idx, item in enumerate(plans, start=1):
        console.print(Panel(item.itinerary, title=f"Batch Plan {idx}", expand=False))


if __name__ == "__main__":
    main()
