from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel
from servprog78.routers import (
    universities,
    auth,
    countries,
)
from servprog78.models import (
    Base,
)
from servprog78.dependencies.database import get_db, engine
import uvicorn

app = FastAPI(dependencies=[Depends(get_db)])
app.include_router(universities.router)
app.include_router(auth.router)
app.include_router(countries.router)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)