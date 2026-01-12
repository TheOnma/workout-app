from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from api.models import Workout, Routine
from api.deps import db_dependency, user_dependency 

router = APIRouter(
  prefix='/routines',
  tags=['routines']
)

class RoutineBase(BaseModel):
  name: str
  description: Optional[str] = None

class RoutineCreate(RoutineBase):
  workouts: List[int] = []

@router.get('/')
def get_routines(db: db_dependency, user: user_dependency):
  return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == user.get('id')).all()