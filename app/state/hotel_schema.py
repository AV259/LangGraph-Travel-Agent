from pydantic import BaseModel
from typing import List


class HotelOption(BaseModel):

    name: str

    price_per_night: float

    total_price: float

    rating: float

    amenities: List[str]


class HotelResponse(BaseModel):
    hotels: List[HotelOption]