from backend.database.crud import insert_detection_event

def log_event(model_name, inference_ms, timestamp, confidence, detected, source, image_path):
    insert_detection_event(model_name, inference_ms, timestamp, confidence, detected, source, image_path)