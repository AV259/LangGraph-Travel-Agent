from pydantic import BaseModel
from typing import List


class FlightOption(BaseModel):
    airline: str
    departure_time: str
    arrival_time: str
    price: float


class FlightResponse(BaseModel):
    flights: List[FlightOption]