import fitz


class InvalidCourseRegistration(Exception):
    """Raised when unable to parse course registration"""
    pass


def parse_course_registration(stream: any) -> list[dict]:
    rows = []
    doc = fitz.open(stream=stream)
    for page in doc:
        tables = page.find_tables()
        rows.extend(tables[2].extract())

    courses = get_courses(rows)

    if len(courses) == 0:
        raise InvalidCourseRegistration

    return courses


def get_courses(rows: list[list[str]]) -> list[dict]:
    courses = []

    for row in rows[1:-1]:  # skip header (first) row and total (last) row

        course = {}
        course["course_code"] = row[0]
        course["title"] = row[1]
        course["unit"] = int(row[2])
        courses.append(course)

    return courses
