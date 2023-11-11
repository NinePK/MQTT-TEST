import paho.mqtt.client as mqtt
import requests
import json

base_url="http://127.0.0.1:8000"

broker_address = "nebular.mqtt.ifra.io"
broker_port = 1883
broker_username = "f7af5d8c-121f-4985-9976-9b46bcff1678"
broker_password = "39f344d2-7968-4dc2-82c2-4b644ff0b72f"

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

client.connect(broker_address, broker_port,,broker_username,broker_password, 60)

client.loop_forever()



