import json

import aioredis
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .functions import *
from .models import SessionLocal

route = APIRouter()
redis = aioredis.Redis(host="localhost", port=6379,db=0)

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
    db_user = get_user(db,id)
    if db_user is None:
        return HTTPException(status_code=404,
                             detail="User not found")
    
    user_data = new_user.model_dump()

    for k,v in user_data.items():
        setattr(db_user,k,v)

    db.commit()
    return db_user

@route.patch("/entity/{id}")
async def updateEntityProfile(id: int,new_entity: apiModels.EntityProfile,db: Session = Depends(get_db)):
    db_entity = get_entity(db,id)
    if db_entity is None:
        return HTTPException(status_code=404,
                             detail="Entity not found")
    user_data = new_entity.model_dump()

    for k,v in user_data.items():
        setattr(db_entity,k,v)

    db.commit()
    return db_entity    

@route.post("/donate/{entity_id}")
async def donateViaEntity(entity_id: int,vol: int,donor: apiModels.UserRegisterWithEmail,db: Session = Depends(get_db)):
    res = donate_blood(entity_id=entity_id,available_vol=vol,email=donor.email,db=db)
    if res:
        return {"message": "Donation has been added"}
    raise HTTPException(404,"Resources not found")

@route.post("/notify_donors")
async def notifyDonors(donor: apiModels.UserProfile):
    pass

@route.post("/request/{entity_id}")
async def requestBlood(entity_id: int,receiver: apiModels.UserRegisterWithEmail,
                    db: Session = Depends(get_db)):
    res = request_blood(entity_id,receiver.email,db)
    if res:
        return {"message": "Added to waitlist"}
    raise HTTPException(404,"Resources not found")

@route.get("/waitlist/{entity_id}")
async def getWaitlist(entity_id: int,db: Session = Depends(get_db)):
    lst = get_waitlist(entity_id,db)
    if lst is None:
        return HTTPException(status_code=404,
                             detail="Entity not found")
    return lst

@route.get("/donors/{entity_id}")
async def getDonors(entity_id: int,db: Session = Depends(get_db)):
    lst = get_donorlist(entity_id,db)
    if lst is None:
        return HTTPException(status_code=404,
                             detail="Entity not found")
    return lst

@route.get('/total_volume/{entity_id}')
async def quantity_by_group(entity_id: int, db: Session = Depends(get_db)):
    res = group_by_volume(entity_id,db)
    if res is None:
        return HTTPException(status_code=404,detail="Entity not found")
    return res

@route.get("/donors/bloodgroup/{entity_id}")
async def get_donors_by_bg(entity_id: int,bg: str,  db: Session = Depends(get_db)):
    res = donors_by_blood_in_entity(entity_id,bg,db)
    if res is None:
        return HTTPException(status_code=404,detail="Resources not found")
    return res

@route.get("/locations")
async def get_locations(lat: str ="17.5054036", lon: str ="78.4937645",radius: str = "2000"):

    ans = await redis.get(f"{lat}&{lon}&{radius}")
    if ans is not None:
        return json.loads(ans)

    loop = asyncio.get_event_loop()
    res = await fetch_all(loop, lat, lon, radius)
    bb_results = res[0]["results"]
    hospital_results = res[1]["results"]

    ans = []

    for result in bb_results + hospital_results:
        if result["type"] == "POI" and result["score"] > 0.70:
            ans.append(result)

    ans.sort(key=lambda x: x["score"], reverse=True)
    rs = json.dumps(ans)
    await redis.set(f"{lat}&{lon}&{radius}",rs)
    return ans

@route.get("/search")
async def search(lat: str ="17.5054036", lon: str ="78.4937645",radius: str = "2000",q: str=""):

    ans = await redis.get(f"{q}&{lat}&{lon}&{radius}")
    if ans is not None:
        return json.loads(ans)

    loop = asyncio.get_event_loop()
    res = await fetch_search(loop,lat,lon,radius,q)
    ans = []
    for r in res["results"]:
        if r["type"] == "POI" and (r["matchConfidence"]["score"] > 0.70 or r["score"]>0.70):
            ans.append(r)

    ans.sort(key=lambda x: x["score"], reverse=True)
    rs = json.dumps(ans)
    await redis.set(f"{q}&{lat}&{lon}&{radius}",rs)
    return ans