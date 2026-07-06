from app.state.travel_state import (
    TravelState
)

from app.state.itinerary_schema import (
    ItineraryResponse
)

from app.services.gemini_service import (
    llm
)


def itinerary_agent(
    state: TravelState
):

    structured_llm = (
        llm.with_structured_output(
            ItineraryResponse
        )
    )

    # Prepare flight journey information
    selected_flight = state.get("selected_flight", {})
    flight_journey_text = ""
    if selected_flight:
        flight_journey_text = f"""
SELECTED FLIGHT JOURNEY (Important - Include in Itinerary):
- Departure: {selected_flight.get('departure_time')}
- Final Arrival: {selected_flight.get('arrival_airport_name')} ({selected_flight.get('arrival_airport')})
- Arrival Time: {selected_flight.get('arrival_time')}
- Total Journey Duration: {selected_flight.get('total_duration')} minutes
- Number of Stops: {selected_flight.get('num_stops')}
- Layovers: {selected_flight.get('layovers', [])}

Flight Segments (Legs):
{selected_flight.get('segments', [])}
"""
    secondary_hotels_info = state.get("secondary_hotels", [])
    secondary_hotels_text = ""
    if secondary_hotels_info:
        secondary_hotels_text = "\n\nSecondary Accommodations (Auto-Selected):\n"
        for hotel_data in secondary_hotels_info:
            hotel = hotel_data.get("hotel", {})
            secondary_hotels_text += f"- {hotel_data.get('destination')}: {hotel.get('name')} (€{hotel.get('price_per_night')}/night, ⭐ {hotel.get('rating')})\n"

    # Prepare restaurant recommendations
    restaurant_recs = state.get("restaurant_results", [])
    restaurant_text = ""
    if restaurant_recs:
        restaurant_text = "\n\nRestaurant Recommendations:\n"
        for rest in restaurant_recs:
            restaurant_text += f"- {rest.get('destination')} - {rest.get('name')} ({rest.get('cuisine_type')}): {rest.get('reason')} Best for: {rest.get('best_for')}\n"

    # Prepare transport suggestions
    transport_text = ""
    transport_suggestions = state.get("transport_suggestions", [])
    if transport_suggestions:
        transport_text = "\n\nInter-City Transport Options:\n"
        for route in transport_suggestions:
            transport_text += f"- {route.get('from_city')} to {route.get('to_city')} ({route.get('distance_estimate')}):\n"
            for option in route.get('options', []):
                transport_text += f"  • {option.get('type')}: {option.get('duration')}, {option.get('estimated_cost')}\n"

    response = structured_llm.invoke(
        f"""
You are an expert travel planner.

Create a personalized multi-destination travel itinerary.

Traveler Interests:
{state.get("interests")}

Traveler Memories:
{state.get("memory_context")}

Trip Duration:
{state.get("duration")} days

Travel Dates:
{state.get("start_date")}
to
{state.get("end_date")}

{flight_journey_text}

All Recommended Destinations:
{state.get("destination_results")}

Selected Flight:
{state.get("selected_flight")}

Primary Accommodation (User Selected):
{state.get("selected_hotel")}
{secondary_hotels_text}

Activities:
{state.get("activity_results")}

{transport_text}

{restaurant_text}

Budget Information:
{state.get("budget_summary")}

INSTRUCTIONS:

1. Create a concise trip summary covering ALL destinations.

2. Summarize the selected flight.
   - Include departure and FINAL arrival city
   - Note any layovers/connections
   - Explain the journey clearly (e.g., "Depart Frankfurt, connect in Delhi, arrive in Jaipur")
   - Do NOT confuse layover cities with the actual trip destination

3. Summarize ALL accommodations (primary and secondary).

4. Summarize the budget situation.

5. Generate a realistic day-by-day itinerary.
   - Allocate days appropriately across all destinations
   - Include travel days between cities
   - Use the transport suggestions provided
   - Show approximate travel times
   - Include specific restaurant names for meals instead of generic descriptions

6. Use activities from ALL destinations appropriately.

7. Include secondary accommodations in the itinerary naturally.

8. Include restaurant recommendations in meals.
   - Use the restaurant names and types provided
   - Match restaurants with meals (breakfast, lunch, dinner)
   - Include reasons why each restaurant is recommended

9. Keep the itinerary realistic and practical.

10. Use morning, afternoon, and evening plans.

11. Add practical travel tips relevant to all destinations.

Return structured output only.
"""
    )

    state["itinerary"] = (
        response.model_dump()
    )

    return state