from functools import reduce
from uuid import uuid4
import fitz

from utils import calculate_cgpa


class InvalidResult(Exception):
    """Raised when unable to parse results
    """
    pass


def parse_result(stream: any) -> list[list[dict]]:
    rows = []
    doc = fitz.open(stream=stream)
    for page in doc:
        tables = page.find_tables()
        rows.extend(tables[0].extract())

    rows = clean_result(rows)
    semesters = get_semesters(rows)
    cgpa = round(calculate_cgpa(semesters), 2)
    total_units = reduce(lambda sum, sem: sum +
                         sem["total_units"], semesters, 0)

    if len(semesters) == 0:
        raise InvalidResult

    return {"semesters": semesters, "cgpa": cgpa, "total_units": total_units}


def get_semesters(rows: list[list[str]]) -> list[dict]:
    semesters = []
    current_semester = None

    for row in rows:
        is_new_semster = row[0].lower().find("semester") > -1

        if is_new_semster:
            if current_semester is not None:
                semesters.append(current_semester)
            current_semester = {"courses": [], "title": row[0]}
            continue

        course = {}

        course["course_code"] = row[0]
        course["title"] = clean_title(row[1])
        course["unit"] = int(row[2])
        course["grade"] = row[3]
        course["grade_point"] = int(row[4])

        if course["title"].lower() == "total":
            current_semester["id"] = str(uuid4())
            current_semester["total_units"] = course["unit"]
            current_semester["total_grade_points"] = course["grade_point"]
            current_semester["gpa"] = round(
                current_semester["total_grade_points"]/current_semester["total_units"], 2)

            continue

        current_semester["courses"].append(course)

    semesters.append(current_semester)

    return semesters


def clean_result(rows: list[list[str]]) -> list[list[str]]:
    filtered_rows = filter(lambda row: is_header(row) == False, rows)
    return list(filtered_rows)


def clean_title(title: str) -> str:
    return title.replace("\n", " ").replace("\u2013", "- ")


def is_header(row: list[str]) -> bool:
    is_column_header = row[0].lower().find("course") > -1
    is_page_header = row[0].lower().find("transcript") > -1

    return is_column_header or is_page_header
