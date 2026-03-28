from fastapi import FastAPI

app = FastAPI()

# Root route (test if API works)
# To test, run "uvicorn main:app --reload" in the backend folder
@app.get("/")
def root():
    return {"message": "EdgeSafe API running"}