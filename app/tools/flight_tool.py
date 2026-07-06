from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

def search_flights(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
    return_date: str
):

    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "return_date": return_date,
        "currency": "EUR",
        "api_key": os.getenv(
            "SERP_API_KEY"
        )
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    #print("Response Keys:", results.keys())

    if "error" in results:
     print("SERP API ERROR:")
     print(results["error"])

    '''print(
    "Best Flights Count:",
    len(results.get("best_flights", []))
)

    print(
    "Other Flights Count:",
    len(results.get("other_flights", []))
)'''

    flights = []

    for option in results.get(
        "best_flights",
        []
    )[:5]:

        first_leg = option["flights"][0]
        last_leg = option["flights"][-1]
        
        # Extract layover information
        layovers_info = []
        if "layovers" in option and option["layovers"]:
            for layover in option["layovers"]:
                layovers_info.append({
                    "airport": layover.get("name", "Unknown"),
                    "airport_id": layover.get("id", ""),
                    "duration_minutes": layover.get("duration", 0),
                    "overnight": layover.get("overnight", False)
                })
        
        # Extract flight segments
        segments_info = []
        for idx, leg in enumerate(option["flights"]):
            segments_info.append({
                "leg_number": idx + 1,
                "from": leg["departure_airport"]["id"],
                "to": leg["arrival_airport"]["id"],
                "departure": leg["departure_airport"]["time"],
                "arrival": leg["arrival_airport"]["time"],
                "airline": leg["airline"],
                "flight_number": leg.get("flight_number", ""),
                "duration_minutes": leg["duration"],
                "airplane": leg.get("airplane", ""),
                "travel_class": leg.get("travel_class", "")
            })

        flights.append(
            {
                "airline":
                    first_leg["airline"],

                "departure_time":
                    first_leg[
                        "departure_airport"
                    ]["time"],
                
                "departure_airport":
                    first_leg["departure_airport"]["id"],

                "arrival_time":
                    last_leg[
                        "arrival_airport"
                    ]["time"],
                
                "arrival_airport":
                    last_leg["arrival_airport"]["id"],
                
                "arrival_airport_name":
                    last_leg["arrival_airport"]["name"],

                "price":
                    option["price"],

                "total_duration":
                    option[
                        "total_duration"
                    ],

                "flight_type":
                    option["type"],
                
                "layovers": layovers_info,
                
                "segments": segments_info,
                
                "num_stops": len(option["flights"]) - 1
            }
        )

    return flights