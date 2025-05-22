from fastapi import APIRouter, HTTPException, Request, Depends, Header
from app.models import UserRegister, UserLogin, StationStatus
from app.database import db
from app.auth import create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(user: UserRegister):
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="使用者已存在")
    await db.users.insert_one(user.dict())
    return {"message": "註冊成功"}

@router.post("/login")
async def login(user: UserLogin):
    record = await db.users.find_one({"username": user.username})
    if not record or user.password != record["password"]:
        raise HTTPException(status_code=401, detail="帳密錯誤")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def get_me(Authorization: str = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供 JWT")
    token = Authorization.split(" ")[1]
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token 無效或過期")
    return {"username": payload.get("sub")}

@router.post("/api/stations/{station_id}/update")
async def update_station(station_id: str, status: StationStatus):
    try:
        await db["stations"].update_one(
            {"station_id": station_id},
            {"$set": status.dict()},
            upsert=True
        )
        return {"message": f"{station_id} 更新成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"寫入失敗：{str(e)}")

@router.get("/api/stations")
async def get_all_stations():
    cursor = db["stations"].find({}, {"_id": 0})
    stations = await cursor.to_list(length=100)
    return stations

@router.post("/api/reset_stations")
async def reset_stations():
    default_state = {
        "occupied": False,
        "battery_voltage": 54.0,
        "charge_voltage": 58.0,
        "charge_current": 0.0
    }
    station_ids = ['A', 'B', 'C']
    for sid in station_ids:
        await db["stations"].update_one(
            {"station_id": sid},
            {"$set": {"station_id": sid, **default_state}},
            upsert=True
        )
    return {"message": "站點狀態已重設"}
