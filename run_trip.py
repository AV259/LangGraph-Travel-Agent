from langgraph.types import Command

from app.graph.travel_graph import travel_graph

config = {
        "configurable": {
        "thread_id": "user_1"
        }
        }

state = {
        "user_input": input(
        "Describe your trip:\n\n"
        ),
        "budget_adjustment_attempted": False
        }

result = travel_graph.invoke(
        state,
        config=config
        )

while "__interrupt__" in result:

        interrupt_data = (
            result["__interrupt__"][0].value
        )

        print("\n")
        print("=" * 60)
        print(interrupt_data["message"])
        print("=" * 60)

# Destination Display

        if "destinations" in interrupt_data:

            destinations = interrupt_data["destinations"]

            for dest in destinations:
                print(f"\n {dest['name'].upper()}")
                print(f"   Nearest Airport: {dest['airport_city']}")
                print(f"   Why: {dest['reason']}")
                print(f"\n   Activities:")
                for activity in dest.get('activities', [])[:4]:
                    print(f"   • {activity.get('name')}: {activity.get('reason')}")

            print("\n Great! Now let's continue with flight selection...")

            # Continue without user input (just acknowledge)
            result = travel_graph.invoke(
                Command(
                    resume=True
                ),
                config=config
            )

            continue

# Flight Selection

        if "flights" in interrupt_data:

            flights = interrupt_data["flights"]

            print("\nRecommended Flight:\n")

            rec_flight = interrupt_data.get("recommended_flight", {})
            print(f"  Airline: {rec_flight.get('airline', 'N/A')}")
            print(f"  Arrival Airport: {rec_flight.get('arrival_airport', 'N/A')}")
            print(f"  Why: {rec_flight.get('reason', 'N/A')}")

            print("\nAvailable Flights:\n")

            for idx, flight in enumerate(
                flights,
                start=1
            ):
                arrival_info = f"{flight.get('arrival_airport_name', 'N/A')} ({flight.get('arrival_airport', 'N/A')})"
                num_stops = flight.get('num_stops', 0)
                stops_text = f", {num_stops} stop(s)" if num_stops > 0 else ", Direct"
                
                print(
                    f"{idx}. "
                    f"{flight['airline']} → {arrival_info}{stops_text} | "
                    f"€{flight['price']} | "
                    f"{flight['total_duration']} mins"
                )

            choice = int(
                input(
                    "\nChoose flight number: "
                )
            )

            selected = flights[
                choice - 1
            ]

            result = travel_graph.invoke(
                Command(
                    resume=selected
                ),
                config=config
            )

            continue

# Hotel Selection

        if "hotels" in interrupt_data:

            hotels = interrupt_data["hotels"]

            # Handle empty hotel list
            if not hotels or len(hotels) == 0:
                print("\n  No hotels found for the selected destination.")
                print("Continuing with default hotel selection...")
                
                result = travel_graph.invoke(
                    Command(
                        resume=None
                    ),
                    config=config
                )
                continue

            print("\nRecommended Hotel:\n")

            rec_hotel = interrupt_data.get("recommended", {})
            print(f"  Hotel: {rec_hotel.get('hotel_name', 'N/A')}")
            print(f"  City: {rec_hotel.get('city', 'N/A')}")
            print(f"  Why: {rec_hotel.get('reason', 'N/A')}")

            print("\nAvailable Hotels:\n")

            for idx, hotel in enumerate(
                hotels,
                start=1
            ):

                print(
                    f"{idx}. "
                    f"{hotel['name']} | "
                    f"€{hotel['total_price']} | "
                    f"Rating: {hotel['rating']}"
                )

            choice = int(
                input(
                    "\nChoose hotel number: "
                )
            )

            selected = hotels[
                choice - 1
            ]

            result = travel_graph.invoke(
                Command(
                    resume=selected
                ),
                config=config
            )

            continue

