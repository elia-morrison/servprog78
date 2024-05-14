from typing import Optional
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

class UniversityYearPatch(BaseModel):
    university_id: Optional[int] = None
    year: Optional[int] = None
    num_students: Optional[int] = None
    student_staff_ratio: Optional[float] = None
    pct_international_students: Optional[int] = None
    pct_female_students: Optional[int] = None

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
uni_controller.register_patch_endpoint("/university_years/{entity_id}", response_model=UniversityYearResponse,
                                        patch_model=UniversityYearPatch)