from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from dotenv import load_dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import sqlite3
import httpx

load_dotenv()

app = FastAPI()

DATABASE = "users.db"
os.makedirs("uploads", exist_ok=True)  # Belge yüklenmediği için bu sadece yer tutucu

# mikroservis ayar fonksiyonu
def get_headers():
    return {"X-API-KEY": os.getenv("API_KEY")}

API_BASE = os.getenv("API_BASE")

# JWT Ayarları
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

# Kullanıcı DB
def init_user_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
        """)
init_user_db()

def authenticate_user(username: str, password: str):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cur.fetchone()

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Şifre mi yanlış, sen mi yanlışsın bilemedim.")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Token sahte ya da süresi dolmuş. Bunu sen mi yaptın?")
    return username

# Kayıtları Listele
@app.get("/calls")
async def list_calls(current_user: str = Depends(get_current_user)):
    headers = get_headers()
    async with httpx.AsyncClient() as client:
        res = await client.get(API_BASE, headers=headers)
        return res.json()

# Status güncelleme
@app.patch("/calls/{call_id}/status")
async def update_status(call_id: int, status: str = Form(...), current_user: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        payload = {"status": status}
        res = await client.patch(f"{API_BASE}/{call_id}", headers=get_headers(), json=payload)
        return res.json()

# Doc ID güncelleme
@app.patch("/calls/{call_id}/doc")
async def update_doc(call_id: int, doc_id: str = Form(...), current_user: str = Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        payload = {"doc_id": doc_id}
        res = await client.patch(f"{API_BASE}/{call_id}", headers=get_headers(), json=payload)
        return res.json()
