from utils.result import parse_result
from utils.course_reg import parse_course_registration

from fastapi import FastAPI,  UploadFile
from fastapi.responses import JSONResponse
from model import SuccessResponse, CourseRegData, ResultData


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
