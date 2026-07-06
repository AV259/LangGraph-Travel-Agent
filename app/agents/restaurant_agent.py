from app.state.travel_state import TravelState
from app.state.restaurant_schema import RestaurantRecommendations
from app.services.gemini_service import llm
from app.tools.restaurant_tool import search_restaurants_detailed


def restaurant_agent(state: TravelState):
    """
    Recommends restaurants for each destination based on user interests.
    Uses SerpAPI to find real restaurants and LLM to match them with interests.
    """

    destinations = state.get("destination_results", [])
    interests = state.get("interests", [])

    if not destinations:
        state["restaurant_results"] = []
        return state

    # Search for restaurants in each destination
    restaurant_data = []

    for destination_info in destinations:
        destination_name = destination_info.get("destination")

        # Determine cuisine preferences based on user interests
        cuisine_prefs = ["local"]
        if "food" in interests:
            cuisine_prefs.extend(["vegetarian", "fine dining"])

        # Search restaurants
        restaurants = search_restaurants_detailed(
            destination=destination_name,
            cuisine_preferences=cuisine_prefs
        )

        restaurant_data.append(
            {
                "destination": destination_name,
                "search_results": restaurants,
            }
        )

    structured_llm = llm.with_structured_output(
        RestaurantRecommendations
    )

    response = structured_llm.invoke(
        f"""
You are an expert food and travel guide.

Traveler Interests:
{interests}

Traveler Preferences:
{state.get("memory_context")}

Restaurant Search Results:
{restaurant_data}

TASK:

For each destination, recommend 3-4 restaurants that match the traveler's interests.

For each restaurant:

1. destination: The city name
2. name: Actual restaurant name from search results
3. cuisine_type: Type of cuisine (local, vegetarian, fine dining, street food, fusion, etc.)
4. reason: 2-3 sentences explaining why this restaurant matches the traveler (based on interests)
5. best_for: Meal type (Breakfast, Lunch, Dinner, Street Food, Snacks)

IMPORTANT RULES:

- Use restaurant names from the search results provided
- Match recommendations with traveler interests
- Include diverse meal types (breakfast, lunch, dinner)
- Explain how each restaurant relates to the traveler's interests (food, culture, nature, etc.)
- If the traveler loves "food", prioritize authentic and highly-rated options
- If the traveler loves "culture/history", choose restaurants with cultural significance

Return structured output only.
"""
    )

    state["restaurant_results"] = [
        restaurant.model_dump() for restaurant in response.destinations
    ]

    return state
