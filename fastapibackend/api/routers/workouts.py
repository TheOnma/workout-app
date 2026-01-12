from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status

from api.models import Workout
from api.deps import db_dependency, user_dependency

router = APIRouter(
  prefix='/workouts',
  tags=['workouts']
)

class WorkoutBase(BaseModel):
  name: str
  description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
  pass

