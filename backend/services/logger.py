from backend.database.crud import insert_detection_event

def log_event(model_name, inference_ms, timestamp, confidence, detected, source, image_path):
    if model_name and inference_ms and timestamp and confidence and detected and source and image_path:
        insert_detection_event(model_name, inference_ms, timestamp, confidence, detected, source, image_path)

    else:
        print("Bad request")