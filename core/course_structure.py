import fitz


def parse_course_structure(stream: any) -> list[dict]:
    rows = []
    doc = fitz.open(stream=stream)
    for page in doc:
        tables = page.find_tables()
        for table in tables:
            rows.extend(table.extract())

    return get_semesters(rows)


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
