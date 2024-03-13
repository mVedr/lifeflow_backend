import asyncio
import json

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter

from .config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, loop
from .functions import get_image_remote

route = APIRouter()

async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumer Received: {json.loads(msg.value)}')
            data = json.loads(msg.value)
            res = await get_image_remote(data["url"])
            print(res)
    except Exception as e:
        print(f"Consumer Error: {e}")
    finally:
        await consumer.stop()
