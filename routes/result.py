from functools import reduce
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile
from pydantic import BaseModel

from core.result import parse_result
from model import SuccessResponse
from utils import calculate_cgpa, format_error_response, format_response

router = APIRouter()


class CourseResult(BaseModel):
    course_code: str
    title: str
    unit: int
    grade: str
    grade_point: int


class SemesterResult(BaseModel):
    id: str
    courses: list[CourseResult]
    title: str
    gpa: float
    total_grade_points: int
    total_units: int


class ResultData(BaseModel):
    semesters: list[SemesterResult]
    cgpa: float
    total_units: int


@router.post("/result")
async def upload_result(file: UploadFile) -> SuccessResponse[ResultData]:
    try:

        if file.content_type != "application/pdf":
            err_message = "Wrong file format. File must be of type application/pdf"
            return format_error_response(err_message, "INVALID_FILE_TYPE", 400)

        results = parse_result(await file.read())

        return format_response(results)

    except:
        err_message = "Unable to parse result transcript. Please provide a valid document"
        return format_error_response(err_message, "UNPROCESSABLE", 422)
