from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database.crud import get_all_events, get_event_by_id, get_filtered_events
from auth.auth_crud import get_user_by_username
from auth.security import verify_password, create_access_token
from auth.dependencies import get_current_user

# Create database if not created yet
init_db()

# Fill table with fake logs for testing
test_logger()

app = FastAPI()

# Adding CORS middleware so frontend can work/connect with backend (https://fastapi.tiangolo.com/tutorial/cors/)
# Vite may shift ports (5173, 5174) if one is taken, so we accept any
# localhost / 127.0.0.1 port during development
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route (test if API works)
# To test, run "uvicorn main:app --reload" in the backend folder

class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    return {"message": "EdgeSafe API running"}


@app.post("/auth/login")
def login(body: LoginRequest):
    user = get_user_by_username(body.username)
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/events")
def read_events(detected: bool = Query(default = None), source: str = Query(default = None), limit: int = Query(default = None),  _current_user: str = Depends(get_current_user),
):
    if detected is None and source is None and limit is None:
        events = get_all_events()
    else:
        events = get_filtered_events(detected, source, limit)

    return [dict(e) for e in events]


@app.get("/events/{event_id}")
def read_event(
    event_id: int,
    _current_user: str = Depends(get_current_user),  # require authentication to access this route
):
    event = get_event_by_id(event_id)
    if event:
        return dict(event)

    raise HTTPException(status_code=404, detail="Event not found")