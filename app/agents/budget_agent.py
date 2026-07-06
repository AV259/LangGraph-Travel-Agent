from app.state.travel_state import (
    TravelState
)


def budget_agent(
    state: TravelState
):

    duration = state.get(
        "duration",
        0
    )

    budget = state.get(
        "budget",
        0
    )

    selected_flight = state.get("selected_flight") or {}
    selected_hotel = state.get("selected_hotel") or {}

    flight_cost = selected_flight.get("price", 0)

    hotel_cost = selected_hotel.get("total_price", 0)

    food_cost = duration * 30

    transport_cost = duration * 5

    activity_cost = duration * 6

    total_cost = (
        flight_cost
        + hotel_cost
        + food_cost
        + transport_cost
        + activity_cost
    )

    remaining_budget = (
        budget - total_cost
    )

    suggestions = []
    state["budget_suggestions"] =[]

    if remaining_budget < 0:

        current_flight_price = selected_flight.get("price", 0)

        current_hotel_price = selected_hotel.get("total_price", 0)

        # cheaper flights

        for flight in (
            state["flight_results"]
        ):

            savings = (
                current_flight_price
                - flight["price"]
            )

            if savings > 0:

                suggestions.append(
                    {
                        "type":
                            "flight",

                        "savings":
                            savings,

                        "option":
                            flight
                    }
                )

        # cheaper hotels

        for hotel in (
            state["hotel_results"]
        ):

            savings = (
                current_hotel_price
                - hotel["total_price"]
            )

            if savings > 0:

                suggestions.append(
                    {
                        "type":
                            "hotel",

                        "savings":
                            savings,

                        "option":
                            hotel
                    }
                )

    state["budget_summary"] = {

        "total_cost":
            total_cost,

        "remaining_budget":
            remaining_budget,

        "budget_status":
            (
                "within_budget"
                if remaining_budget >= 0
                else "over_budget"
            )
    }

    state[
        "budget_suggestions"
    ] = sorted(
        suggestions,
        key=lambda x: x["savings"],
        reverse=True
    )[:5]

    return state