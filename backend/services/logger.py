from database.crud import insert_detection_event
from datetime import datetime
import random

rows = 99

def log_event(model_name, inference_ms, timestamp, confidence, detected, source, image_path):
    if model_name and inference_ms and timestamp and confidence and (detected is not None) and source and image_path:
        insert_detection_event(model_name, inference_ms, timestamp, confidence, detected, source, image_path)

    else:
        print("Bad request")

def test_logger():
    for i in range(rows):
        log_event(
            model_name="YOLO",
            inference_ms=random.randint(5, 15),
            timestamp=datetime.now().isoformat(),
            confidence=random.random(),
            detected=True,
            source=f"CAM {random.randint(1, 9)}",
            image_path=f"images/test{i}.jpg"
        )

    print("Fake events logged!")