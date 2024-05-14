from pydantic import BaseModel
from servprog78.models import UniversityRankingYear
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

uni_controller = CRUDController(model=UniversityRankingYear, router=router, tags=['Unversity Ranking Years'])

class UniversityRankingYearCreate(BaseModel):
    university_id: int
    ranking_criteria_id: int
    year: int
    score: int

class UniversityRankingYearResponse(BaseModel):
    id: int
    university_id: int
    ranking_criteria_id: int
    year: int
    score: int
    class Config:
        orm_mode = True

uni_controller.register_delete_endpoint("/university_ranking_years/{entity_id}", status_code=204)
uni_controller.register_read_endpoint("/university_ranking_years/{entity_id}", response_model=UniversityRankingYearResponse)
uni_controller.register_read_all_endpoint("/university_ranking_years/", response_model=UniversityRankingYearResponse)
uni_controller.register_create_endpoint("/university_ranking_years/", response_model=UniversityRankingYearResponse,
                                        create_model=UniversityRankingYearCreate)
uni_controller.register_patch_endpoint("/university_ranking_years/{entity_id}", response_model=UniversityRankingYearResponse,
                                        patch_model=UniversityRankingYearCreate)