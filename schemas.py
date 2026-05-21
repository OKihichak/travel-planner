from pydantic import BaseModel
from typing import Optional





class PlaceCreate(BaseModel):

    external_id: int

class ProjectCreate(BaseModel):

    name: str
    description: str | None = None
    start_date: str | None = None

    places: list[PlaceCreate] = []

class ProjectResponse(ProjectCreate):

    id: int
    completed: bool

    class Config:
        from_attributes = True


class PlaceUpdate(BaseModel):

    notes: str | None = None
    visited: bool | None = None


class PlaceResponse(BaseModel):

    id: int
    external_id: int
    title: str
    notes: str | None = None
    visited: bool

    class Config:
        from_attributes = True