from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from langgraph.config import get_stream_writer

from app.tools.flight_tool import (
    FlightSearchTemporaryError,
    search_flights,
)
from app.utils.airport_lookup import get_iata_code


def flight_agent(state):
    try:
        writer = get_stream_writer()
    except RuntimeError:
        writer = lambda _: None

    state["flight_status"] = "searching"
    state["flight_message"] = None
    state["flight_retry_count"] = 0

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

    def notify_retry(retry_state):
        retry_number = retry_state.attempt_number
        state["flight_retry_count"] = retry_number
        writer(
            {
                "type": "flight_retrying",
                "attempt": retry_number,
                "message": (
                    "Flight search is temporarily unavailable. "
                    f"We're retrying now (attempt {retry_number} of 1)."
                ),
            }
        )

    retryer = Retrying(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=2, min=2, max=4),
        retry=retry_if_exception_type(FlightSearchTemporaryError),
        before_sleep=notify_retry,
        reraise=True,
    )

    try:
        flights = retryer(
            search_flights,
            departure_id=departure_code,
            arrival_id=destination_code,
            outbound_date=state["start_date"],
            return_date=state["end_date"],
        )
    except FlightSearchTemporaryError:
        state["flight_results"] = []
        state["flight_status"] = "failed"
        state["flight_message"] = (
            "We couldn't retrieve flight options after a retry. "
            "We'll continue planning your trip without flight details."
        )
        return state

    state["flight_results"] = flights
    if flights:
        state["flight_status"] = "available"
    else:
        state["flight_status"] = "unavailable"
        state["flight_message"] = (
            "We couldn't find available flights for these dates and destinations. "
            "We'll continue planning the rest of your trip without flight details."
        )

    return state
 