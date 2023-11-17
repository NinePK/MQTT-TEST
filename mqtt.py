import paho.mqtt.client as mqtt
import json
import requests
from datetime import datetime
import pytz
from fastapi import Depends

fastapi_url = "http://fastapi:8000"  
mqtt_broker = "broker.emqx.io"
mqtt_port = 1883
mqtt_topic = "/temp"

thailand_timezone = pytz.timezone('Asia/Bangkok')

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        timestamp = datetime.now(thailand_timezone)
        temperature_data = {
            "temperature": payload["temperature"],
            "timestamp": timestamp.replace(tzinfo=pytz.utc).isoformat(),
        }
        print(f"Received temperature data at {timestamp}: {temperature_data}")
        response = requests.post(f"{fastapi_url}/temperature/", json=temperature_data)
        print(response.json())
    except Exception as e:
        print(f"Error processing message: {e}")

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

client.loop_forever()
