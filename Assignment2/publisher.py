# publisher.py
import asyncio
import json
import random
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
nc = NATS()
async def publish_events():
    

    await nc.connect(servers=["nats://localhost:4222"])

    while True:
        event = generate_event()
        await nc.publish("taxi-ride", json.dumps(event).encode())
        await asyncio.sleep(1)  # Adjust the rate of events per second

async def close_connection():
    await nc.close()

def generate_event():
    event = {
        "ride_id": generate_ride_id(),
        "timestamp": generate_timestamp(),
        "pickup_longitude": random.uniform(-180, 180),
        "pickup_latitude": random.uniform(-90, 90),
        "dropoff_longitude": random.uniform(-180, 180),
        "dropoff_latitude": random.uniform(-90, 90),
        "passenger_count": random.randint(1, 6),
        "fare_amount": random.uniform(5, 100)
    }
    return event

def generate_ride_id():
    # Generate a unique ride ID (for simplicity, using a random integer)
    return random.randint(1, 1000000)

def generate_timestamp():
    # Generate a timestamp (for simplicity, using the current time)
    return str(datetime.now())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(publish_events())
