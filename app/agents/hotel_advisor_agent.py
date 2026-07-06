from app.state.travel_state import TravelState

from app.state.hotel_advisor_schema import (
    HotelRecommendation
)

from app.services.gemini_service import llm


def hotel_advisor_agent(
    state: TravelState
):

    structured_llm = llm.with_structured_output(
        HotelRecommendation
    )

    # Get destination city
    destination_city = state["destination_results"][0].get("destination", "Unknown")

    response = structured_llm.invoke(
        f"""
        User Budget:
        {state.get("budget")}

        Interests:
        {state.get("interests")}

        Memory Context:
        {state.get("memory_context")}

        Destination City:
        {destination_city}

        Hotel Options:
        {state.get("hotel_results")}

        Recommend ONE hotel.

        Consider:

        - value for money
        - rating
        - amenities
        - overall suitability

        IMPORTANT: Include the city name in your recommendation.
        The destination city is: {destination_city}

        Explain why it is the best choice.
        """
    )

    state["recommended_hotel"] = (
        response.model_dump()
    )

    return state