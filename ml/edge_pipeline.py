"""
edge_pipeline.py - EdgeSafe ML Team
Pipeline de deteccion en el edge device (Jetson Orin Nano).

ARQUITECTURA CORRECTA (inferencia en el edge):
  Camara -> frame -> preprocessing -> YOLO (AQUI, en el edge) ->
  ?arma? -> guardar imagen anotada -> POST /detect con los
  RESULTADOS (JSON, no la imagen) -> backend solo guarda el evento.

El backend NO corre inferencia. Respeta la separacion de
responsabilidades del reporte (5.1): ML team = inferencia edge,
systems team = persistencia y API.

Requiere el endpoint /detect rediseñado (ver detect_endpoint_redesign.py)
acordado con el systems team.

Uso:
    python3 edge_pipeline.py \
        --model ../runs/detect/yolo11n_firearm_v1/weights/best.pt \
        --api http://127.0.0.1:8000 \
        --user USUARIO --password CLAVE \
        --source "CAM 1"

    # Modo prueba: parar tras N eventos
    python3 edge_pipeline.py --model ... --api ... --user ... \
        --password ... --max-events 5
"""

import argparse
import time
import signal
import sys
from datetime import datetime
from pathlib import Path

import cv2
import requests
from ultralytics import YOLO

from camera_capture import CameraCapture


_RUNNING = True


def _handle_sigint(signum, frame):
    global _RUNNING
    print("\n[pipeline] Apagado solicitado, cerrando limpio...")
    _RUNNING = False


def login(api_base, username, password):
    """POST /auth/login -> token JWT."""
    resp = requests.post(f"{api_base}/auth/login",
                          json={"username": username, "password": password},
                          timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Login fallo ({resp.status_code}): {resp.text}\n"
            f"Verifica credenciales con Marymar."
        )
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError(f"Login OK pero sin token: {resp.json()}")
    return token


def send_result(api_base, token, payload):
    """POST /detect con el resultado YA procesado (JSON)."""
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(f"{api_base}/detect", headers=headers,
                         json=payload, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"/detect fallo ({resp.status_code}): {resp.text}")
    return resp.json()


def preprocess(frame):
    if frame is None or frame.size == 0:
        return None
    return frame


def main():
    p = argparse.ArgumentParser(description="EdgeSafe edge pipeline")
    p.add_argument("--model", required=True, help="Ruta al modelo .pt")
    p.add_argument("--api", default="http://127.0.0.1:8000")
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--source", default="CAM 1")
    p.add_argument("--device", type=int, default=0)
    p.add_argument("--conf", type=float, default=0.04)
    p.add_argument("--process-every", type=int, default=15,
                   help="Procesar 1 de cada N frames")
    p.add_argument("--cooldown", type=float, default=3.0,
                   help="Segundos minimos entre eventos guardados")
    p.add_argument("--max-events", type=int, default=0,
                   help="0 = indefinido; >0 = parar tras N (prueba)")
    p.add_argument("--save-dir", default="../backend/images",
                   help="Donde el pipeline guarda las imagenes anotadas")
    a = p.parse_args()

    signal.signal(signal.SIGINT, _handle_sigint)

    mp = Path(a.model)
    if not mp.exists():
        print(f"[ERROR] No existe el modelo: {mp.resolve()}")
        sys.exit(1)

    save_dir = Path(a.save_dir).expanduser()
    save_dir.mkdir(parents=True, exist_ok=True)

    model_name = "YOLOv11n" if "11n" in str(mp) else (
        "YOLOv11s" if "11s" in str(mp) else mp.stem)

    print("=" * 55)
    print("EdgeSafe - Edge Pipeline (inferencia en el edge)")
    print("=" * 55)
    print(f"  Modelo:    {mp.name} ('{model_name}')")
    print(f"  Backend:   {a.api}")
    print(f"  Camara:    /dev/video{a.device} ({a.source})")
    print(f"  Conf:      {a.conf}")
    print(f"  Procesa 1/{a.process_every} frames, cooldown {a.cooldown}s")
    if a.max_events > 0:
        print(f"  Modo prueba: para tras {a.max_events} eventos")
    print()

    print("[1] Cargando modelo YOLO en el edge...")
    model = YOLO(str(mp))

    print("[2] Autenticando con el backend...")
    try:
        token = login(a.api, a.user, a.password)
        print("    Login OK")
    except Exception as e:
        print(f"    [ERROR] {e}")
        sys.exit(1)

    events = 0
    frame_idx = 0
    last_event_time = 0.0

    print("[3] Abriendo camara...")
    with CameraCapture(device=a.device) as cam:
        print("\n[4] Pipeline corriendo. Ctrl+C para detener.\n")
        while _RUNNING:
            ok, frame = cam.read()
            if not ok or frame is None:
                continue

            frame_idx += 1
            if frame_idx % a.process_every != 0:
                continue

            proc = preprocess(frame)
            if proc is None:
                continue

            # --- Inferencia EN EL EDGE ---
            t0 = time.perf_counter()
            results = model.predict(proc, conf=a.conf,
                                    device=0, verbose=False)
            inference_ms = int((time.perf_counter() - t0) * 1000)

            r = results[0]
            boxes = r.boxes
            detected = boxes is not None and len(boxes) > 0
            if not detected:
                continue

            confidence = max(float(b.conf[0]) for b in boxes)
            label = model.names[int(boxes[0].cls[0])]

            now = time.time()
            if now - last_event_time < a.cooldown:
                continue
            last_event_time = now

            # --- Guardar imagen anotada (el pipeline, no el backend) ---
            ts = datetime.now()
            stamp = ts.strftime("%Y%m%d_%H%M%S_%f")
            img_name = f"event_{stamp}.jpg"
            cv2.imwrite(str(save_dir / img_name), r.plot())
            image_path = f"images/{img_name}"

            # --- Mandar SOLO los resultados (JSON) al backend ---
            payload = {
                "model_name": model_name,
                "inference_ms": inference_ms,
                "timestamp": ts.isoformat(),
                "confidence": round(confidence, 4),
                "detected": True,
                "source": a.source,
                "image_path": image_path,
                "label": label,
            }

            try:
                resp = send_result(a.api, token, payload)
                if resp.get("event_logged"):
                    events += 1
                    print(f"  [EVENTO #{events}] {label} "
                          f"conf={confidence*100:.1f}% "
                          f"inferencia={inference_ms}ms -> guardado")
            except Exception as e:
                print(f"  [ERROR] envio fallo: {e}")

            if a.max_events > 0 and events >= a.max_events:
                print(f"\n[pipeline] {a.max_events} eventos (modo prueba). "
                      f"Terminando.")
                break

    print(f"\n[5] Pipeline detenido. Eventos guardados: {events}")
    print("    Verifica en el dashboard o con GET /events")
    print("=" * 55)


if __name__ == "__main__":
    main()