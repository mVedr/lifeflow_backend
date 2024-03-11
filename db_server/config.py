import asyncio

KAFKA_BOOTSTRAP_SERVERS= "localhost:9092"
NOTIFICATION_TOPIC="notification"
VERIFICATION_TOPIC="verification"
loop = asyncio.get_event_loop()