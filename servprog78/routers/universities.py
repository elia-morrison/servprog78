from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List, Optional
from servprog78.dependencies.auth import User, check_user_role
from servprog78.dependencies.database import (
    get_db,
)
from servprog78.models import University
from fastapi import APIRouter
from servprog78.routers.shared.controller import CRUDController

router = APIRouter()

uni_controller = CRUDController(model=University, router=router)

class UniversityCreate(BaseModel):
    country_id: int
    university_name: str

class UniversityResponse(BaseModel):
    id: int
    country_id: int
    university_name: str

    class Config:
        orm_mode = True

uni_controller.register_delete_endpoint("/universities/{university_id}", status_code=204)
uni_controller.register_read_endpoint("/universities/{university_id}", response_model=UniversityResponse)
uni_controller.register_read_all_endpoint("/universities/", response_model=UniversityResponse)
uni_controller.register_create_endpoint("/universities/", response_model=UniversityResponse,
                                        create_model=UniversityCreate)