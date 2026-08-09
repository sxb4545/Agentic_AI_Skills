from __future__ import annotations

import json
from typing import Any, Dict, List

import requests
from tavily import TavilyClient

from .config import Settings

SERPAPI_ENDPOINT = "https://serpapi.com/search.json"


def _safe_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=True)


def _serpapi_request(params: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    payload = {**params, "api_key": api_key}
    response = requests.get(SERPAPI_ENDPOINT, params=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def search_flights(settings: Settings, query: str, max_results: int = 5) -> str:
    """Search flights using SerpApi Google Flights engine."""

    if not settings.serpapi_api_key:
        return "SERPAPI_API_KEY is missing. Flight search is unavailable."

    try:
        raw = _serpapi_request(
            {
                "engine": "google_flights",
                "q": query,
                "hl": "en",
                "gl": "us",
                "currency": "USD",
            },
            settings.serpapi_api_key,
        )
    except Exception as exc:
        return f"Flight search failed: {exc}"

    records: List[Dict[str, Any]] = []
    for section in ("best_flights", "other_flights"):
        for item in raw.get(section, []):
            records.append(
                {
                    "airlines": [f.get("name", "Unknown") for f in item.get("flights", [])],
                    "price": item.get("price", "N/A"),
                    "duration": item.get("total_duration", "N/A"),
                    "carbon_kg": item.get("carbon_emissions", {}).get("this_flight", "N/A"),
                    "booking": item.get("booking_token", "N/A"),
                }
            )

    return _safe_json(records[:max_results] or [{"message": "No flights found"}])


def search_hotels(settings: Settings, query: str, check_in: str, check_out: str, max_results: int = 5) -> str:
    """Search hotels using SerpApi Google Hotels engine."""

    if not settings.serpapi_api_key:
        return "SERPAPI_API_KEY is missing. Hotel search is unavailable."

    try:
        raw = _serpapi_request(
            {
                "engine": "google_hotels",
                "q": query,
                "check_in_date": check_in,
                "check_out_date": check_out,
                "adults": "2",
                "currency": "USD",
                "gl": "us",
                "hl": "en",
            },
            settings.serpapi_api_key,
        )
    except Exception as exc:
        return f"Hotel search failed: {exc}"

    properties = raw.get("properties", [])
    records: List[Dict[str, Any]] = []
    for item in properties:
        records.append(
            {
                "name": item.get("name", "Unknown"),
                "price_per_night": item.get("rate_per_night", {}).get("lowest", "N/A"),
                "total_rate": item.get("total_rate", {}).get("lowest", "N/A"),
                "rating": item.get("overall_rating", "N/A"),
                "reviews": item.get("reviews", "N/A"),
            }
        )

    return _safe_json(records[:max_results] or [{"message": "No hotels found"}])


def deep_research(settings: Settings, question: str, max_results: int = 5) -> str:
    """Run deeper web research using Tavily search."""

    if not settings.tavily_api_key:
        return "TAVILY_API_KEY is missing. Research agent is unavailable."

    try:
        client = TavilyClient(api_key=settings.tavily_api_key)
        result = client.search(
            query=question,
            search_depth="advanced",
            max_results=max_results,
            include_answer=True,
            include_raw_content=False,
        )
    except Exception as exc:
        return f"Research search failed: {exc}"

    compact = {
        "answer": result.get("answer", "No direct answer returned"),
        "sources": [
            {
                "title": item.get("title", "Unknown"),
                "url": item.get("url", "N/A"),
                "content": item.get("content", "")[:320],
            }
            for item in result.get("results", [])
        ],
    }
    return _safe_json(compact)
