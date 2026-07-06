from serpapi import GoogleSearch
import os

def search_activities(query: str):

    params = {
        "engine": "google",
        "q": query,
        "api_key": os.getenv("SERP_API_KEY"),
        "num": 5
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    return results.get(
        "organic_results",
        []
    )