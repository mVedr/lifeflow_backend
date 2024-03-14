import asyncio
import json

import aiohttp
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import APIRouter
from pydantic import BaseModel

from db_server.config import NOTIFICATION_TOPIC

from .config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, loop
from .functions import get_image_remote

route = APIRouter()

class Message(BaseModel):
    to :str
    subject :str
    body :str

async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumer Received: {json.loads(msg.value)}')
            data = json.loads(msg.value)
            res = await get_image_remote(data["url"])
            '''
            if len(res)>0:
                1. check for hospital in users location
                2. If present, verify them in db and send them an email saying they are verified
            '''
            if(len(res)>0):
                print("You are verified!!!")
                producer = AIOKafkaProducer(loop=loop,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,)
                await producer.start()
                message :Message = Message(
                    to=data["email"],
                    subject=f'LifeFlow - Your request has been verified',
                    body=
                    f'''
     Hi,
        You have recently requested to donate blood, your request has been 
        verified and you can now request blood at various hospitals and blood banks.

    Regards,
    LifeFlow.'''
                )
                try:
                    print(f'Producer Sent: {message}')
                    value_json = json.dumps(message.__dict__).encode('utf-8')
                    await producer.send(topic=NOTIFICATION_TOPIC,value=value_json)
                    await post_request(data["email"], data["vol"]) 
                except Exception as e:  
                    print(f"Consumer Error: {e}")  
                finally:
                    await producer.stop()
            else:
                print("You could not be verified :(")
                producer = AIOKafkaProducer(loop=loop,bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,)
                await producer.start()

                message :Message = Message(
                    to=data["email"],
                    subject=f'LifeFlow - Your request has been could not verified',
                    body=
                    f'''
                        Hi,
                            You have recently requested to donate blood, but your request has been revoked.

                            This can be due to number of reasons, try to make sure the prescription you have uploaded is true and image quality is good.

                        Regards,
                        LifeFlow.
                    '''
                )
                try:
                    print(f'Producer Sent: {message}')
                    value_json = json.dumps(message.__dict__).encode('utf-8')
                    
                    await producer.send(topic=NOTIFICATION_TOPIC,value=value_json)
                    
                except Exception as e:  
                    print(f"Consumer Error: {e}")  
                finally:
                    print("Reached...")
                    await producer.stop()                
            # !!! UNCOMMENT BELOW PART !!!
            # async with aiohttp.ClientSession() as session:
            #     async with session.get(f'http://127.0.0.1:8001/search/?lat={data.lat}&lon={data.lon}&q={res}') as resp:
            #         #print(resp.status)
            #         total_data = (await resp.json())
            #         if len(total_data) > 0:
            #             print("You are verified!!!")
            #             pass
            #         else:
            #             #Send mail saying your request failed (Due to image)
            #             print("You could not be verified :(")
            #             pass

    except Exception as e:
        print(f"Consumer Error: {e}")
    finally:
        await consumer.stop()


async def post_request(email, vol):
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(url="http://127.0.0.1:8001/setVolume",
                                          json={
                                              "email": email,
                                              "vol": vol
                                          })
            await response.json()

    except aiohttp.ClientError as e:
        print("Client error:", e)
