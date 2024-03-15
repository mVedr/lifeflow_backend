import asyncio
import json

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter
from pydantic import BaseModel

KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
KAFKA_TOPIC="transaction"
loop = asyncio.get_event_loop()

route = APIRouter()

async def consume():
    consumer = AIOKafkaConsumer(
         KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
        )
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumer Received: {json.loads(msg.value)}')
            data = json.loads(msg.value) 
            
    except Exception as e:
        print(f"Consumer Error: {e}")
    finally:
        await consumer.stop()
