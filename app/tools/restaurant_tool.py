from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()


def search_restaurants(
    destination: str,
    cuisine_type: str = "local",
    num_results: int = 8
):
    """
    Search for restaurants in a destination using SerpAPI.
    
    Returns:
        List of restaurant dictionaries with name, rating, type, and address
    """
    
    params = {
        "engine": "google",
        "q": f"best {cuisine_type} restaurants in {destination}",
        "type": "search",
        "api_key": os.getenv("SERP_API_KEY")
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        restaurants = []

        # Extract from organic results
        for result in results.get("organic_results", [])[:num_results]:
            
            try:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                link = result.get("link", "")

                # Skip if not a restaurant
                if any(skip in title.lower() for skip in ["map", "yelp", "tripadvisor"]):
                    continue

                restaurants.append(
                    {
                        "name": title,
                        "description": snippet,
                        "link": link,
                        "type": cuisine_type
                    }
                )

            except Exception:
                continue

        return restaurants[:num_results]

    except Exception as e:
        print(f"Error searching restaurants: {str(e)}")
        return []


def search_restaurants_detailed(
    destination: str,
    cuisine_preferences: list = None
):
    """
    Search for multiple types of restaurants based on user preferences.
    
    Returns:
        Dictionary with restaurant types as keys and restaurant lists as values
    """
    
    if cuisine_preferences is None:
        cuisine_preferences = ["local", "vegetarian", "fine dining"]

    all_restaurants = {}

    for cuisine in cuisine_preferences[:3]:  
        restaurants = search_restaurants(
            destination=destination,
            cuisine_type=cuisine,
            num_results=3
        )
        if restaurants:
            all_restaurants[cuisine] = restaurants

    return all_restaurants
