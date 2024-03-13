import asyncio
import ssl

import aiohttp
from sqlalchemy.orm import Session

from . import apiModels, config, models, share


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

def create_entity(db: Session,entity: apiModels.EntityRegister,tomtom_id: str):
    if get_entity_by_email(entity.primary_email)!=None and get_entity_by_phone(entity.primary_ph_no)!=None and get_entity_by_regd(entity.reg_number)!=None:
        new_entity = models.Entity(**entity.model_dump())
        new_entity.tomtom_id = tomtom_id
        db.add(new_entity)
        db.commit()
        return new_entity
    else:
        return None

def donate_blood(entity_id: int,available_vol: int,email: str,db: Session):
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

def request_blood_through_entity(entity_id: int,email: str,db: Session):
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

def group_by_volume(entity_id: int,db: Session):
    entity = db.query(models.Entity).where(models.Entity.id == entity_id).one_or_none()
    if entity is None:
        return None

    donors: list[models.Donor] = entity.donors

    res = {
        "O-": 0,
        "O+": 0,
        "A-": 0,
        "A+": 0,
        "B-": 0,
        "B+": 0,
        "AB-": 0,
        "AB+": 0,
    }

    for d in donors:
        usr: models.User = d.user_info
        bg = usr.blood_group
        res[bg] += d.available_vol
    return res

def donors_by_blood_in_entity(entity_id: int,bg: str,  db: Session):
    entity = get_entity(db, entity_id)
    if entity is None:
        return None
    if bg not in share.can_donate_to:
        return None
    res = []
    donors: list[models.Donor] = entity.donors
    for d in donors:
        if d.user_info.blood_group == bg:
            res.append(d.user_info)
    return res

async def fetch(session,url):
    async with session.get(url,ssl=ssl.SSLContext()) as response:
        return await response.json()
    
async def fetch_all(loop,lat,lon,radius):
    url_list = [
    f'https://api.tomtom.com/search/2/search/blood.bank.json?key={config.TOMTOM_API_KEY}&lat={lat}&lon={lon}&radius={radius}',
    f'https://api.tomtom.com/search/2/search/hospital.json?key={config.TOMTOM_API_KEY}&lat={lat}&lon={lon}&radius={radius}' ]
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[fetch(session, url) for url in url_list], return_exceptions=True)
        return results
    
async def fetch_search(loop, lat, lon, radius, q):
    url = f'https://api.tomtom.com/search/2/poiSearch/"{q}".json?key={config.TOMTOM_API_KEY}&lat={lat}&lon={lon}&radius={radius}'
    print(url)
    async with aiohttp.ClientSession(loop=loop) as session:
        result = await fetch(session, url)
        return result