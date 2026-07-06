from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
load_dotenv()

#print(os.getenv("SERP_API_KEY"))

params = {
    "engine": "google_flights",
    "departure_id": "FRA",
    "arrival_id": "HND",
    "outbound_date": "2026-07-10",
    "return_date": "2026-07-20",
    "currency": "EUR",
    "api_key": os.getenv("SERP_API_KEY")
}

search = GoogleSearch(params)

results = search.get_dict()

print(results.keys())

print(results.get("best_flights"))

#print(results.get("error"))