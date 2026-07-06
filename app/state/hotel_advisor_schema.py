from pydantic import BaseModel


class HotelRecommendation(BaseModel):

    hotel_name: str

    city: str

    reason: str