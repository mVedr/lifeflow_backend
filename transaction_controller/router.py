import asyncio
import concurrent.futures as cf
import json

from aiokafka import AIOKafkaConsumer
from fastapi import APIRouter
from pydantic import BaseModel

from .test import addTransaction, getAllTransactions, getTransactionByID

KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
KAFKA_TOPIC="transaction"
loop = asyncio.get_event_loop()

route = APIRouter()

async def consume():
    consumer = AIOKafkaConsumer(
         KAFKA_TOPIC, loop=asyncio.get_running_loop(), bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS
        )
    await consumer.start()
    try:
        async for msg in consumer:
            #print(f'Consumer Received: {json.loads(msg.value)}')
            data = json.loads(msg.value) 
            arr = data["donorsThatCanDonate"]
            rid = data["receiverId"]
            print(rid)
            # for i in arr:
            #     print(i["donor"])
            with cf.ThreadPoolExecutor() as executor:
                loop = asyncio.get_running_loop()
                tasks = [loop.run_in_executor(executor, addTransaction, d["donor"]["user_id"], rid, d["donor"]["entity_id"], d["donor"]["available_vol"] - d["rem"]) for d in arr]
                rrr = await asyncio.gather(*tasks)
            print("Transaction Complete")
    except Exception as e:
        print(f"Consumer Error: {e}")
    finally:
        await consumer.stop()