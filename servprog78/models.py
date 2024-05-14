from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from pydantic import BaseModel

Base = declarative_base()

class University(Base):
    __tablename__ = "university"
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey('country.id'))
    university_name = Column(Text)

    country = relationship("Country", back_populates="universities")
    ranking_years = relationship("UniversityRankingYear", back_populates="university")
    university_years = relationship("UniversityYear", back_populates="university")


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, index=True)
    country_name = Column(Text)

    universities = relationship("University", back_populates="country")


class UniversityRankingYear(Base):
    __tablename__ = "university_ranking_year"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey('university.id'))
    ranking_criteria_id = Column(Integer, ForeignKey('ranking_criteria.id'))
    year = Column(Integer)
    score = Column(Integer)

    university = relationship("University", back_populates="ranking_years")
    ranking_criteria = relationship("RankingCriteria", back_populates="university_ranking_years")


class UniversityYear(Base):
    __tablename__ = "university_year"
    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey('university.id'))
    year = Column(Integer)
    num_students = Column(Integer)
    student_staff_ratio = Column(Float)
    pct_international_students = Column(Integer)
    pct_female_students = Column(Integer)

    university = relationship("University", back_populates="university_years")


class RankingSystem(Base):
    __tablename__ = "ranking_system"
    id = Column(Integer, primary_key=True, index=True)
    system_name = Column(Text)

    ranking_criteria = relationship("RankingCriteria", back_populates="ranking_system")


class RankingCriteria(Base):
    __tablename__ = "ranking_criteria"
    id = Column(Integer, primary_key=True, index=True)
    ranking_system_id = Column(Integer, ForeignKey('ranking_system.id'))
    criteria_name = Column(Text)

    ranking_system = relationship("RankingSystem", back_populates="ranking_criteria")
    university_ranking_years = relationship("UniversityRankingYear", back_populates="ranking_criteria")

class UniversityBase(BaseModel):
    university_name: str

class UniversityCreate(UniversityBase):
    country_id: int

class UniversityUpdate(UniversityBase):
    country_id: int

class UniversityOut(UniversityBase):
    id: int
    class Config:
        orm_mode = True

class CountryBase(BaseModel):
    country_name: str

class CountryCreate(CountryBase):
    pass

class CountryUpdate(CountryBase):
    pass

class CountryOut(CountryBase):
    id: int
    class Config:
        orm_mode = True