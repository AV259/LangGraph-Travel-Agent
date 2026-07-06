from app.state.travel_state import TravelState
from datetime import datetime, timedelta


def itinerary_formatter_agent(state: TravelState):
    """
    Formats the structured itinerary into a clean, readable text format.
    """

    itinerary = state.get("itinerary")
    selected_flight = state.get("selected_flight")
    selected_hotel = state.get("selected_hotel")
    budget_summary = state.get("budget_summary")
    start_date_str = state.get("start_date")

    if not itinerary:
        state["formatted_itinerary"] = ""
        return state

    # Parse start date to calculate day dates
    try:
        start_date = datetime.strptime(
            start_date_str, "%Y-%m-%d"
        )
    except:
        start_date = datetime.now()

    # Build formatted output
    output = []

    # Header
    output.append("=" * 70)
    output.append("YOUR PERSONALIZED TRAVEL ITINERARY".center(70))
    output.append("=" * 70)
    output.append("")

    # Trip Summary
    output.append("TRIP SUMMARY")
    output.append("-" * 70)
    output.append(itinerary.get("trip_summary", ""))
    output.append("")

    # Flight Details
    output.append("FLIGHT DETAILS")
    output.append("-" * 70)
    if selected_flight:
        output.append(
            f"Airline: {selected_flight.get('airline', 'N/A')}"
        )
        output.append(
            f"Departure: {selected_flight.get('departure_time', 'N/A')}"
        )
        output.append(
            f"Final Arrival: {selected_flight.get('arrival_airport_name', 'N/A')} ({selected_flight.get('arrival_airport', 'N/A')})"
        )
        output.append(
            f"Arrival Time: {selected_flight.get('arrival_time', 'N/A')}"
        )
        
        num_stops = selected_flight.get('num_stops', 0)
        if num_stops > 0:
            output.append(f"Stops: {num_stops} connection(s)")
            layovers = selected_flight.get('layovers', [])
            if layovers:
                output.append("Layover Details:")
                for layover in layovers:
                    duration = layover.get('duration_minutes', 0)
                    overnight = " (Overnight)" if layover.get('overnight') else ""
                    output.append(f"  • {layover.get('airport')} ({duration} minutes){overnight}")
        else:
            output.append("Direct Flight")
            
        output.append(
            f"Duration: {selected_flight.get('total_duration', 'N/A')} minutes"
        )
        output.append(
            f"Cost: €{selected_flight.get('price', 'N/A')}"
        )
    output.append(itinerary.get("flight_summary", ""))
    output.append("")

    # Hotel Details
    output.append("PRIMARY ACCOMMODATION")
    output.append("-" * 70)
    if selected_hotel:
        # Try to get city from flight arrival airport name, fallback to destination results
        primary_city = "N/A"
        if selected_flight and selected_flight.get('arrival_airport'):
            # Extract city name from airport name
            airport_name = selected_flight.get('arrival_airport_name', '')
            primary_city = airport_name.split('International')[0].split('Airport')[0].strip()
            if not primary_city:
                primary_city = state.get('destination_results', [{}])[0].get('destination', 'N/A')
        else:
            primary_city = state.get('destination_results', [{}])[0].get('destination', 'N/A')
            
        output.append(f"City: {primary_city}")
        output.append(
            f"Hotel: {selected_hotel.get('name', 'N/A')}"
        )
        output.append(
            f"Rating: ⭐ {selected_hotel.get('rating', 'N/A')}"
        )
        output.append(
            f"Price per Night: €{selected_hotel.get('price_per_night', 'N/A')}"
        )
        output.append(
            f"Total for {selected_hotel.get('total_price', 0) // selected_hotel.get('price_per_night', 1) if selected_hotel.get('price_per_night') else 1} nights: €{selected_hotel.get('total_price', 'N/A')}"
        )
        amenities = selected_hotel.get("amenities", [])
        if amenities:
            output.append(
                f"Amenities: {', '.join(amenities)}"
            )
    output.append(itinerary.get("hotel_summary", ""))
    output.append("")

    # Secondary Hotels
    secondary_hotels = state.get("secondary_hotels", [])
    if secondary_hotels:
        output.append("SECONDARY ACCOMMODATIONS")
        output.append("-" * 70)
        for hotel_data in secondary_hotels:
            hotel = hotel_data.get("hotel", {})
            output.append(f"\n{hotel_data.get('destination')}:")
            output.append(
                f"  Hotel: {hotel.get('name', 'N/A')}"
            )
            output.append(
                f"  Rating:  {hotel.get('rating', 'N/A')}"
            )
            output.append(
                f"  Price per Night: €{hotel.get('price_per_night', 'N/A')}"
            )
            output.append(
                f"  Total: €{hotel.get('total_price', 'N/A')}"
            )
            amenities = hotel.get("amenities", [])
            if amenities:
                output.append(
                    f"  Amenities: {', '.join(amenities[:3])}..."
                )
        output.append("")

    # Budget Summary
    output.append(" BUDGET SUMMARY")
    output.append("-" * 70)
    if budget_summary:
        output.append(
            f"Total Cost: €{budget_summary.get('total_cost', 'N/A')}"
        )
        output.append(
            f"Remaining Budget: €{budget_summary.get('remaining_budget', 'N/A')}"
        )
        output.append(
            f"Status: {budget_summary.get('budget_status', 'N/A').upper()}"
        )
    output.append(itinerary.get("budget_summary", ""))
    output.append("")

    # Restaurant Recommendations
    restaurants = state.get("restaurant_results", [])
    if restaurants:
        output.append(" FEATURED RESTAURANTS")
        output.append("-" * 70)
        by_destination = {}
        for rest in restaurants:
            dest = rest.get("destination")
            if dest not in by_destination:
                by_destination[dest] = []
            by_destination[dest].append(rest)
        
        for dest, rests in by_destination.items():
            output.append(f"\n{dest.upper()}:")
            for rest in rests:
                output.append(f"  • {rest.get('name')} ({rest.get('cuisine_type')})")
                output.append(f"    Best for: {rest.get('best_for')}")
                output.append(f"    Why: {rest.get('reason')}")
        output.append("")

    # Travel Tips
    output.append(" TRAVEL TIPS")
    output.append("-" * 70)
    tips = itinerary.get("travel_tips", [])
    for idx, tip in enumerate(tips, 1):
        output.append(f"{idx}. {tip}")
    output.append("")

    # Day-by-Day Itinerary
    output.append("DAY-BY-DAY ITINERARY")
    output.append("=" * 70)
    output.append("")

    days = itinerary.get("days", [])
    for day_plan in days:
        day_num = day_plan.get("day", 1)
        current_date = (
            start_date + timedelta(days=day_num - 1)
        ).strftime("%B %d, %Y")

        output.append(
            f"DAY {day_num}: {current_date}"
        )
        output.append("-" * 70)

        output.append(" Morning:")
        output.append(f"   {day_plan.get('morning', '')}")
        output.append("")

        output.append("  Afternoon:")
        output.append(f"   {day_plan.get('afternoon', '')}")
        output.append("")

        output.append(" Evening:")
        output.append(f"   {day_plan.get('evening', '')}")
        output.append("")
        output.append("")

    # Footer
    output.append("=" * 70)
    output.append("Have a wonderful trip! Safe travels! ".center(70))
    output.append("=" * 70)

    formatted_text = "\n".join(output)
    state["formatted_itinerary"] = formatted_text

    return state
