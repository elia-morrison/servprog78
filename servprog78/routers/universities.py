from pydantic import BaseModel
from servprog78.models import University
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

uni_controller = CRUDController(model=University, router=router, tags=['Unversities'])

class UniversityCreate(BaseModel):
    country_id: int
    university_name: str

class UniversityResponse(BaseModel):
    id: int
    country_id: int
    university_name: str

    class Config:
        orm_mode = True

uni_controller.register_delete_endpoint("/universities/{entity_id}", status_code=204)
uni_controller.register_read_endpoint("/universities/{entity_id}", response_model=UniversityResponse)
uni_controller.register_read_all_endpoint("/universities/", response_model=UniversityResponse)
uni_controller.register_create_endpoint("/universities/", response_model=UniversityResponse,
                                        create_model=UniversityCreate)