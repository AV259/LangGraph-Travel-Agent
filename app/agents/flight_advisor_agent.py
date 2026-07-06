from app.state.travel_state import TravelState
from app.state.flight_advisor_schema import (
    FlightRecommendation
)

from app.services.gemini_service import llm


def flight_advisor_agent(state: TravelState):

    structured_llm = llm.with_structured_output(
        FlightRecommendation
    )

    # Get flight results - they now include actual arrival airport
    flight_results = state.get("flight_results", [])
    
    # Extract final destination from first flight in results
    final_arrival_airport = "Unknown"
    if flight_results:
        final_arrival_airport = flight_results[0].get("arrival_airport_name", "Unknown")

    response = structured_llm.invoke(
        f"""
        User Budget:
        {state.get("budget")}

        User Interests:
        {state.get("interests")}

        User Preferences:
        {state.get("memory_context")}

        Available Flights (with complete journey information):
        {state.get("flight_results")}

        Final Destination Airport:
        {final_arrival_airport}

        Recommend the best flight.

        Consider:
        - price
        - convenience
        - total journey time (including layovers)
        - number of stops
        - overall trip suitability

        IMPORTANT: 
        - The arrival_airport_name field shows the FINAL destination
        - layovers field shows all intermediate stops
        - num_stops shows how many connections are needed
        - Use arrival_airport_name in your recommendation (not the code)

        Explain your reasoning.
        """
    )

    state["recommended_flight"] = (
        response.model_dump()
    )

    return state