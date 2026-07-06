from langgraph.types import interrupt
from app.state.travel_state import TravelState

def flight_selection_agent(state: TravelState):
    state["flight_selection_required"] = True

    selected_option = interrupt(
        {
            "message": "Please select a flight from the available options.",
            "flights": state['flight_results'],
            "recommended_flight": state["recommended_flight"]
        }
    )

    state["selected_flight"] = selected_option

    state["flight_selection_required"] = False

    return state



