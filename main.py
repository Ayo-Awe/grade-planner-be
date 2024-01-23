from core.result import parse_result
from core.course_reg import parse_course_registration
from core.course_structure import parse_course_structure
from core.grade_estimator import GradeEstimator

from fastapi import FastAPI,  UploadFile
from fastapi.responses import JSONResponse
from model import SuccessResponse, CourseRegData, ResultData, EstimateGradeRequest
from functools import reduce


app = FastAPI()


@app.post("/api/v1/course_reg")
async def upload_course_registration(file: UploadFile) -> SuccessResponse[CourseRegData]:
    try:
        if file.content_type != "application/pdf":
            return JSONResponse(status_code=400, content={"status": "error",
                                                          "message": "Wrong file format. File must be of type application/pdf"})

        courses = parse_course_registration(await file.read())
        return {"status": "success", "data": {"courses": courses}}
    except:
        return JSONResponse(status_code=400, content={"status": "error",
                                                      "message": "Unable to parse course registration"})


@app.post("/api/v1/course_structure")
async def upload_course_registration(file: UploadFile):
    try:
        if file.content_type != "application/pdf":
            return JSONResponse(status_code=400, content={"status": "error",
                                                          "message": "Wrong file format. File must be of type application/pdf"})

        semesters = parse_course_structure(await file.read())
        return {"status": "success", "data": {"semesters": semesters}}
    except:
        return JSONResponse(status_code=400, content={"status": "error",
                                                      "message": "Unable to parse course registration"})


@app.post("/api/v1/result")
async def upload_result(file: UploadFile) -> SuccessResponse[ResultData]:
    try:

        if file.content_type != "application/pdf":
            return JSONResponse(status_code=400, content={"status": "error",
                                                          "message": "Wrong file format. File must be of type application/pdf"})

        semesters = parse_result(await file.read())
        return {"status": "success", "data": {"semesters": semesters}}
    except:
        return JSONResponse(status_code=400, content={"status": "error",
                                                      "message": "Unable to parse course registration"})


@app.post("/api/v1/estimate")
async def estimate_grades(er: EstimateGradeRequest):
    # get target grade points
    req = er.model_dump()
    semesters = req["new_semesters"]
    new_semester_units = 0

    for i, semester in enumerate(semesters):
        tu = reduce(lambda x, y: x + y["unit"], semester["courses"], 0)
        new_semester_units += tu
        semesters[i]["total_units"] = tu

    total_units = req["current_units"] + new_semester_units
    target_gp = (total_units * req["target_cgpa"]) - \
        (req["current_units"] * req["cgpa"])

    res = []

    for semester in semesters:
        estimator = GradeEstimator(semester["courses"], "")
        weighted_dist = round(
            target_gp * (semester["total_units"]/new_semester_units))

        solns = estimator.get_estimate(weighted_dist)

        gpa = round(weighted_dist / semester["total_units"], 2)
        sb = {"gpa": gpa, "solutions":  solns,  "grade_point": weighted_dist}
        res.append(sb)

    return {"semesters": res}
