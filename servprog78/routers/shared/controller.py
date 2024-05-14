from fastapi import HTTPException, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Type, Generic, TypeVar
from pydantic import BaseModel

from servprog78.dependencies.auth import User, check_user_role
from servprog78.dependencies.database import get_db

T = TypeVar('T', bound=BaseModel)

class CRUDController(Generic[T]):
    def __init__(self, model: Type[T], router: APIRouter, tags: List[str] | None = None):
        self.model = model
        self.router = router
        self.tags = tags

    def register_read_endpoint(self, path: str, response_model):
        @self.router.get(path, tags=self.tags, response_model=response_model)
        def read_entity(entity_id: int, db: Session = Depends(get_db), 
                        current_user: User = Depends(check_user_role("reader"))):
            entity = db.query(self.model).filter(self.model.id == entity_id).first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
            return entity
        
    def register_read_all_endpoint(self, path: str, response_model):
        @self.router.get(path, tags=self.tags, response_model=List[response_model])
        def read_entities(limit: Optional[int] = Query(10, gt=0), db: Session = Depends(get_db),
                              current_user: User = Depends(check_user_role("reader"))):
            entities = db.query(self.model).order_by(self.model.id).limit(limit).all()
            return entities
        
    def register_create_endpoint(self, path: str, response_model, create_model):
        @self.router.post(path, tags=self.tags, response_model=response_model, status_code=201)
        def create_entity(entitity: create_model, db: Session = Depends(get_db),
                              current_user: User = Depends(check_user_role("writer"))):
            new_entity = self.model(**entitity.model_dump())
            db.add(new_entity)
            try:
                db.commit()
                db.refresh(new_entity)
            except IntegrityError:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Could not create the {self.model.__name__}, check the data")
            return new_entity
        
    def register_patch_endpoint(self, path: str, response_model, patch_model):
        @self.router.patch(path, tags=self.tags, response_model=response_model)
        def update_entity(entity_id: int, updates: patch_model, db: Session = Depends(get_db),
                        current_user: User = Depends(check_user_role("writer"))):
            existing_entity = db.query(self.model).filter(self.model.id == entity_id).first()
            if not existing_entity:
                raise HTTPException(status_code=404, detail=f"{self.model.__name__} with id {entity_id} not found")

            update_data = updates.dict(exclude_unset=True)
            for key, value in update_data.items():
                if value is None:
                    continue
                setattr(existing_entity, key, value)

            try:
                db.commit()
                db.refresh(existing_entity)
            except IntegrityError:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Could not update the {self.model.__name__}, check the data")
            return existing_entity

    def register_delete_endpoint(self, path: str, status_code: int = 204):
        @self.router.delete(path, tags=self.tags, status_code=status_code)
        def delete_entity(entity_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(check_user_role("writer"))):
            entity = db.query(self.model).filter(self.model.id == entity_id).first()
            if entity is None:
                raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
            db.delete(entity)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Could not delete {self.model.__name__}, check dependencies")
            return {"ok": True}