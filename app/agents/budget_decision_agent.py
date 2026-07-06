from langgraph.types import interrupt

from app.state.travel_state import (
    TravelState
)


def budget_decision_agent(
    state: TravelState
):

    if (
        state["budget_summary"]
        ["budget_status"]
        == "within_budget"
    ):
        return state

    state[
        "budget_decision_required"
    ] = True

    decision = interrupt(
    {
        "message":
            "Your trip exceeds budget",

        "budget_summary":
            state["budget_summary"],

        "advisor_recommendation":
            state[
                "budget_recommendation"
            ],
        "valid_actions": [
                "switch_hotel",
                "switch_flight",
                "keep_current"
            ],

        "suggestions":
            state[
                "budget_suggestions"
            ]
    }
)

    state[
        "budget_decision"
    ] = decision

    state[
        "budget_decision_required"
    ] = False

    return state