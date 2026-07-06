from pydantic import BaseModel
from typing import List


class DestinationRecommendation(BaseModel):

    destination: str

    airport_city: str

    reason: str


class DestinationResponse(BaseModel):

    recommendations: List[DestinationRecommendation]