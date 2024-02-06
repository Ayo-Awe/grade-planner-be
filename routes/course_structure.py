from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile
from pydantic import BaseModel

from core.course_structure import parse_course_structure
from model import SuccessResponse
from utils import format_error_response, format_response

router = APIRouter()


class Course(BaseModel):
    course_code: str
    title: str
    unit: int
    is_elective: bool


class Semester(BaseModel):
    courses: list[Course]
    title: str
    total_units: int
    elective_units: Optional[int]


class CourseStructureResponse(BaseModel):
    semesters: list[Semester]


@router.post("/course_structure")
async def upload_course_registration(file: UploadFile) -> SuccessResponse[CourseStructureResponse]:
    try:
        if file.content_type != "application/pdf":
            err_message = "Wrong file format. File must be of type application/pdf"
            return format_error_response(err_message, "INVALID_FILE_TYPE", 400)

        semesters = parse_course_structure(await file.read())
        return format_response({"semesters": semesters})

    except:
        err_message = "Unable to parse course structure. Please provide a valid document"
        return format_error_response(err_message, "UNPROCESSABLE", 422)
