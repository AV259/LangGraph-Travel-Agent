def flight_status_router(state):
    if state.get("flight_status") == "available":
        return "flight_advisor"

    return "hotel"
