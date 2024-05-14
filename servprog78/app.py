from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from servprog78.models import (
    Base,
    UniversityOut,
    UniversityCreate, 
    University
)
import uvicorn

DATABASE_URL = "sqlite:///./database/db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/universities/", response_model=UniversityOut)
def create_university(university: UniversityCreate, db: Session = Depends(get_db)):
    db_university = University(**university.dict())
    db.add(db_university)
    db.commit()
    db.refresh(db_university)
    return db_university

@app.get("/universities/{university_id}", response_model=UniversityOut)
def read_university(university_id: int, db: Session = Depends(get_db)):
    db_university = db.query(University).filter(University.id == university_id).first()
    if db_university is None:
        raise HTTPException(status_code=404, detail="University not found")
    return db_university

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)