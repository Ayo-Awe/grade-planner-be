from uuid import uuid4
import fitz
import re


def parse_course_structure(stream: any) -> tuple[list[dict], list[str]]:
    rows = []
    doc = fitz.open(stream=stream)
    text = ""

    for page in doc:
        text += page.get_text()
        tables = page.find_tables()
        for table in tables:
            rows.extend(table.extract())

    titles = re.compile(
        r"\d00 Level In (?:Omega|Alpha) Semester").findall(text)

    semesters = []

    for semester, title in zip(get_semesters(rows), titles):
        semester["title"] = title.replace("In ", "")
        semester["id"] = str(uuid4())
        semesters.append(semester)

    return semesters


def get_semesters(rows: list[list[str]]) -> list[dict]:
    semesters = []
    current_semester = None

    for row in rows:
        is_new_semster = is_header(row)

        if is_new_semster:
            if current_semester is not None:
                semesters.append(current_semester)

            # Reset current semester
            current_semester = {"courses": []}
            continue

        if is_total_row(row):

            if row[0].lower() == "elective total":
                elective_units = 0 if row[3] == '' else int(row[3])
                current_semester["elective_units"] = elective_units

            continue

        course = {}

        course["course_code"] = row[0]
        course["title"] = clean_title(row[1])
        course["unit"] = int(row[2])
        course["is_elective"] = row[3].lower().strip() == "e"

        current_semester["courses"].append(course)

    semesters.append(current_semester)

    return semesters


def clean_title(title: str) -> str:
    return title.replace("\n", " ").replace("\u2013", "- ")


def is_header(row: list[str]) -> bool:
    return row[0].lower().find("course") > -1


def is_total_row(row: list[str]) -> bool:
    return row[0].lower().find("total") > -1
