from fastapi import FastAPI, HTTPException

from database.crud import get_all_events, get_event_by_id

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


@app.get("/events/{event_id}")
def read_event(event_id: int):
    event = get_event_by_id(event_id)
    if event:
        return dict(event)

    raise HTTPException(status_code=404, detail="Event not found")