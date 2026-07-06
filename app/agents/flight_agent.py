from app.state.travel_state import TravelState
from app.state.flight_schema import FlightResponse
from app.tools.flight_tool import search_flights
from app.utils.airport_lookup import get_iata_code


def flight_agent(state):

    required = ["departure_city", "start_date", "end_date", "destination_results"]
    missing = [key for key in required if not state.get(key)]
    if missing:
        raise ValueError(f"Cannot search flights. Missing required fields: {', '.join(missing)}")

    departure_code = (
        get_iata_code(
            state["departure_city"]
        )
    )

    destination_city = (
        state["destination_results"][0]
        ["airport_city"]
    )

    destination_code = (
        get_iata_code(
            destination_city
        )
    )

    if not departure_code:
        raise ValueError(
            f"No airport found for "
            f"{state['departure_city']}"
        )

    if not destination_code:
        raise ValueError(
            f"No airport found for "
            f"{destination_city}"
        )
    
    '''print("Departure Code:", departure_code)
    print("Destination City:", destination_city)
    print("Destination Code:", destination_code)
    print("Start Date:", state["start_date"])
    print("End Date:", state["end_date"])'''

    flights = search_flights(
        departure_id=departure_code,
        arrival_id=destination_code,
        outbound_date=state["start_date"],
        return_date=state["end_date"]
    )

    state["flight_results"] = flights

    return state
 