# Budget Decision

        if "valid_actions" in interrupt_data:

            print(
                "\nBudget Summary:\n"
            )

            print(
                interrupt_data[
                    "budget_summary"
                ]
            )

            print(
                "\nAI Advisor Recommendation:\n"
            )

            print(
                interrupt_data[
                    "advisor_recommendation"
                ]
            )

            suggestions = (
                interrupt_data[
                    "suggestions"
                ]
            )

            print(
                "\nSavings Suggestions:\n"
            )

            for idx, suggestion in enumerate(
                suggestions,
                start=1
            ):

                print(
                    f"{idx}. "
                    f"{suggestion['type']} | "
                    f"Saves €{suggestion['savings']}"
                )

            print("\nActions:")

            print(
                "1. Switch Hotel"
            )

            print(
                "2. Switch Flight"
            )

            print(
                "3. Keep Current"
            )

            action = input(
                "\nChoose action: "
            )

            if action == "1":

                hotel_options = [
                    s
                    for s in suggestions
                    if s["type"] == "hotel"
                ]

                if not hotel_options:

                    print(
                        "No cheaper hotels available."
                    )

                    decision = {
                        "action":
                            "keep_current"
                    }

                else:

                    print(
                        "\nCheaper Hotels:\n"
                    )

                    for idx, option in enumerate(
                        hotel_options,
                        start=1
                    ):

                        hotel = option[
                            "option"
                        ]

                        print(
                            f"{idx}. "
                            f"{hotel['name']} | "
                            f"€{hotel['total_price']}"
                        )

                    choice = int(
                        input(
                            "\nChoose hotel: "
                        )
                    )

                    decision = {
                        "action":
                            "switch_hotel",

                        "option":
                            hotel_options[
                                choice - 1
                            ]["option"]
                    }

            elif action == "2":

                flight_options = [
                    s
                    for s in suggestions
                    if s["type"] == "flight"
                ]

                if not flight_options:

                    print(
                        "No cheaper flights available."
                    )

                    decision = {
                        "action":
                            "keep_current"
                    }

                else:

                    print(
                        "\nCheaper Flights:\n"
                    )

                    for idx, option in enumerate(
                        flight_options,
                        start=1
                    ):

                        flight = option[
                            "option"
                        ]

                        print(
                            f"{idx}. "
                            f"{flight['airline']} | "
                            f"€{flight['price']}"
                        )

                    choice = int(
                        input(
                            "\nChoose flight: "
                        )
                    )

                    decision = {
                        "action":
                            "switch_flight",

                        "option":
                            flight_options[
                                choice - 1
                            ]["option"]
                    }

            else:

                decision = {
                    "action":
                        "keep_current"
                }

            result = travel_graph.invoke(
                Command(
                    resume=decision
                ),
                config=config
            )

            continue

print("\n")

print("=" * 70)
print("SELECTED FLIGHT".center(70))
print("=" * 70)

flight = result.get("selected_flight")
if flight:
    print(f"Airline: {flight.get('airline', 'N/A')}")
    print(f"Departure: {flight.get('departure_time', 'N/A')}")
    print(f"Arrival: {flight.get('arrival_time', 'N/A')}")
    print(f"Duration: {flight.get('total_duration', 'N/A')} minutes")
    print(f"Price: €{flight.get('price', 'N/A')}")
else:
    print("No flight selected")

print("\n")

print("=" * 70)
print("SELECTED HOTEL".center(70))
print("=" * 70)

hotel = result.get("selected_hotel")
if hotel:
    print(f"Hotel: {hotel.get('name', 'N/A')}")
    print(f"Rating:  {hotel.get('rating', 'N/A')}")
    print(f"Price per Night: €{hotel.get('price_per_night', 'N/A')}")
    print(f"Total Price: €{hotel.get('total_price', 'N/A')}")
    amenities = hotel.get("amenities", [])
    if amenities:
        print(f"Amenities: {', '.join(amenities)}")
else:
    print("No hotel selected")

print("\n")

print("=" * 70)
print("BUDGET SUMMARY".center(70))
print("=" * 70)

budget = result.get("budget_summary")
if budget:
    print(f"Total Cost: €{budget.get('total_cost', 'N/A')}")
    print(f"Remaining Budget: €{budget.get('remaining_budget', 'N/A')}")
    print(f"Status: {budget.get('budget_status', 'N/A').upper()}")
else:
    print("No budget information available")


print("\n")

print("=" * 70)
print("ITINERARY".center(70))
print("=" * 70)

formatted = result.get(
    "formatted_itinerary",
    ""
)

if formatted:
    print(formatted)
else:
    print("No itinerary available")

