from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from core.grade_generator import GradeGenerator

from model import FIVE_POINT_GP_SYSTEM, Semester, SuccessResponse
from utils import calculate_gpa, format_error_response, format_response

router = APIRouter()


class Course(BaseModel):
    course_code: str
    title: str
    unit: int


class TargetSemester(BaseModel):
    courses: list[Course]


class GenerateGradesRequest(BaseModel):
    target_cgpa: float
    semester: TargetSemester


class GeneratedCourse(BaseModel):
    course_code: str
    title: str
    unit: int
    grade: str


class Pattern(BaseModel):
    pattern: dict
    generated_grades: list[GeneratedCourse]


class GenerateGradesResponse(BaseModel):
    patterns: list[Pattern]
    generated_gpa: float


@router.post("/generate_grades")
async def generate_grades(request: GenerateGradesRequest) -> GenerateGradesResponse:
    # get target grade points
    req = request.model_dump()
    semester = req["semester"]
    semester = Semester(semester["courses"], FIVE_POINT_GP_SYSTEM)

    if request.target_cgpa > 5:
        return format_error_response("Target CGPA must be less than or equal to 5", "INVALID_TARGET_CGPA", 400)

    target_gp_sum = semester.calculate_grade_points_sum(
        request.target_cgpa)

    generator = GradeGenerator(semester.courses, "")
    patterns = generator.generate(target_gp_sum)

    if len(patterns) == 0:
        err_message = "There a no valid grade combinations for your specified requirements"
        return format_error_response(err_message, "NO_VALID_GRADE_COMBINATION", 422)

    generated_gpa = round(calculate_gpa(patterns[0]["generated_grades"]), 2)

    return format_response({"patterns": patterns, "generated_gpa": generated_gpa})
