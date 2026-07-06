from app.state.travel_state import TravelState
from app.state.tip_info_schema import TripInfo
from app.services.gemini_service import llm
from app.utils.trip_validation import get_missing_fields
from datetime import datetime

current_year = datetime.now().year

def trip_intake_agent(state: TravelState):
    user_input = state['user_input']

    structured_llm = llm.with_structured_output(TripInfo)

    result = structured_llm.invoke(
        f"""
    Extract trip information from the user request.

    IMPORTANT:
- Return start_date and end_date in YYYY-MM-DD format.
- Current year is {current_year}.
- If user provides month/day but no year, assume year {current_year}.
- Never return dates in the past.
- Return null for unknown fields.

    User Request:
    {user_input}
    Return only the structured fields. """)
    
    if result.destination:
     state["destination"] = result.destination

    if result.departure_city:
     state["departure_city"] = result.departure_city

    if result.duration:
     state["duration"] = result.duration

    if result.start_date:
     state["start_date"] = result.start_date

    if result.end_date:
     state["end_date"] = result.end_date

    if result.budget:
     state["budget"] = result.budget

    if result.interests:
     state["interests"] = result.interests
    
    state["missing_fields"] = get_missing_fields(state)

    return state

