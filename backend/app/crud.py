from sqlalchemy.orm import Session

from app import models, schemas


def create_group(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_groups(db: Session):
    return db.query(models.Group).all()


def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(**person.model_dump())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_people(db: Session):
    return db.query(models.Person).all()


def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()


def update_person(db: Session, person_id: int, person: schemas.PersonCreate):
    db_person = get_person(db, person_id)
    if db_person is None:
        return None
    for key, value in person.model_dump().items():
        setattr(db_person, key, value)
    db.commit()
    db.refresh(db_person)
    return db_person


def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id)
    if db_person is None:
        return None
    db.delete(db_person)
    db.commit()
    return db_person