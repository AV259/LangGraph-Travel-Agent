from pydantic import BaseModel


class FlightRecommendation(BaseModel):

    airline: str

    arrival_airport: str

    reason: str