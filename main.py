import asyncio
import random
from fastapi_mqtt.fastmqtt import FastMQTT
from fastapi import FastAPI
from fastapi_mqtt.config import MQTTConfig

app = FastAPI()

mqtt_config = MQTTConfig(
    host="broker.emqx.io",
    port=1883,
)

fast_mqtt = FastMQTT(config=mqtt_config)

fast_mqtt.init_app(app)

mqtt_publish_topic = "/random_number"
mqtt_subscribe_topic = "/subscribed_numbers"

async def publish_random_number():
    while True:
        random_number = random.randint(1, 10)
        fast_mqtt.publish(mqtt_publish_topic, str(random_number))
        print(f"Published random number: {random_number}")
        await asyncio.sleep(5)

@fast_mqtt.on_message()
async def handle_mqtt_message(mqtt_publish_topic, payload):
    print(f"Received message on topic {mqtt_publish_topic}: {payload}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(publish_random_number())
    fast_mqtt.subscribe(mqtt_subscribe_topic)

@fast_mqtt.on_connect()
async def mqtt_connected():
    await fast_mqtt.subscribe(mqtt_publish_topic)
    print(f"Subscribed to MQTT topic: {mqtt_publish_topic}")

@app.get("/")
async def func():
    return {"result": True, "message": "Publishing and subscribing to random numbers"}
    return {"result": True, "message": "Subscribing to random numbers"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
