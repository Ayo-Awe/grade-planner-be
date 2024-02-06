from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import course_registration, course_structure, generate_grades, result
from utils import format_response


app = FastAPI()

origins = [
    "https://grade-planner.vercel.app/",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)


@app.get("/")
def root_handler():
    return format_response({"message": "Welcome to grade planner"})


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(course_registration.router)
api_router.include_router(course_structure.router)
api_router.include_router(result.router)
api_router.include_router(generate_grades.router)

app.include_router(api_router)


# @app.post("/api/v1/estimate")
# async def estimate_grades(er: EstimateGradeRequest):
#     # get target grade points
#     req = er.model_dump()
#     semesters = req["new_semesters"]
#     new_semester_units = 0

#     for i, semester in enumerate(semesters):
#         tu = reduce(lambda x, y: x + y["unit"], semester["courses"], 0)
#         new_semester_units += tu
#         semesters[i]["total_units"] = tu

#     total_units = req["current_units"] + new_semester_units
#     target_gp = (total_units * req["target_cgpa"]) - \
#         (req["current_units"] * req["cgpa"])

#     res = []

#     for semester in semesters:
#         estimator = GradeEstimator(semester["courses"], "")
#         weighted_dist = round(
#             target_gp * (semester["total_units"]/new_semester_units))

#         solns = estimator.generate(weighted_dist)

#         gpa = round(weighted_dist / semester["total_units"], 2)
#         sb = {"gpa": gpa, "solutions":  solns,  "grade_point": weighted_dist}
#         res.append(sb)

#     return {"semesters": res}
