from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")


class Course(BaseModel):
    course_code: str
    title: str
    unit: int


class CourseResult(BaseModel):
    course_code: str
    title: str
    unit: int
    grade: str
    grade_point: int


class Semester(BaseModel):
    courses: list[CourseResult]
    title: str
    gpa: float
    total_grade_points: int
    total_units: int


class SuccessResponse(BaseModel, Generic[T]):
    status: str
    data: T


class CourseRegData(BaseModel):
    courses: list[Course]


class ResultData(BaseModel):
    semesters: list[Semester]
