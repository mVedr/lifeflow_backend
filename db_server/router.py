from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .functions import *
from .models import SessionLocal

route = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@route.post("/user/create")
async def createUser(user: apiModels.UserRegisterWithEmail,db: Session = Depends(get_db)):
    new_user = create_user(db,user)
    if new_user is  None:
        return {"message": "User already exists in DB"}
    return {"message": "User created successfully"}
    

@route.post("/entity/create")
async def createEntity(entity: apiModels.EntityRegister ,db: Session = Depends(get_db)):
    new_entity = create_entity(db,entity)
    if new_entity is None:
        return {"message":"Credentials are already associated with some other entity"}
    return {"message": "Entity created successfully"}

@route.get("/user/{id}")
async def getUserProfile(id: int,db: Session = Depends(get_db)):
    user = get_user(db,id)
    if user is None:
        raise HTTPException(status_code=404,
                            detail="User not found")
    return user

@route.get("/user_e/{email}")
async def getUserProfileByEmail(email: str,db: Session = Depends(get_db)):
    user = get_user_by_email(db,email)
    if user is None:
        raise HTTPException(status_code=404,
                            detail="User not found")
    return user


@route.get("/entity/{id}")
async def getEntityProfile(id: int,db: Session = Depends(get_db)):
    entity = get_entity(db,id)
    if entity is None:
        raise HTTPException(status_code=404,
                            detail="Entity not found")
    return entity

@route.patch("/user/{id}")
async def updateUserProfile(id: int,new_user: apiModels.UserProfile,db: Session = Depends(get_db)):
    pass

@route.patch("/entity/{id}")
async def updateEntityProfile(id: int,new_user: apiModels.EntityProfile,db: Session = Depends(get_db)):
    pass