"""
camera_capture.py - EdgeSafe ML Team
Modulo de captura de camara para el Jetson Orin Nano usando OpenCV.

Cubre el checklist de Trello "Camera Integration for Live Image Capture":
  - Implement frame capture using OpenCV
  - Test continuous frame streaming
  - Provide frames to the YOLO inference pipeline (clase reutilizable)

Camara detectada: Elgato Facecam MK.2 en /dev/video0
Config elegida: MJPG 1280x720 @ 30fps (optimo para YOLOv11 + Jetson)

Modos de uso:
    # Prueba rapida (cuenta frames 10 segundos, sin ventana)
    python3 camera_capture.py --test

    # Vista en vivo con ventana (necesita monitor/escritorio)
    python3 camera_capture.py --preview

    # Guardar un frame de prueba a disco
    python3 camera_capture.py --snapshot test_frame.jpg
"""

import argparse
import time
import sys

import cv2


class CameraCapture:
    """
    Encapsula la captura de la webcam para que el edge pipeline
    pueda pedir frames sin preocuparse de la configuracion.
    """

    def __init__(self, device=0, width=1280, height=720, fps=30):
        self.device = device
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None

    def open(self):
        # CAP_V4L2 fuerza el backend Video4Linux2 (correcto en Jetson/Linux)
        self.cap = cv2.VideoCapture(self.device, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            raise RuntimeError(
                f"No se pudo abrir la camara en /dev/video{self.device}. "
                f"Verifica que este conectada (lsusb) y libre (no usada por otra app)."
            )

        # Forzar MJPG (comprimido, eficiente sobre USB)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        # Buffer chico = frames mas frescos (menos lag en deteccion)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Confirmar la config real que acepto la camara
        aw = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        ah = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        af = self.cap.get(cv2.CAP_PROP_FPS)
        print(f"[camera] Abierta /dev/video{self.device} -> {aw}x{ah} @ {af:.0f}fps")
        return self

    def read(self):
        """Lee un frame. Devuelve (ok, frame). frame es un ndarray BGR."""
        if self.cap is None:
            raise RuntimeError("La camara no esta abierta. Llama a open() primero.")
        return self.cap.read()

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    # Soporte para 'with CameraCapture() as cam:'
    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


# ----------------- Modos de prueba (CLI) -----------------

def mode_test(device, seconds=10):
    """Cuenta frames durante N segundos para validar streaming continuo."""
    print(f"[test] Capturando {seconds}s para medir FPS real...")
    with CameraCapture(device=device) as cam:
        n = 0
        bad = 0
        start = time.time()
        while time.time() - start < seconds:
            ok, frame = cam.read()
            if not ok or frame is None:
                bad += 1
                continue
            n += 1
        elapsed = time.time() - start

    print(f"\n[test] Resultados")
    print(f"    Frames OK:        {n}")
    print(f"    Frames fallidos:  {bad}")
    print(f"    Tiempo:           {elapsed:.1f}s")
    print(f"    FPS real:         {n/elapsed:.1f}")
    if n > 0 and bad == 0:
        print("    PASS - streaming continuo estable, 0 frames perdidos")
    elif n > 0:
        print(f"    OK con advertencia - {bad} frames fallidos (revisa USB/cable)")
    else:
        print("    FAIL - no se capturo ningun frame")


def mode_snapshot(device, out_path):
    """Guarda un frame a disco (util para probar la integracion con YOLO)."""
    with CameraCapture(device=device) as cam:
        # Descartar primeros frames (la camara tarda en estabilizar exposicion)
        for _ in range(5):
            cam.read()
            time.sleep(0.05)
        ok, frame = cam.read()
        if not ok or frame is None:
            print("[snapshot] FAIL - no se pudo capturar el frame")
            sys.exit(1)
        cv2.imwrite(out_path, frame)
        h, w = frame.shape[:2]
        print(f"[snapshot] Guardado {out_path} ({w}x{h})")


def mode_preview(device):
    """Ventana en vivo. Presiona 'q' para salir. Necesita escritorio (no SSH)."""
    print("[preview] Ventana en vivo. Presiona 'q' en la ventana para salir.")
    with CameraCapture(device=device) as cam:
        while True:
            ok, frame = cam.read()
            if not ok:
                print("[preview] Frame fallido, reintentando...")
                continue
            cv2.imshow("EdgeSafe - Camera Preview", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    cv2.destroyAllWindows()


def main():
    p = argparse.ArgumentParser(description="EdgeSafe camera capture")
    p.add_argument("--device", type=int, default=0,
                   help="Indice de /dev/videoN (default 0)")
    p.add_argument("--test", action="store_true",
                   help="Medir FPS y estabilidad 10s")
    p.add_argument("--seconds", type=int, default=10)
    p.add_argument("--snapshot", metavar="PATH",
                   help="Guardar un frame a disco")
    p.add_argument("--preview", action="store_true",
                   help="Ventana en vivo (necesita escritorio)")
    a = p.parse_args()

    if a.test:
        mode_test(a.device, a.seconds)
    elif a.snapshot:
        mode_snapshot(a.device, a.snapshot)
    elif a.preview:
        mode_preview(a.device)
    else:
        print("Especifica un modo: --test | --snapshot PATH | --preview")
        print("Ej: python3 camera_capture.py --test")


if __name__ == "__main__":
    main()