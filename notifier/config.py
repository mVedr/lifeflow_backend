import asyncio

KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
KAFKA_TOPIC="notification"
SENDER_EMAIL="YOUR_MAIL_ID"
SENDER_PASSWORD="YOUR_APP_PASSWORD"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587

loop = asyncio.get_event_loop()
