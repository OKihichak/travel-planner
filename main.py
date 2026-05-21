from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from services import validate_artwork
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials
import secrets

import models
import schemas

from database import engine, SessionLocal



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
security = HTTPBasic()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



def authenticate(
    credentials: HTTPBasicCredentials = Depends(security)
):

    correct_username = secrets.compare_digest(
        credentials.username,
        "admin"
    )

    correct_password = secrets.compare_digest(
        credentials.password,
        "password123"
    )

    if not (
        correct_username
        and correct_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )


@app.get("/")
def home():

    return {
        "message": "Travel Planner API running"
    }


@app.post(
    "/projects",
    response_model=schemas.ProjectResponse
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):

    new_project = models.TravelProject(
        name=project.name,
        description=project.description,
        start_date=project.start_date
    )

    db.add(new_project)

    db.flush()

    if len(project.places) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 places allowed"
        )

    for place in project.places:

        artwork = validate_artwork(
            place.external_id
        )

        if not artwork:
            raise HTTPException(
                status_code=404,
                detail=f"Artwork {place.external_id} not found"
            )

        new_place = models.ProjectPlace(
            project_id=new_project.id,
            external_id=artwork["id"],
            title=artwork["title"]
        )

        db.add(new_place)

    db.commit()
    db.refresh(new_project)

    return new_project


@app.get(
    "/projects",
    response_model=list[schemas.ProjectResponse]
)
def get_projects(
    auth: str = Depends(authenticate),
    name: str | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(
        models.TravelProject
    )

    if name:
        query = query.filter(
            models.TravelProject.name.contains(name)
        )

    return query.all()



@app.get(
    "/projects/{project_id}",
    response_model=schemas.ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(
        models.TravelProject
    ).filter(
        models.TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project


@app.put(
    "/projects/{project_id}",
    response_model=schemas.ProjectResponse
)
def update_project(
    project_id: int,
    updated_data: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):

    project = db.query(
        models.TravelProject
    ).filter(
        models.TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    project.name = updated_data.name
    project.description = updated_data.description
    project.start_date = updated_data.start_date

    db.commit()
    db.refresh(project)

    return project


@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = db.query(
        models.TravelProject
    ).filter(
        models.TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    visited_place = db.query(
        models.ProjectPlace
    ).filter(
        models.ProjectPlace.project_id == project_id,
        models.ProjectPlace.visited == True
    ).first()

    if visited_place:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete project with visited places"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted"
    }



@app.post(
    "/projects/{project_id}/places",
    response_model=schemas.PlaceResponse
)
def add_place(
    project_id: int,
    place: schemas.PlaceCreate,
    db: Session = Depends(get_db)
):

    project = db.query(
        models.TravelProject
    ).filter(
        models.TravelProject.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    artwork = validate_artwork(
        place.external_id
    )

    if not artwork:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found in Art API"
        )
    existing_place = db.query(
        models.ProjectPlace
    ).filter(
        models.ProjectPlace.project_id == project_id,
        models.ProjectPlace.external_id == artwork["id"]
    ).first()

    if existing_place:
        raise HTTPException(
            status_code=400,
            detail="Place already exists in this project"
        )
    place_count = db.query(
        models.ProjectPlace
    ).filter(
        models.ProjectPlace.project_id == project_id
    ).count()

    if place_count >= 10:
        raise HTTPException(
            status_code=400,
            detail="Project cannot have more than 10 places"
        )

    new_place = models.ProjectPlace(
        project_id=project_id,
        external_id=artwork["id"],
        title=artwork["title"]
    )

    db.add(new_place)
    db.commit()
    db.refresh(new_place)

    return new_place



@app.patch(
    "/projects/{project_id}/places/{place_id}",
    response_model=schemas.PlaceResponse
)
def update_place(
    project_id: int,
    place_id: int,
    updates: schemas.PlaceUpdate,
    db: Session = Depends(get_db)
):

    place = db.query(
        models.ProjectPlace
    ).filter(
        models.ProjectPlace.id == place_id,
        models.ProjectPlace.project_id == project_id
    ).first()

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    if updates.notes is not None:
        place.notes = updates.notes

    if updates.visited is not None:
        place.visited = updates.visited

    db.commit()
    db.refresh(place)

    return place



@app.get(
    "/projects/{project_id}/places",
    response_model=list[schemas.PlaceResponse]
)
def get_places(
    project_id: int,
    visited: bool | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(
        models.ProjectPlace
    ).filter(
        models.ProjectPlace.project_id == project_id
    )

    if visited is not None:
        query = query.filter(
            models.ProjectPlace.visited == visited
        )

    return query.all()


@app.get(
    "/projects/{project_id}/places/{place_id}",
    response_model=schemas.PlaceResponse
)
def get_place(
    project_id: int,
    place_id: int,
    db: Session = Depends(get_db)
):

    place = db.query(
        models.ProjectPlace
    ).filter(
        models.ProjectPlace.id == place_id,
        models.ProjectPlace.project_id == project_id
    ).first()

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place
