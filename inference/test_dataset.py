
from pathlib import Path
import kagglehub
import requests

from backend.database.crud import insert_detection_event
from inference.inference_service import run_detection

API_BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "admin123"

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

# 1. Login
login_response = requests.post(
    f"{API_BASE_URL}/auth/login",
    json={
        "username": USERNAME,
        "password": PASSWORD,
    },
)

login_response.raise_for_status()
token = login_response.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

# 2. Send each test image to /detect endpoint
images = [
    p for p in TEST_IMAGES_DIR.iterdir()
    if p.suffix.lower() in SUPPORTED_EXTENSIONS
]

print(f"Found {len(images)} test images")

for image_path in images:
    with open(image_path, "rb") as file:
        response = requests.post(
            f"{API_BASE_URL}/detect",
            headers=headers,
            files={
                "file": (
                    image_path.name,
                    file,
                    "image/jpeg"
                )
            },
        )
    if response.ok:
        data = response.json()
        print(
            f"{image_path.name} | "
            f"Detected={data.get('detected')} | "
            f"Logged={data.get('event_logged')} | "
            f"Conf={data.get('confidence')}"
        )
    else:
        print(f"ERROR {image_path.name}: {response.status_code} {response.text}")

print("DONE")