from app.state.travel_state import TravelState
from app.services.gemini_service import llm
from langgraph.types import interrupt


def follow_up_agent(state: TravelState):

    missing_fields = state["missing_fields"]
    
    response = llm.invoke(
        f"""
        The user wants to plan a trip.

        Missing information:
        {missing_fields}

        Ask a friendly follow-up question
        requesting ONLY the missing information.
        """
    )

    state["follow_up_question"] = response.content

    user_follow_up = interrupt(
        {
            "message": response.content,
            "missing_fields": missing_fields,
            "type": "follow_up",
        }
    )

    if user_follow_up:
        state["user_input"] = (
            f"{state.get('user_input', '')}\n\nAdditional details from user:\n{user_follow_up}"
        )

    state["trip_complete"] = False

    return state