from uuid import uuid4
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile
from pydantic import BaseModel

from core.course_reg import parse_course_registration
from model import SuccessResponse
from utils import format_error_response, format_response

router = APIRouter()


class Course(BaseModel):
    course_code: str
    title: str
    unit: int


class CourseRegData(BaseModel):
    courses: list[Course]


@router.post("/course_registration")
async def upload_course_registration(file: UploadFile) -> SuccessResponse[CourseRegData]:
    try:
        if file.content_type != "application/pdf":
            err_message = "Wrong file format. File must be of type application/pdf"
            return format_error_response(err_message, "INVALID_FILE_TYPE", 400)

        courses = parse_course_registration(await file.read())
        return format_response({"courses": courses, "id": str(uuid4())})

    except:
        err_message = "Unable to parse course registration. Please supply a valid document"
        return format_error_response(err_message, "UNPROCESSABLE", 422)
