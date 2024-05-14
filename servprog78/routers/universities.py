from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import List, Optional
from servprog78.dependencies import (
    get_db,
)
from servprog78.models import University
from fastapi import APIRouter

router = APIRouter()


class UniversityCreate(BaseModel):
    country_id: int
    university_name: str

class UniversityResponse(BaseModel):
    id: int
    country_id: int
    university_name: str

    class Config:
        orm_mode = True

@router.get("/universities/{university_id}", response_model=UniversityResponse)
def read_university(university_id: int, db: Session = Depends(get_db)):
    university = db.query(University).filter(University.id == university_id).first()
    if university is None:
        raise HTTPException(status_code=404, detail="University not found")
    return university

@router.get("/universities/", response_model=List[UniversityResponse])
def read_universities(limit: Optional[int] = Query(10, gt=0), db: Session = Depends(get_db)):
    universities = db.query(University).order_by(University.id).limit(limit).all()
    return universities

@router.post("/universities/", response_model=UniversityResponse, status_code=201)
def create_university(university: UniversityCreate, db: Session = Depends(get_db)):
    new_university = University(country_id=university.country_id, university_name=university.university_name)
    db.add(new_university)
    try:
        db.commit()
        db.refresh(new_university)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not create the university, check the data")
    return new_university

@router.delete("/universities/{university_id}", status_code=204)
def delete_university(university_id: int, db: Session = Depends(get_db)):
    university = db.query(University).filter(University.id == university_id).first()
    if university is None:
        raise HTTPException(status_code=404, detail="University not found")
    db.delete(university)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Could not delete university, check dependencies")
    return {"ok": True}