from pydantic import BaseModel
from typing import List


class DayPlan(BaseModel):

    day: int

    morning: str

    afternoon: str

    evening: str


class ItineraryResponse(BaseModel):

    trip_summary: str

    flight_summary: str

    hotel_summary: str

    budget_summary: str

    travel_tips: List[str]

    days: List[DayPlan]