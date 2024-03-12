from sqlalchemy.orm import Session

from . import apiModels, models


def get_user(db: Session,id: int):
    user = db.query(models.User).where(models.User.id == id).one_or_none()
    return user

def get_user_by_email(db: Session,email: str):
    user = db.query(models.User).where(models.User.email == email).one_or_none()
    return user

def get_entity(db: Session,id: int):
    entity = db.query(models.Entity).where(models.Entity.id == id).one_or_none()
    return entity

def get_entity_by_regd(db: Session,reg_no :str):
    entity = db.query(models.Entity).where(models.Entity.reg_number == reg_no).one_or_none()
    return entity

def get_entity_by_phone(db: Session,phone :str):
    entity = db.query(models.Entity).where(models.Entity.primary_ph_no == phone).one_or_none()
    return entity

def get_entity_by_email(db: Session,email :str):
    entity = db.query(models.Entity).where(models.Entity.primary_email == email).one_or_none()
    return entity

def create_user(db: Session,user: apiModels.UserRegisterWithEmail):
    old_user = get_user_by_email(db,user.email)
    if old_user is not None:
        return None
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    return new_user

def create_entity(db: Session,entity: apiModels.EntityRegister):
    if get_entity_by_email(entity.primary_email)!=None and get_entity_by_phone(entity.primary_ph_no)!=None and get_entity_by_regd(entity.reg_number)!=None:
        new_entity = models.Entity(**entity.model_dump())
        db.add(new_entity)
        db.commit()
        return new_entity
    else:
        return None

def donate_blood(entity_id: int,available_vol: str,email: str,db: Session):
    en = get_entity(db, entity_id)
    user = get_user_by_email(db, email)
    if en is None or user is None:
        return False
    donor = models.Donor(
        available_vol = available_vol,
        entity_info = en,
        user_info = user
    )
    en.donors.append(donor)
    db.commit()
    return True

def request_blood(entity_id: int,email: str,db: Session):
    en = get_entity(db, entity_id)
    user = get_user_by_email(db, email)
    if en is None or user is None:
        return False
    en.waitlist.append(user)
    db.commit()
    return True

def get_waitlist(entity_id: int,db: Session):
    entity = db.query(models.Entity).where(models.Entity.id == entity_id).one_or_none()
    if entity is None:
        return None
    return entity.waitlist

def get_donorlist(entity_id: int,db: Session):
    entity = db.query(models.Entity).where(models.Entity.id == entity_id).one_or_none()
    if entity is None:
        return None
    return entity.donors