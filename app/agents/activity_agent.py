from app.state.travel_state import TravelState

from app.state.activity_schema import (
    ActivityResponse
)

from app.services.gemini_service import llm

from app.tools.serp_search_tool import (
    search_activities
)


def activity_agent(state: TravelState):

    city_data = []

    for destination_data in state["destination_results"]:
        
        destination = (
        destination_data["destination"]
    )

        interests = state.get(
        "interests",
        []
    )

        query = (
            f"Top attractions, experiences, landmarks, "
            f"nature spots, food experiences, and tourist "
            f"activities in {destination} for travelers interested in "
            f"{', '.join(interests)}"
        )

        search_results = search_activities(
        query
    )

        city_data.append(
        {
            "destination": destination,
            "search_results": search_results
        }
    )

    structured_llm = llm.with_structured_output(
        ActivityResponse
    )

    response = structured_llm.invoke(
        f"""
    You are an expert travel activity planner.

    Traveler Interests:
    {state.get("interests")}

    Traveler Preferences:
    {state.get("memory_context")}

    Search Results:
    {city_data}

    TASK:

    For each destination:

    - Recommend 4-6 activities.
    - Use the search results as the primary source.
    - Prioritize activities matching the traveler's interests.
    - Include a mix of sightseeing, local experiences,
      food experiences, nature experiences, cultural experiences,
      and iconic attractions when relevant.
    - Avoid generic recommendations.
    - Do not recommend the destination itself as an activity.
    - Recommend actual places, attractions, experiences,
      museums, landmarks, beaches, food districts,
      hiking areas, tours, or cultural activities.
    - Explain briefly in 2-3 sentences why each activity is a good fit.

    Return structured output only.
    """
    )

    state["activity_results"] = [
    destination.model_dump()
    for destination in response.destinations
]

    return state