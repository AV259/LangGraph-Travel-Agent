from app.agents.flight_agent import flight_agent

state = {
    "departure_city": "Frankfurt",
    "start_date": "2026-07-10",
    "end_date": "2026-07-20",

    "destination_results": [
        {
            "city": "Tokyo"
        }
    ]
}

result = flight_agent(state)

print(result["flight_results"])