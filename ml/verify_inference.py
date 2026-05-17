"""
verify_inference.py - EdgeSafe ML Team
Verifica que YOLO corre con GPU en el Jetson y mide latencia real.
Uso: python3 verify_inference.py --model yolo11n.pt --image debug_detection.jpg --conf 0.04
"""
import argparse, time, sys
from pathlib import Path
import torch
from ultralytics import YOLO

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="yolo11n.pt")
    p.add_argument("--image", default="debug_detection.jpg")
    p.add_argument("--conf", type=float, default=0.04)
    p.add_argument("--runs", type=int, default=30)
    a = p.parse_args()

    print("="*55)
    print("EdgeSafe - Verificacion de Inferencia en Jetson")
    print("="*55)
    print(f"\n[1] Entorno")
    print(f"    Python:  {sys.version.split()[0]}")
    print(f"    PyTorch: {torch.__version__}")
    cuda = torch.cuda.is_available()
    print(f"    CUDA:    {cuda}")
    if cuda:
        print(f"    GPU:     {torch.cuda.get_device_name(0)}")
        dev = 0
    else:
        print("    !! CUDA NO disponible - correra en CPU (LENTO)")
        dev = "cpu"

    mp = Path(a.model)
    if not mp.exists():
        print(f"\n[ERROR] No existe el modelo: {mp.resolve()}"); sys.exit(1)
    print(f"\n[2] Cargando modelo: {mp.name}")
    model = YOLO(str(mp))

    ip = Path(a.image)
    if not ip.exists():
        print(f"\n[ERROR] No existe la imagen: {ip.resolve()}"); sys.exit(1)

    print(f"\n[3] Warm-up (3 inferencias)...")
    for _ in range(3):
        model.predict(str(ip), conf=a.conf, device=dev, verbose=False)

    print(f"\n[4] Midiendo {a.runs} inferencias...")
    lat, det = [], 0
    for _ in range(a.runs):
        s = time.perf_counter()
        r = model.predict(str(ip), conf=a.conf, device=dev, verbose=False)
        e = time.perf_counter()
        lat.append((e-s)*1000.0)
        b = r[0].boxes
        if b is not None and len(b) > 0: det += 1

    avg = sum(lat)/len(lat)
    mn, mx = min(lat), max(lat)
    std = (sum((x-avg)**2 for x in lat)/len(lat))**0.5

    print(f"\n[5] Resultados")
    print(f"    Inferencias:       {a.runs}")
    print(f"    Detecciones (>0):  {det}/{a.runs}")
    print(f"    Latencia promedio: {avg:.2f} ms")
    print(f"    Min / Max:         {mn:.2f} / {mx:.2f} ms")
    print(f"    Desv. estandar:    {std:.2f} ms")

    print(f"\n[6] Objetivo SMART #1 (<= 1000 ms)")
    if avg <= 1000.0:
        print(f"    PASS - {avg:.2f} ms <= 1000 ms")
    else:
        print(f"    FAIL - {avg:.2f} ms > 1000 ms")

    last = r[0].boxes
    if last is not None and len(last) > 0:
        print(f"\n[7] Ultima deteccion")
        for x in last:
            print(f"    {model.names[int(x.cls[0])]}: {float(x.conf[0])*100:.1f}%")
    print("\n" + "="*55)
    print("Verificacion completada.")
    print("="*55)

if __name__ == "__main__":
    main()