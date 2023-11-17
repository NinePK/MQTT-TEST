import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime  # Import datetime module
from pydantic import BaseModel
import pytz
from fastapi import Depends

thailand_timezone = pytz.timezone('Asia/Bangkok')

class Temperature(BaseModel):
    temperature: int
    timestamp: datetime = datetime.now(thailand_timezone)

app = FastAPI(
    title="Temperature Data API",
)

mongodb_url = os.environ.get("MONGODB_URL")
client = AsyncIOMotorClient(mongodb_url)
db = client.get_database("getTemp")
temperature_collection = db.get_collection("temp_data")

@app.post("/temperature/")
async def create_temperature(
    temperature_data: Temperature,
    timestamp: datetime = Depends(lambda: datetime.now(thailand_timezone)),
):
    print("Received temperature data:", temperature_data.temperature)

    try:
        temperature_data.timestamp = timestamp.replace(tzinfo=pytz.utc)
        new_temperature = await temperature_collection.insert_one(temperature_data.dict())
        print("Inserted temperature data with ID:", new_temperature.inserted_id)
        return {"message": "Temperature data created successfully"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

@app.get(
    "/temperature/",
    response_description="List all temperature data",
    response_model=List[Temperature],
)
async def list_temperatures():
    temperatures = await temperature_collection.find().to_list(1000)
    return temperatures



# import os
# from typing import List
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from motor.motor_asyncio import AsyncIOMotorClient
# from pydantic import BaseModel

# class Temperature(BaseModel):
#     temperature: int

# app = FastAPI(
#     title="Temperature Data API",
# )

# mongodb_url = os.environ.get("MONGODB_URL")
# client = AsyncIOMotorClient(mongodb_url)
# db = client.get_database("getTemp")
# temperature_collection = db.get_collection("temp_data")

# @app.post("/temperature/")
# async def create_temperature(temperature_data: Temperature):
#     print("Received temperature data:", temperature_data.temperature)
    
#     try:
#         new_temperature = await temperature_collection.insert_one(temperature_data.dict())
#         print("Inserted temperature data with ID:", new_temperature.inserted_id)
#         return {"message": "Temperature data created successfully"}
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return {"error": str(e)}
    
# @app.get(
#     "/temperature/",
#     response_description="List all temperature data",
#     response_model=List[Temperature],
# )
# async def list_temperatures():
#     temperatures = await temperature_collection.find().to_list(1000)
#     return temperatures
