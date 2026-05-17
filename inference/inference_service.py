import time
from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = Path("ml/yolov11n/best.onnx")
CONF_THRESHOLD = 0.09           # best confidence threshold as determined by testing  (see notebook "find_best_confid.ipynb")

model = YOLO(str(MODEL_PATH))

def run_detection(image_path: str):
    start = time.perf_counter()

    results = model.predict(
        source=image_path,
        conf=CONF_THRESHOLD,
        verbose=False
    )

    inference_ms = (time.perf_counter() - start) * 1000

    best_detection = None

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = result.names[class_id]
            confidence = float(box.conf[0])
            if best_detection is None or confidence > best_detection["confidence"]:
                best_detection = {
                    "label": label,
                    "confidence": confidence
                }

    return {
        "model_name": MODEL_PATH.stem,
        "inference_ms": round(inference_ms, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "detected": best_detection is not None,
        "confidence": round(best_detection["confidence"], 4) if best_detection else 0.0,
        "label": best_detection["label"] if best_detection else "none",
        "image_path": image_path
    }