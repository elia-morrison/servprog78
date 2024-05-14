from typing import Optional
from pydantic import BaseModel
from servprog78.models import RankingCriteria
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

controller = CRUDController(model=RankingCriteria, router=router, tags=['Ranking Criteria'])

class RankingCriteriaCreate(BaseModel):
    ranking_system_id: int
    criteria_name: str

class RankingCriteriaPatch(BaseModel):
    ranking_system_id: Optional[int]
    criteria_name: Optional[str]

class RankingCriteriaResponse(BaseModel):
    id: int
    ranking_system_id: int
    criteria_name: str

    class Config:
        orm_mode = True

controller.register_delete_endpoint("/ranking_criteria/{entity_id}", status_code=204)
controller.register_read_endpoint("/ranking_criteria/{entity_id}", response_model=RankingCriteriaCreate)
controller.register_read_all_endpoint("/ranking_criteria/", response_model=RankingCriteriaCreate)
controller.register_create_endpoint("/ranking_criteria/", response_model=RankingCriteriaCreate,
                                        create_model=RankingCriteriaResponse)
controller.register_patch_endpoint("/ranking_criteria/{entity_id}", response_model=RankingCriteriaResponse,
                                        patch_model=RankingCriteriaCreate)