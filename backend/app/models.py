# backend/app/models.py
from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class StationStatus(BaseModel):
    station_id: str
    occupied: bool
    battery_voltage: float
    charge_voltage: float
    charge_current: float

