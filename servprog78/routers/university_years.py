from pydantic import BaseModel
from servprog78.models import UniversityYear
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

uni_controller = CRUDController(model=UniversityYear, router=router, tags=['Unversity Years'])

class UniversityYearCreate(BaseModel):
    university_id: int
    year: int
    num_students: int
    student_staff_ratio: float
    pct_international_students: int
    pct_female_students: int

class UniversityYearResponse(BaseModel):
    id: int
    university_id: int
    year: int
    num_students: int | None
    student_staff_ratio: float | None
    pct_international_students: int | None
    pct_female_students: int | None
    class Config:
        orm_mode = True

uni_controller.register_delete_endpoint("/university_years/{entity_id}", status_code=204)
uni_controller.register_read_endpoint("/university_years/{entity_id}", response_model=UniversityYearResponse)
uni_controller.register_read_all_endpoint("/university_years/", response_model=UniversityYearResponse)
uni_controller.register_create_endpoint("/university_years/", response_model=UniversityYearResponse,
                                        create_model=UniversityYearCreate)