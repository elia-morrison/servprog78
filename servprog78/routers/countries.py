from pydantic import BaseModel
from servprog78.models import Country
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

c_controller = CRUDController(model=Country, router=router, tags=['Countries'])

class CountryCreate(BaseModel):
    country_name: str

class CountryResponse(BaseModel):
    id: int
    country_name: str

    class Config:
        orm_mode = True

c_controller.register_delete_endpoint("/countries/{entity_id}", status_code=204)
c_controller.register_read_endpoint("/countries/{entity_id}", response_model=CountryResponse)
c_controller.register_read_all_endpoint("/countries/", response_model=CountryResponse)
c_controller.register_create_endpoint("/countries/", response_model=CountryResponse,
                                        create_model=CountryCreate)
c_controller.register_patch_endpoint("/countries/{entity_id}", response_model=CountryResponse,
                                        patch_model=CountryCreate)