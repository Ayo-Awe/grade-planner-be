from pydantic import BaseModel
from typing import Generic, TypeVar
from functools import reduce

from utils import invert_dict

FIVE_POINT_GP_SYSTEM = {
    5: "A",
    4: "B",
    3: "C",
    2: "D",
    # 0: "F"
}

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    status: str
    data: T


class Semester:
    def __init__(self, courses: list[dict], grade_point_system: dict) -> None:
        self.courses = courses
        self.course_units = list(
            map(lambda course: course["unit"], self.courses))

        self.credit_courses = list(
            filter(lambda course: course["unit"] > 0, self.courses))
        self.credit_course_units = list(
            map(lambda course: course["unit"], self.credit_courses))

        self.total_units = reduce(
            lambda sum, course: sum + course["unit"], courses, 0)

        self.grade_point_system = grade_point_system

    def calculate_grade_points_sum(self, grade_point_average: float) -> int:
        return round(grade_point_average * self.total_units)

    def calculate_cgpa(self, grade_point_sum: int) -> float:
        return grade_point_sum/self.total_units

    def grades_to_courses(self, grades: list[int], credit_courses_only=True) -> list[dict]:
        courses = self.credit_courses if credit_courses_only == True else self.courses

        graded_courses = []

        inverted_gp_lookup = invert_dict(self.grade_point_system)

        for grade, course in zip(grades, courses):
            c = course.copy()
            c["grade_int"] = grade
            c["grade"] = inverted_gp_lookup(grade)
            graded_courses.append(c)

        return graded_courses

    def grade_points_to_grades(self, grades_points: list[int], credit_courses_only=True) -> list[int]:
        course_units = self.credit_course_units if credit_courses_only == True else self.course_units

        grades = []

        for grade_point, course_unit in zip(grades_points, course_units):
            grades.append(grade_point/course_unit)

        return grades
