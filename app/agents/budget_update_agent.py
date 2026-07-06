from app.state.travel_state import (
    TravelState
)


def budget_update_agent(
    state: TravelState
):

    decision = state.get(
        "budget_decision"
    )

    if not decision:
        return state

    action = decision.get(
        "action"
    )

    if action == "switch_hotel":

        state["selected_hotel"] = (
            decision["option"]
        )

        state[
            "budget_adjustment_attempted"
        ] = True

    elif action == "switch_flight":

        state["selected_flight"] = (
            decision["option"]
        )

        state[
            "budget_adjustment_attempted"
        ] = True

    elif action == "keep_current":

        state[
            "budget_adjustment_attempted"
        ] = True

    return state