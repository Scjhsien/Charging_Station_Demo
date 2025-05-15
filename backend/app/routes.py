# backend/app/routes.py
from fastapi import APIRouter, HTTPException, Request, Depends
from app.models import UserRegister, UserLogin, StationStatus
from app.database import db
from app.auth import create_access_token, verify_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Header

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

@router.post("/update_station")
async def update_station(status: StationStatus):
    try:
        await db["stations"].update_one(
            {"station_id": status.station_id},  # 用 station_id 當 key
            {"$set": status.dict()},            # 全量更新欄位
            upsert=True                         # 若找不到則新增
        )
        return {"message": f"{status.station_id} 更新成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"寫入失敗：{str(e)}")

