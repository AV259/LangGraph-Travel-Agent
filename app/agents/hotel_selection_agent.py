from langgraph.types import interrupt

from app.state.travel_state import TravelState


def hotel_selection_agent(state: TravelState):

    state["hotel_selection_required"] = True

    selected_hotel = interrupt(
        {
            "message":
                "Please select a hotel",

            "hotels":
                state["hotel_results"],

            "recommended":
                state["recommended_hotel"]
        }
    )

    state["selected_hotel"] = selected_hotel

    state["hotel_selection_required"] = False

    return state