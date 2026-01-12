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