"""
benchmark_edge.py - EdgeSafe ML Team
Benchmarking formal de ambos modelos (YOLOv11n y YOLOv11s) en el Jetson Orin Nano.
Guarda resultados en un .txt fechado para evidencia del reporte final / ABET.

Uso:
    python3 benchmark_edge.py
"""

import time
import sys
import platform
from datetime import datetime
from pathlib import Path

import torch
from ultralytics import YOLO

# --- CONFIGURACION: ajusta las rutas a tus modelos ---
MODELS = {
    "YOLOv11n": {
        "path": "../runs/detect/yolo11n_firearm_v1/weights/best.pt",
        "conf": 0.04,   # del tuning de tu reporte (Tabla 2)
    },
    "YOLOv11s": {
        "path": "../runs/detect/yolo11s_firearm_v12/weights/best.pt",
        "conf": 0.03,   # del tuning de tu reporte (Tabla 2)
    },
}
TEST_IMAGE = "debug_detection.jpg"
RUNS = 50          # mas corridas = numero mas confiable para el reporte
WARMUP = 5
OUTPUT_FILE = "edge_benchmark_results.txt"


def bench_model(name, model_path, conf, image, runs, warmup):
    mp = Path(model_path)
    if not mp.exists():
        return None, f"NO ENCONTRADO: {mp.resolve()}"

    model = YOLO(str(mp))
    names = model.names

    # Warm-up
    for _ in range(warmup):
        model.predict(image, conf=conf, device=0, verbose=False)

    # Medicion
    lat = []
    detections = 0
    last_result = None
    for _ in range(runs):
        s = time.perf_counter()
        r = model.predict(image, conf=conf, device=0, verbose=False)
        e = time.perf_counter()
        lat.append((e - s) * 1000.0)
        b = r[0].boxes
        if b is not None and len(b) > 0:
            detections += 1
        last_result = r[0]

    avg = sum(lat) / len(lat)
    mn, mx = min(lat), max(lat)
    std = (sum((x - avg) ** 2 for x in lat) / len(lat)) ** 0.5

    # Confianza de la ultima deteccion
    conf_str = "ninguna"
    if last_result is not None and last_result.boxes is not None and len(last_result.boxes) > 0:
        tops = []
        for x in last_result.boxes:
            tops.append(f"{names[int(x.cls[0])]}:{float(x.conf[0])*100:.1f}%")
        conf_str = ", ".join(tops[:3])

    return {
        "name": name,
        "model_path": str(mp),
        "num_classes": len(names),
        "classes": dict(names),
        "conf_threshold": conf,
        "runs": runs,
        "detections": detections,
        "avg_ms": avg,
        "min_ms": mn,
        "max_ms": mx,
        "std_ms": std,
        "last_detection": conf_str,
    }, None


def main():
    cuda = torch.cuda.is_available()
    gpu = torch.cuda.get_device_name(0) if cuda else "N/A (CPU)"

    lines = []
    lines.append("=" * 60)
    lines.append("EdgeSafe - Edge Platform Benchmark Results")
    lines.append("=" * 60)
    lines.append(f"Timestamp:     {datetime.now()}")
    lines.append(f"Platform:      {platform.platform()}")
    lines.append(f"Python:        {sys.version.split()[0]}")
    lines.append(f"PyTorch:       {torch.__version__}")
    lines.append(f"CUDA enabled:  {cuda}")
    lines.append(f"GPU:           {gpu}")
    lines.append(f"Test image:    {TEST_IMAGE}")
    lines.append(f"Runs/model:    {RUNS} (warmup {WARMUP})")
    lines.append("")

    results = []
    for name, cfg in MODELS.items():
        print(f"Benchmarking {name}...")
        res, err = bench_model(name, cfg["path"], cfg["conf"],
                               TEST_IMAGE, RUNS, WARMUP)
        if err:
            lines.append(f"[{name}] ERROR: {err}")
            lines.append("")
            print(f"  {err}")
            continue
        results.append(res)
        lines.append(f"[{name}]")
        lines.append(f"  Model:           {res['model_path']}")
        lines.append(f"  Classes ({res['num_classes']}): {res['classes']}")
        lines.append(f"  Conf threshold:  {res['conf_threshold']}")
        lines.append(f"  Detections:      {res['detections']}/{res['runs']}")
        lines.append(f"  Avg latency:     {res['avg_ms']:.2f} ms")
        lines.append(f"  Min / Max:       {res['min_ms']:.2f} / {res['max_ms']:.2f} ms")
        lines.append(f"  Std deviation:   {res['std_ms']:.2f} ms")
        lines.append(f"  Last detection:  {res['last_detection']}")
        lines.append(f"  SMART Obj #1 (<=1000ms): {'PASS' if res['avg_ms']<=1000 else 'FAIL'}")
        lines.append("")
        print(f"  {name}: {res['avg_ms']:.2f} ms avg, {res['detections']}/{res['runs']} det")

    # Comparacion / recomendacion
    if len(results) == 2:
        a, b = results[0], results[1]
        faster = a if a["avg_ms"] < b["avg_ms"] else b
        lines.append("-" * 60)
        lines.append("COMPARISON SUMMARY")
        lines.append("-" * 60)
        lines.append(f"  Faster model:    {faster['name']} "
                      f"({faster['avg_ms']:.2f} ms)")
        diff = abs(a["avg_ms"] - b["avg_ms"])
        lines.append(f"  Latency diff:    {diff:.2f} ms")
        more_stable = a if a["std_ms"] < b["std_ms"] else b
        lines.append(f"  More stable:     {more_stable['name']} "
                      f"(std {more_stable['std_ms']:.2f} ms)")
        lines.append("")
        lines.append("  Note: Final model selection should weigh latency,")
        lines.append("  stability, model size and memory footprint on the")
        lines.append("  resource-constrained Jetson Orin Nano (7.4 GB RAM).")
        lines.append("")

    lines.append("=" * 60)
    report = "\n".join(lines)
    print("\n" + report)

    with open(OUTPUT_FILE, "w") as f:
        f.write(report + "\n")
    print(f"\nResultados guardados en: {Path(OUTPUT_FILE).resolve()}")


if __name__ == "__main__":
    main()