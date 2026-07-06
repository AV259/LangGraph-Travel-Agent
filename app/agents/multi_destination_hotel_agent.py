from app.state.travel_state import TravelState
from app.tools.hotel_tool import search_hotels


def multi_destination_hotel_agent(state: TravelState):
    """
    Automatically selects hotels for secondary destinations after the user
    has selected the primary hotel. Uses budget allocation and ratings to
    choose appropriate accommodations without requiring additional HITL.
    """

    destinations = state.get("destination_results", [])
    selected_hotel = state.get("selected_hotel")
    budget_summary = state.get("budget_summary", {})
    total_budget = state.get("budget", 0)
    selected_flight_price = state.get("selected_flight", {}).get("price", 0)
    selected_hotel_cost = selected_hotel.get("total_price", 0) if selected_hotel else 0

    secondary_hotels = []

    # Skip if only one destination or no hotels selected yet
    if len(destinations) <= 1 or not selected_hotel:
        state["secondary_hotels"] = secondary_hotels
        return state

    # Calculate budget remaining after flight and primary hotel
    remaining_budget = total_budget - selected_flight_price - selected_hotel_cost
    trip_duration = state.get("duration", 7)
    primary_hotel_nights = selected_hotel.get("total_price", 0) / selected_hotel.get(
        "price_per_night", 1
    ) if selected_hotel.get("price_per_night") else 1

    # Estimate nights for secondary destinations
    # Distribute remaining nights evenly among secondary destinations
    secondary_destinations = destinations[1:]  # All except first (primary)
    if secondary_destinations:
        nights_per_destination = max(
            1,
            (trip_duration - primary_hotel_nights) // len(secondary_destinations),
        )
        budget_per_destination = remaining_budget / len(secondary_destinations)
    else:
        return state

    # Search and select hotels for each secondary destination
    for dest_info in secondary_destinations:
        destination_name = dest_info.get("destination")

        try:
            # Search hotels for this destination
            hotels = search_hotels(
                destination=destination_name,
                check_in=state.get("start_date"),
                check_out=state.get("end_date"),
            )

            if not hotels:
                continue

            # Auto-select logic:
            # 1. Find highest-rated hotel within budget
            # 2. If none available, pick best value (good rating + affordable)
            # 3. Calculate nights based on trip distribution

            best_hotel = None
            max_rating = 0

            for hotel in hotels:
                hotel_price = hotel.get("total_price", 0)
                hotel_rating = hotel.get("rating", 0)

                # Check if within allocated budget
                if hotel_price <= budget_per_destination:
                    if hotel_rating > max_rating:
                        best_hotel = hotel
                        max_rating = hotel_rating

            # If no hotel found within budget, pick the most affordable one
            if not best_hotel and hotels:
                best_hotel = min(hotels, key=lambda x: x.get("total_price", float("inf")))

            if best_hotel:
                secondary_hotels.append(
                    {
                        "destination": destination_name,
                        "hotel": best_hotel,
                        "nights": nights_per_destination,
                        "selection_reason": f"Highest-rated hotel (⭐ {best_hotel.get('rating', 'N/A')}) within budget allocation for {destination_name}",
                    }
                )

        except Exception as e:
            print(f"Error searching hotels for {destination_name}: {str(e)}")
            continue

    state["secondary_hotels"] = secondary_hotels

    return state
