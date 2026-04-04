from datetime import datetime

from backend.services.logger import log_event

# Fake model output
log_event(
    model_name="YOLO",
    inference_ms=10,
    timestamp=datetime.now().isoformat(),
    confidence=0.91,
    detected=True,
    source="CAM 1",
    image_path="images/test1.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=12,
    timestamp=datetime.now().isoformat(),
    confidence=0.87,
    detected=True,
    source="CAM 2",
    image_path="images/test2.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=9,
    timestamp=datetime.now().isoformat(),
    confidence=0.15,
    detected=False,
    source="CAM 1",
    image_path="images/test3.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=11,
    timestamp=datetime.now().isoformat(),
    confidence=0.76,
    detected=True,
    source="CAM 3",
    image_path="images/test4.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=14,
    timestamp=datetime.now().isoformat(),
    confidence=0.33,
    detected=False,
    source="CAM 2",
    image_path="images/test5.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=8,
    timestamp=datetime.now().isoformat(),
    confidence=0.95,
    detected=True,
    source="CAM 1",
    image_path="images/test6.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=13,
    timestamp=datetime.now().isoformat(),
    confidence=0.52,
    detected=False,
    source="CAM 4",
    image_path="images/test7.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=10,
    timestamp=datetime.now().isoformat(),
    confidence=0.89,
    detected=True,
    source="CAM 2",
    image_path="images/test8.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=15,
    timestamp=datetime.now().isoformat(),
    confidence=0.21,
    detected=False,
    source="CAM 3",
    image_path="images/test9.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=7,
    timestamp=datetime.now().isoformat(),
    confidence=0.97,
    detected=True,
    source="CAM 1",
    image_path="images/test10.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=12,
    timestamp=datetime.now().isoformat(),
    confidence=0.64,
    detected=True,
    source="CAM 4",
    image_path="images/test11.jpg"
)

log_event(
    model_name="YOLO",
    inference_ms=11,
    timestamp=datetime.now().isoformat(),
    confidence=0.40,
    detected=False,
    source="CAM 2",
    image_path="images/test12.jpg"
)

print("Fake events logged!")