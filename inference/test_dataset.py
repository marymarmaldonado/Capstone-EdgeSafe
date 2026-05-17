from pathlib import Path
import kagglehub

from backend.database.crud import insert_detection_event
from inference.inference_service import run_detection

# Download dataset automatically
dataset_path = kagglehub.dataset_download(
    "abuzarkhaaan/helmetandguntesting",
    output_dir=r"C:\kaggle"
)

print("Dataset path:", dataset_path)

dataset_path = Path(dataset_path)

# Locate test images
TEST_IMAGES_DIR = dataset_path / "Gun with webcam views.v1i.yolov8" / "test" / "images"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

images = [
    p for p in TEST_IMAGES_DIR.iterdir()
    if p.suffix.lower() in SUPPORTED_EXTENSIONS
]

print(f"Found {len(images)} test images")

for image_path in images:
    result = run_detection(str(image_path))
    print(
        f"{image_path.name} | "
        f"Detected={result['detected']} | "
        f"Conf={result['confidence']}"
    )
    if result["detected"]:
        insert_detection_event(
            model_name=result["model_name"],
            inference_ms=result["inference_ms"],
            timestamp=result["timestamp"],
            confidence=result["confidence"],
            detected=int(result["detected"]),
            source="test_dataset",
            image_path=result["image_path"]
        )

print("DONE")