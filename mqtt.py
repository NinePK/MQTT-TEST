import paho.mqtt.client as mqtt
import requests
import json

base_url="http://127.0.0.1:8000"

broker_address = "broker.emqx.io"
broker_port = 1883

client = mqtt.Client()
def create_student(name, email, course, gpa):
    url = f"{base_url}/students/"
    payload = {
        "number":
        "gpa": gpa,
    }
    response = requests.post(url, json=payload)
    print(response.json())
    return response.json()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe('/topic')

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    create_student(data['msg'],'email@xxx.xxx','course',4.00)

# ฟังก์ชันสำหรับส่งคำขอ POST เพื่อสร้างนักศึกษาใหม่



client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect(broker_address, broker_port,60)

client.loop_forever()



