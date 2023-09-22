from typing import TypedDict

class ResultTime(TypedDict):
    start: str
    end: str

class Result(TypedDict):
    studio: str
    program: str
    coach: str
    time: ResultTime
    day: str