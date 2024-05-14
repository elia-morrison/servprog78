from pydantic import BaseModel
from servprog78.models import RankingSystem
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

controller = CRUDController(model=RankingSystem, router=router, tags=['Ranking Systems'])

class RankingSystemCreate(BaseModel):
    system_name: str

class RankingSystemResponse(BaseModel):
    id: int
    system_name: str

    class Config:
        orm_mode = True

controller.register_delete_endpoint("/ranking_systems/{entity_id}", status_code=204)
controller.register_read_endpoint("/ranking_systems/{entity_id}", response_model=RankingSystemResponse)
controller.register_read_all_endpoint("/ranking_systems/", response_model=RankingSystemResponse)
controller.register_create_endpoint("/ranking_systems/", response_model=RankingSystemResponse,
                                        create_model=RankingSystemCreate)