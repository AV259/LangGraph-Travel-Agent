from typing import TypedDict, Optional, List, Dict

class TravelState(TypedDict):
    user_input: str
    destination: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    budget: Optional[float]
    departure_city: Optional[str]
    interests: Optional[List[str]]
    duration: Optional[int]

    memory_context: List[str]

    destination_results: List[Dict]
    flight_results: List[Dict]
    hotel_results: List[Dict]
    activity_results: List[Dict]
    restaurant_results: List[Dict]
    budget_results: Dict

    missing_fields: List[str]

    follow_up_question: Optional[str]

    trip_complete: bool

    recommended_flight: Dict | None

    selected_flight: Dict | None

    flight_selection_required: bool

    recommended_hotel: Optional[Dict]

    selected_hotel: Optional[Dict]

    hotel_selection_required: bool

    budget_summary: Optional[Dict]

    budget_suggestions: List[Dict]

    budget_recommendation: Optional[Dict]

    budget_decision_required: bool

    budget_decision: Optional[Dict]

    budget_adjustment_attempted: bool

    destinations_display_shown: bool

    secondary_hotels: List[Dict]

    transport_suggestions: List[Dict]

    itinerary: Optional[Dict]

    formatted_itinerary: Optional[str]

    