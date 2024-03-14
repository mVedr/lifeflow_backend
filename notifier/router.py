import asyncio
import json
import smtplib
import ssl

import aiosmtplib
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import APIRouter

from .config import (KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, SENDER_EMAIL,
                     SENDER_PASSWORD, SMTP_PORT, SMTP_SERVER, loop)
from .models import Message

route = APIRouter()

async def send_email_async(email_message: Message):
    context = ssl.create_default_context()
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    message = f"Subject: {email_message.subject}\n\n{email_message.body}"
    
    if SMTP_PORT == 587:  
        client = aiosmtplib.SMTP(hostname=SMTP_SERVER, port=SMTP_PORT, use_tls=False, start_tls=True, tls_context=context)
    else: 
        client = aiosmtplib.SMTP(hostname=SMTP_SERVER, port=SMTP_PORT, use_tls=True, tls_context=context)
    
    await client.connect()
    await client.login(SENDER_EMAIL, SENDER_PASSWORD)
    await client.sendmail(SENDER_EMAIL, email_message.to, message)
    await client.quit()

async def consume():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, loop=loop, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await consumer.start()
    try:
        async for msg in consumer:
            print(f'Consumer Received: {json.loads(msg.value)}')
            message_data_dict = json.loads(msg.value) 
            message_data = Message(**message_data_dict)

            asyncio.create_task(send_email_async(message_data))

    except Exception as e:
        print(f"Consumer Error: {e}")
    finally:
        await consumer.stop()

