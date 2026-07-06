from pydantic import BaseModel
from typing import List


class Activity(BaseModel):

    name: str

    reason: str

class DestinationActivities(BaseModel):

    destination: str

    activities: List[Activity]


class ActivityResponse(BaseModel):

    destinations: List[DestinationActivities]
