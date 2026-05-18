"""
visualize_detection.py - EdgeSafe ML Team
Corre el modelo sobre una imagen y GUARDA una copia con los bounding
boxes dibujados (caja + label + confianza), igual que las figuras de
deteccion del reporte.

Uso:
    python3 visualize_detection.py \
        --model ../runs/detect/yolo11n_firearm_v1/weights/best.pt \
        --image test_frame.jpg \
        --conf 0.04 \
        --out detected_frame.jpg
"""

import argparse
import sys
from pathlib import Path

import cv2
from ultralytics import YOLO


def main():
    p = argparse.ArgumentParser(description="EdgeSafe detection visualizer")
    p.add_argument("--model", required=True, help="Ruta al modelo .pt")
    p.add_argument("--image", required=True, help="Imagen de entrada")
    p.add_argument("--conf", type=float, default=0.04)
    p.add_argument("--out", default="detected_output.jpg",
                   help="Imagen de salida con las cajas dibujadas")
    a = p.parse_args()

    mp = Path(a.model)
    ip = Path(a.image)
    if not mp.exists():
        print(f"[ERROR] No existe el modelo: {mp.resolve()}")
        sys.exit(1)
    if not ip.exists():
        print(f"[ERROR] No existe la imagen: {ip.resolve()}")
        sys.exit(1)

    print(f"[1] Cargando modelo: {mp.name}")
    model = YOLO(str(mp))

    print(f"[2] Corriendo inferencia sobre: {ip.name} (conf={a.conf})")
    results = model.predict(str(ip), conf=a.conf, device=0, verbose=False)
    r = results[0]

    # --- Opcion A: usar el plot() de Ultralytics (rapido y bonito) ---
    annotated = r.plot()  # devuelve ndarray BGR con cajas + labels dibujados
    cv2.imwrite(a.out, annotated)

    # --- Reportar lo que detecto ---
    boxes = r.boxes
    n = 0 if boxes is None else len(boxes)
    print(f"\n[3] Detecciones encontradas: {n}")
    if n > 0:
        for i, b in enumerate(boxes):
            cls = model.names[int(b.cls[0])]
            conf = float(b.conf[0])
            x1, y1, x2, y2 = [int(v) for v in b.xyxy[0].tolist()]
            print(f"    #{i+1}  {cls}  {conf*100:.1f}%  "
                  f"bbox=({x1},{y1})-({x2},{y2})")
    else:
        print("    (ninguna - prueba bajando --conf o revisa la imagen)")

    print(f"\n[4] Imagen anotada guardada en: {Path(a.out).resolve()}")
    print("    Abrela con el visor de imagenes del Jetson para verla,")
    print("    o copiala a tu laptop con scp para el reporte.")


if __name__ == "__main__":
    main()