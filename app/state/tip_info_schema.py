from pydantic import BaseModel, Field
from typing import Optional, List


class TripInfo(BaseModel):
    destination: Optional[str] = None
    departure_city: Optional[str] = None
    duration: Optional[int] = None
    start_date: Optional[str] = Field(
    default=None,
    description="Travel start date in YYYY-MM-DD format")
    end_date: Optional[str] = Field(
    default=None,
    description="Travel end date in YYYY-MM-DD format")
    budget: Optional[float] = None
    interests: List[str] = []
    