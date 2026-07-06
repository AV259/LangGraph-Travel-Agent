from pydantic import BaseModel
from typing import List


class WeatherInfo(BaseModel):

    city: str

    temperature: float

    weather_description: str


class WeatherResponse(BaseModel):

    forecasts: List[WeatherInfo]