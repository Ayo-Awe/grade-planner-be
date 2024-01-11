import fitz


def parse_course_registration(stream: any) -> list[dict]:
    rows = []
    doc = fitz.open(stream=stream)
    for page in doc:
        tables = page.find_tables()
        rows.extend(tables[2].extract())

    courses = get_courses(rows)
    return courses


def get_courses(rows: list[list[str]]) -> list[dict]:
    courses = []

    for row in rows[1:-1]:  # skip header and total row

        course = {}
        course["course_code"] = row[0]
        course["title"] = row[1]
        course["unit"] = int(row[2])
        courses.append(course)

    return courses
