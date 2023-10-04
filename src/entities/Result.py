from typing import TypedDict

class SchedulingResultTime(TypedDict):
    start: str
    end: str

class SchedulingResult(TypedDict):
    studio: str
    program: str
    coach: str
    time: SchedulingResultTime
    day: str

class ForecastResult(TypedDict):
    date: str
    studio: str
    location: str
    program: str
    capacity: float
    capacity_lower: float
    capacity_upper: float