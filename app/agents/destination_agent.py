from app.state.travel_state import TravelState

from app.state.destination_schema import (
    DestinationResponse
)

from app.services.gemini_service import llm


def destination_agent(state: TravelState):

    structured_llm = llm.with_structured_output(
        DestinationResponse
    )

    response = structured_llm.invoke(
        f"""
        You are a travel planning expert and a world-class travel researcher.

        Destination:
        {state.get("destination")}

        Budget:
        {state.get("budget")}

        Duration:
        {state.get("duration")}

        Interests:
        {state.get("interests")}

        User Preferences:
        {state.get("memory_context")}

    TASK:

    Recommend the best travel destinations that match the traveler's interests, budget, and trip duration.

    For EACH recommendation provide:

    1. destination
    - The actual place the traveler should visit.
    - Can be a city, region, island, mountain area, beach destination, etc.

    2. airport_city
    - The nearest major city that has an international or domestic airport suitable for flight search.
    - This field will later be used by the Flight Agent.
    - Always provide a real city with a major airport.

    3. reason
    - Explain in 2-3 sentences why this destination matches the traveler.

    IMPORTANT RULES:

        1. If the user already specifies a city, town,
            region, island, or tourist destination:

            Return ONLY that destination.

            Examples:
            Tokyo → Tokyo
            Munich → Munich
            Halstatt → Halstatt
            Paris → Paris
            Mumbai → Mumbai
            Santorini → Santorini

        2. If the user specifies a country:

            Return 2-3 destination recommendations.

            Examples:
            Japan → Tokyo, Kyoto, Osaka
            Germany → Munich, Berlin, Hamburg
            Austria → Vienna, Salzburg, Hallstatt
            India → Mumbai, Delhi, Lucknow, Jaipur
            Italy → Rome, Florence, Venice

        Destination and airport_city are NOT always the same.

        Examples:

        destination = Kerala
        airport_city = Kochi

        destination = Swiss Alps
        airport_city = Zurich

        destination = Bavaria
        airport_city = Munich

        destination = Santorini
        airport_city = Santorini

        destination = Tokyo
        airport_city = Tokyo
      
        Recommend the best cities or regions
        for this trip.

        Explain briefly why each recommendation
        fits the traveler.
        """
    )

    state["destination_results"] = [
        rec.model_dump()
        for rec in response.recommendations
    ]

    #print(state["destination_results"])

    return state