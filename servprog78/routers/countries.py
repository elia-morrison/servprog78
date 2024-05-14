from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List, Optional
from servprog78.dependencies.auth import User, check_user_role
from servprog78.dependencies.database import (
    get_db,
)
from servprog78.models import Country
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

c_controller = CRUDController(model=Country, router=router)

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