from langgraph.types import interrupt
from app.state.travel_state import TravelState


def destination_display_agent(state: TravelState):
    """
    Displays all recommended destinations and their activities to the user
    before flight and hotel selection. This gives users context about their
    entire trip before making booking decisions.
    """

    destinations = state.get("destination_results", [])
    activities = state.get("activity_results", [])

    # Create display data structure
    display_data = {
        "message": "Here are your recommended destinations and activities for this trip:",
        "destinations": []
    }

    # Group activities by destination
    for destination_info in destinations:
        destination_name = destination_info.get("destination")
        airport_city = destination_info.get("airport_city")
        reason = destination_info.get("reason")

        # Find activities for this destination
        destination_activities = []
        for activity_data in activities:
            if activity_data.get("destination") == destination_name:
                destination_activities = activity_data.get("activities", [])
                break

        display_data["destinations"].append({
            "name": destination_name,
            "airport_city": airport_city,
            "reason": reason,
            "activities": destination_activities
        })

    # Interrupt to show destinations to user
    interrupt(display_data)

    state["destinations_display_shown"] = True

    return state
