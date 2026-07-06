def budget_status_router(
    state
):

    status = (
        state["budget_summary"]
        ["budget_status"]
    )

    attempted = state.get(
        "budget_adjustment_attempted",
        False
    )

    if status == "within_budget":
        return "itinerary"

    if attempted:
        return "itinerary"

    return "budget_decision"