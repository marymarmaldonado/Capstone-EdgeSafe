from fastapi import FastAPI, HTTPException, Query, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from pathlib import Path

from backend.database.crud import insert_detection_event, get_all_events, get_event_by_id, get_filtered_events
from backend.database.init_db import init_db
from backend.services.logger import test_logger
from backend.auth.auth_crud import get_user_by_username
from backend.auth.security import verify_password, create_access_token
from backend.auth.dependencies import get_current_user

from tempfile import NamedTemporaryFile
import os

import shutil
from inference.inference_service import run_detection

class DetectionResult(BaseModel):
    """
    Resultado de inferencia que el pipeline del edge envia ya
    procesado. Campos en el formato EXACTO del schema
    detection_events (ver API_Documentation.md).
    """
    model_name: str            # ej "YOLOv11n"
    inference_ms: int          # latencia medida en el edge
    timestamp: str             # ISO format, generado en el edge
    confidence: float          # 0.0 - 1.0
    detected: bool             # True si hay arma
    source: str                # ej "CAM 1"
    image_path: str            # ruta a la imagen anotada (guardada por el pipeline)
    label: Optional[str] = None  # ej "Guns" (opcional, por si lo usan luego)

# Create database if not created yet
init_db()

# Fill table with fake logs for testing
# test_logger()

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

@app.post("/detect")
def detect_event(
    result: DetectionResult,
    _current_user: str = Depends(get_current_user),
):
    """
    Recibe un resultado de deteccion YA PROCESADO por el pipeline
    del edge device. El backend NO corre inferencia: solo persiste
    el evento si hubo deteccion de arma.
 
    Separacion de responsabilidades:
      - ML pipeline (edge): captura + inferencia + guarda imagen
      - Backend (este): validar + guardar evento + servir API
    """
    if result.detected:
        insert_detection_event(
            model_name=result.model_name,
            inference_ms=result.inference_ms,
            timestamp=result.timestamp,
            confidence=result.confidence,
            detected=int(result.detected),
            source=result.source,
            image_path=result.image_path,
        )
        return {
            "message": "Event logged",
            "event_logged": True,
        }
 
    # Si no hubo deteccion, no se guarda nada (igual que Figura 1 del reporte)
    return {
        "message": "No detection, event not logged",
        "event_logged": False,
    }