import json
from operator import attrgetter

import aiohttp
import aioredis
import aiosmtplib
from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from transaction_controller.test import (getAllTransactions,
                                         getTransactionByEID,
                                         getTransactionByID)

from . import share
from .config import (KAFKA_BOOTSTRAP_SERVERS, NOTIFICATION_TOPIC,
                     TRANSACTION_TOPIC, VERIFICATION_TOPIC, loop)
from .functions import *
from .models import SessionLocal


class Message(BaseModel):
    to :str
    subject :str
    body :str

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
    #await redis.set(f"user/{new_user.id}",json.dumps(new_user))
    return {"message": "User created successfully"}
    

@route.post("/entity/create")
async def createEntity(tomtom_id: str,entity: apiModels.EntityRegister ,db: Session = Depends(get_db)):
    new_entity = create_entity(db,entity,tomtom_id)
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

@route.get("/user/email/{email}")
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

@route.get("/entity/email/{email}")
async def getUserProfileByEmail(email: str,db: Session = Depends(get_db)):
    user = get_entity_by_email(db,email)
    if user is None:
        raise HTTPException(status_code=404,
                            detail="Entity not found")
    return user

@route.get("/entity/tomtom/{tomtom_id}")
async def getEByTomtom(tomtom_id: str,db: Session = Depends(get_db)):
    E = get_e_by_tom(tomtom_id,db)
    if E is None:
        return {
            "status": "false",
            "data": {}
        }
    return {
        "status": "true",
        "data" : E
    }

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
    usr = get_user_by_email(db,donor.email)
    if res:
        producer = AIOKafkaProducer(loop=loop,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
        await producer.start()
        message :Message = Message(
            to="12113002@nitkkr.ac.in", # make this dynamic later
            subject=f'{usr.name} wants to donate blood',
            body=
            f'''
                {usr.name} wants to donate {usr.blood_group}
                Quanity: {vol}

                Please reach out quickly
            '''
        )
        
        try:
            print(f'Producer Sent: {message}')
            value_json = json.dumps(message.__dict__).encode('utf-8')
            await producer.send(topic=NOTIFICATION_TOPIC,value=value_json)
        except Exception as e:  
            print(f"Consumer Error: {e}")  #
        finally:
            await producer.stop()
            return {"message": "Donation has been added"}
    raise HTTPException(404,"Resources not found")

@route.post("/notify_donors")
async def notifyDonors(donor: apiModels.UserProfile):
    pass

@route.post("/request/{entity_id}")
async def requestBlood(entity_id: int,receiver: apiModels.UserRegisterWithEmail,
                    db: Session = Depends(get_db)):
    res = request_blood_through_entity(entity_id,receiver.email,db)
    if res:
        return {"message": "Added to waitlist"}
    raise HTTPException(404,"Resources not found")

@route.get("/required/{email}")
async def checkRequired(email: str,db: Session = Depends(get_db)):
    usr = get_user_by_email(db,email)
    if usr.volumeRequiredWhileReceiving > 0:
        return {
           "result": True,
           "data": {
            "remaining_blood": usr.volumeRequiredWhileReceiving,
            "blood_group": usr.blood_group,
            "verified": usr.verified,
           } 
        }
    return {
        "result": False,
        "data":{
            "remaining_blood": 0,
        }
    }

@route.post("/initial-request/{vol}")
async def initRequest(vol: int,url: str,receiver: apiModels.UserRegisterWithEmailCords,db: Session = Depends(get_db)):
    usr: models.User = get_user_by_email(db,receiver.email)
    if usr is None:
        raise HTTPException(404,"User not found")
    #usr.volumeRequiredWhileReceiving = vol
    #db.commit()
    producer = AIOKafkaProducer(loop=loop,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,)
    await producer.start()
    obj = {
        "url": url,
        "email": receiver.email,
        "lat": receiver.lat,
        "lon": receiver.lon,
        "vol": vol
    }
    try:
        
        value_json = json.dumps(obj=obj).encode('utf-8')
        print(f'Producer Sent: {value_json}')
        await producer.send(topic=VERIFICATION_TOPIC,value=value_json)
    except Exception as e:  
        print(f"Consumer Error: {e}")  #
    finally:
        await producer.stop()
        return {"message": "Request sent successfully"}


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
async def get_locations(lat: str ="17.5054036", lon: str ="78.4937645",radius: str = "5000"):

    ans = await redis.get(f"{lat}&{lon}&{radius}")
    if ans is not None:
        return json.loads(ans)

    loop = asyncio.get_event_loop()
    res = await fetch_all(loop, lat, lon, radius)
    bb_results = res[0]["results"]
    hospital_results = res[1]["results"]

    ans = []

    for result in bb_results + hospital_results:
        if result["type"] == "POI" and result["score"] > 0.90:
            ans.append(result)

    ans.sort(key=lambda x: x["score"], reverse=True)
    rs = json.dumps(ans)
    await redis.set(f"{lat}&{lon}&{radius}",rs)
    return ans

@route.get("/search")
async def search(lat: str ="17.5054036", lon: str ="78.4937645",radius: str = "5000",q: str=""):

    ans = await redis.get(f"{q}&{lat}&{lon}&{radius}")
    if ans is not None:
        return json.loads(ans)

    loop = asyncio.get_event_loop()
    res = await fetch_search(loop,lat,lon,radius,q)
    ans = []
    for r in res["results"]:
        if r["type"] == "POI" and ( r["score"]>0.90):
            ans.append(r)

    ans.sort(key=lambda x: x["score"], reverse=True)
    rs = json.dumps(ans)
    await redis.set(f"{q}&{lat}&{lon}&{radius}",rs)
    return ans

@route.post("/setVolume")
async def setVolume(req :apiModels.VolumeSetRequest,db: Session = Depends(get_db)):
    usr: models.User = get_user_by_email(db,req.email)
    if usr is None:
        raise HTTPException(404,"No such user found")
    usr.volumeRequiredWhileReceiving = req.vol
    usr.verified = True
    db.commit()
    return {"message":"Verified in the database"}

@route.get("/initialiseTransaction/{user_id}")
async def initializeTransaction(user_id: int,entity_id: int,db: Session = Depends(get_db)):
    en = get_entity(db,entity_id)
    user = get_user(db,user_id)
    req_bg = user.blood_group
    req_vol = user.volumeRequiredWhileReceiving
    donors: list[models.Donor] = en.donors
    donors = sorted(en.donors, key=attrgetter('available_vol'))
    donorsThatCanDonate = []
    donationCanBeCompletedFully = False
    for d in donors:
        d_vol = d.available_vol
        
        d_info: models.User = d.user_info
        if d_info.blood_group in share.can_receive_from[req_bg]:
            if req_vol > d_vol:
                donorsThatCanDonate.append(
                    {
                        "donor": d,
                        "rem": 0
                    }
                )
                req_vol -= d_vol
            else:
                donorsThatCanDonate.append(
                    {
                        "donor": d,
                        "rem": d_vol-req_vol
                    }
                )
                donationCanBeCompletedFully = True
                break
    
    return {
       "donorsThatCanDonate": donorsThatCanDonate,
        "donationCanBeCompletedFully": donationCanBeCompletedFully,
        "receiverId": user_id
    }

@route.post("/completeTransaction/{user_id}")
async def completeTransaction(user_id: int, entity_id: int, db: Session = Depends(get_db)):
    url = f'http://127.0.0.1:8001/initialiseTransaction/{user_id}/?entity_id={entity_id}'
    res = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            res = await resp.json()
    print(res)
    
    producer  = AIOKafkaProducer(loop=loop,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,)

    await producer.start()

    value_json = json.dumps(res).encode('utf-8')
    await producer.send(value=value_json,topic=TRANSACTION_TOPIC)
    await producer.stop()
    donorsThatCanDonate = res["donorsThatCanDonate"]
    donationCanBeCompletedFully = res["donationCanBeCompletedFully"]
    #print(donationCanBeCompletedFully)
    sub = 0
    for dnr in donorsThatCanDonate:
        rem = dnr["rem"]
        dnrId = dnr["donor"]["id"]
        dono = db.query(models.Donor).filter(models.Donor.id == dnrId).one()
        sub += rem
        if rem == 0:
            st = db.query(models.Donor).filter(models.Donor.id == dnrId).delete()
        else:
            dono.available_vol = rem
    if donationCanBeCompletedFully:
        user = db.query(models.User).filter(models.User.id == user_id).one()
        user.verified = False
        user.volumeRequiredWhileReceiving = 0
    else:   
        user = db.query(models.User).filter(models.User.id == user_id).one()
        user.volumeRequiredWhileReceiving -= rem
    db.commit()
    #Send confirmation for transaction
    return {"message":"The donation has been completed"}

'''
 returns list of [donor_id,receiver_id,entity_id,volume]
'''
@route.get("/bchain/all")
async def getAllFromBC():
    return getAllTransactions()

@route.get("/bchain/entity/{id}")
async def getEntityFromBC(id :int):
    return getTransactionByID(id)

@route.get("/bchain/user/{id}")
async def getUserFromBC(id :int):
    return getTransactionByEID(id)