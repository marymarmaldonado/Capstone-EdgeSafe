from fastapi import FastAPI, HTTPException

from database.crud import get_all_events

app = FastAPI()


# Root route (test if API works)
# To test, run "uvicorn main:app --reload" in the backend folder
@app.get("/")
def root():
    return {"message": "EdgeSafe API running"}


@app.get("/events")
def read_events():
    events = get_all_events()
    return [dict(e) for e in events]

