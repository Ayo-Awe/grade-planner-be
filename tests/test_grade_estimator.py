import unittest
from core.grade_generator import GradeGenerator
from model import FIVE_POINT_GP_SYSTEM, Semester
from utils import calculate_gpa


class TestGradeGenerator(unittest.TestCase):
    def test_should_generate_optimum_estimate(self):
        courses_combo = [
            {
                "course_code": "CEN317",
                "title": "Prototyping Methods",
                "unit": 2,
            },
            {
                "course_code": "EIE311",
                "title": "Electromagnetic Fields & Waves",
                "unit": 3,
            },
            {
                "course_code": "EIE312",
                "title": "Communication Principles",
                "unit": 3,
            },

            {
                "course_code": "DLD111",
                "title": "Foundations of Leadership Development",
                "unit": 0,
            },
            {
                "course_code": "TMC311",
                "title": "Total Man Concept V",
                "unit": 1,
            },
            {
                "course_code": "TMC31",
                "title": "Total Man Concept V",
                "unit": 1,
            },
            {
                "course_code": "TMC312",
                "title": "Total Man Concept -  Sports V",
                "unit": 0,
            }
        ]

        semester = Semester(courses_combo, FIVE_POINT_GP_SYSTEM)
        grade_estimator = GradeGenerator(
            semester.courses, "")

        target_gpa = 4.5

        target_gp_sum = semester.calculate_grade_points_sum(target_gpa)

        results = grade_estimator.generate(target_gp_sum)

        for result in results:
            for courses_combo in result["combos"]:
                gpa = calculate_gpa(courses_combo)
                self.assertEqual(gpa, target_gpa)
                self.assertEqual(len(courses_combo), len(semester.courses))

                combo_course_codes = [course["course_code"]
                                      for course in courses_combo]

                course_codes = [course["course_code"]
                                for course in semester.courses]

                course_codes.sort()
                combo_course_codes.sort()

                self.assertEqual(combo_course_codes, course_codes)

    def test_unattainable_target_gpa(self):
        courses = [
            {
                "course_code": "CEN317",
                "title": "Prototyping Methods",
                "unit": 2,
            },
            {
                "course_code": "EIE311",
                "title": "Electromagnetic Fields & Waves",
                "unit": 3,
            },
            {
                "course_code": "EIE312",
                "title": "Communication Principles",
                "unit": 3,
            },

            {
                "course_code": "DLD111",
                "title": "Foundations of Leadership Development",
                "unit": 0,
            },
            {
                "course_code": "TMC311",
                "title": "Total Man Concept V",
                "unit": 1,
            },
            {
                "course_code": "TMC312",
                "title": "Total Man Concept -  Sports V",
                "unit": 0,
            }
        ]

        semester = Semester(courses, FIVE_POINT_GP_SYSTEM)
        grade_estimator = GradeGenerator(
            semester.courses, "")

        target_gpa = 4.57

        target_gp_sum = semester.calculate_grade_points_sum(target_gpa)

        results = grade_estimator.generate(target_gp_sum)

        self.assertEqual(results, [])

    def test_target_cgpa_greater_than_max_cgpa(self):
        courses = [
            {
                "course_code": "CEN317",
                "title": "Prototyping Methods",
                "unit": 2,
            },
            {
                "course_code": "EIE311",
                "title": "Electromagnetic Fields & Waves",
                "unit": 3,
            },
            {
                "course_code": "EIE312",
                "title": "Communication Principles",
                "unit": 3,
            },

            {
                "course_code": "DLD111",
                "title": "Foundations of Leadership Development",
                "unit": 0,
            },
            {
                "course_code": "TMC311",
                "title": "Total Man Concept V",
                "unit": 1,
            },
            {
                "course_code": "TMC312",
                "title": "Total Man Concept -  Sports V",
                "unit": 0,
            }
        ]

        semester = Semester(courses, FIVE_POINT_GP_SYSTEM)
        grade_estimator = GradeGenerator(
            semester.courses, "")

        target_gpa = 5.5

        target_gp_sum = semester.calculate_grade_points_sum(target_gpa)

        results = grade_estimator.generate(target_gp_sum)

        self.assertEqual(results, [])
