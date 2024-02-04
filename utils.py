from typing import Any
from fastapi.responses import JSONResponse


def invert_dict(dic: dict) -> dict:
    """swaps the place of a dictionary's key and value e.g
    {"a":1} => {1:"a"}
    """
    return dict([(value, key) for key, value in dict.items()])


def calculate_gpa(graded_courses: list[dict]) -> float:
    gp_sum = 0
    total_units = 0

    for gc in graded_courses:
        gp_sum += gc["unit"] * gc["grade_int"]
        total_units += gc["unit"]

    return gp_sum/total_units


def format_error_response(message: str, code: str, status_code=500,) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={
        "status": "error",
        "code": code,
        "message": message
    })


def format_response(data: Any, status_code=200) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={
        "status": "success",
        "data": data
    })
