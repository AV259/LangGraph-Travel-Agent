from app.state.travel_state import TravelState
from app.tools.hotel_tool import search_hotels

def hotel_agent(state: TravelState):
    destination = state["destination_results"][0]["destination"]
    
    hotels = search_hotels(
        destination=destination,
        check_in=state["start_date"],
        check_out=state["end_date"]
    )

    state["hotel_results"] = hotels

    return state
