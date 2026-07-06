from app.state.travel_state import TravelState
from app.services.gemini_service import llm
from pydantic import BaseModel
from typing import List


class TransportOption(BaseModel):
    type: str
    duration: str
    estimated_cost: str
    description: str


class TransportRoute(BaseModel):
    from_city: str
    to_city: str
    distance_estimate: str
    options: List[TransportOption]


class TransportResponse(BaseModel):
    routes: List[TransportRoute]


def transport_suggestion_agent(state: TravelState):
    """
    Generates realistic transport suggestions for traveling between
    recommended destinations. Provides users with practical options
    for inter-city travel (cab, bus, train, flight).
    """

    destinations = state.get("destination_results", [])
    duration = state.get("duration", 7)

    # If only one destination, no inter-city transport needed
    if len(destinations) <= 1:
        state["transport_suggestions"] = []
        return state

    # Create transport request for LLM
    destination_list = [d.get("destination") for d in destinations]

    structured_llm = llm.with_structured_output(TransportResponse)

    response = structured_llm.invoke(
        f"""
You are an expert travel logistics planner.

Trip Destinations (in order):
{', '.join(destination_list)}

Trip Duration:
{duration} days

TASK:

For each pair of consecutive destinations, suggest realistic transport options:

1. Generate 2-3 transport methods (e.g., Private Cab, Bus, Train, Flight)
2. Estimate journey duration based on real geography
3. Estimate costs in EUR
4. Provide brief description of each option

Important:
- Use realistic distances and times
- Include typical cost ranges
- Consider destination geography (e.g., scenic routes, mountain roads)
- Options should be practical for a tourist
- Format costs as "€X-Y" (range)

Return structured output only.
"""
    )

    transport_suggestions = [route.model_dump() for route in response.routes]
    state["transport_suggestions"] = transport_suggestions

    return state
