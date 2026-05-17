import time
from pathlib import Path
from ultralytics import YOLO
import cv2
from datetime import datetime


MODEL_PATH = Path("ml/yolov11n/best.onnx")
CONF_THRESHOLD = 0.04           # best confidence threshold as determined by testing  (see notebook "find_best_confid.ipynb")

model = YOLO(str(MODEL_PATH))

ANNOTATED_DIR = Path("data/annotated")
ANNOTATED_DIR.mkdir(parents=True, exist_ok=True)

def run_detection(image_path: str):
    start = time.perf_counter()

    results = model.predict(
        source=image_path,
        conf=CONF_THRESHOLD,
        verbose=False
    )

    inference_ms = (time.perf_counter() - start) * 1000

    best_detection = None
    best_result = None
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
                best_result = result
    annotated_path = None
    if best_detection and best_result is not None:
        annotated_img = best_result.plot()
        annotated_path = ANNOTATED_DIR / Path(image_path).name
        cv2.imwrite(str(annotated_path), annotated_img)
    return {
        "model_name": MODEL_PATH.stem,
        "inference_ms": round(inference_ms, 2),
        "timestamp": datetime.now().isoformat(),
        "detected": best_detection is not None,
        "confidence": round(best_detection["confidence"], 4) if best_detection else 0.0,
        "label": best_detection["label"] if best_detection else "none",
        "image_path": image_path
    }