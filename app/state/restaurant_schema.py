from pydantic import BaseModel
from typing import List


class Restaurant(BaseModel):
    destination: str
    name: str
    cuisine_type: str
    reason: str
    best_for: str  # e.g., "Breakfast", "Lunch", "Dinner", "Street Food"


class RestaurantRecommendations(BaseModel):
    destinations: List[Restaurant]
