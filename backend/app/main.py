from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.database import Base, engine
from app import models
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Contacts Manager")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://contacts-manager-theta.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/groups", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return crud.create_group(db, group)


@app.get("/groups", response_model=list[schemas.Group])
def list_groups(db: Session = Depends(get_db)):
    return crud.get_groups(db)


@app.post("/people", response_model=schemas.Person)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    return crud.create_person(db, person)


@app.get("/people", response_model=list[schemas.Person])
def list_people(db: Session = Depends(get_db)):
    return crud.get_people(db)


@app.get("/people/{person_id}", response_model=schemas.Person)
def get_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.get_person(db, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@app.put("/people/{person_id}", response_model=schemas.Person)
def update_person(person_id: int, person: schemas.PersonCreate, db: Session = Depends(get_db)):
    db_person = crud.update_person(db, person_id, person)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@app.delete("/people/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    db_person = crud.delete_person(db, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"detail": "Person deleted"}


Base.metadata.create_all(bind=engine)