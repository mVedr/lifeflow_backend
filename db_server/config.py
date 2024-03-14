import asyncio

KAFKA_BOOTSTRAP_SERVERS= "localhost:9092"
NOTIFICATION_TOPIC="notification"
VERIFICATION_TOPIC="verification"
TRANSACTION_TOPIC="transaction"
TOMTOM_API_KEY="YOUR_TOMTOM_KEY"
loop = asyncio.get_event_loop()