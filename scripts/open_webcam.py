from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Any

import cv2
from ultralytics import YOLO


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SMOKING_MODEL = PROJECT_ROOT / "models" / "smoking_detection_v1.pt"
DEFAULT_PERSON_MODEL = PROJECT_ROOT / "yolo11n.pt"
WINDOW_NAME = "AIRIS Webcam"

COLORS = {
    "person": (0, 255, 0),
    "cigarette": (0, 165, 255),
    "smoke": (190, 190, 190),
}


def parse_source(value: str) -> int | str:
    """Use a numeric source as a webcam index and other values as video paths."""
    try:
        return int(value)
    except ValueError:
        return value


def draw_detections(frame: Any, result: Any, allowed_classes: set[str]) -> None:
    """Draw detections from one YOLO result whose names are in allowed_classes."""
    if result.boxes is None:
        return

    for box in result.boxes:
        class_id = int(box.cls[0])
        label = str(result.names[class_id])
        if label not in allowed_classes:
            continue

        confidence = float(box.conf[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        color = COLORS.get(label, (255, 255, 255))
        text = f"{label} {confidence:.0%}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame,
            text,
            (x1, max(20, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            cv2.LINE_AA,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Detect people, cigarettes, and smoke from a webcam or video."
    )
    parser.add_argument(
        "--source",
        default="0",
        help="Webcam index or video path (default: 0).",
    )
    parser.add_argument(
        "--smoking-model",
        type=Path,
        default=DEFAULT_SMOKING_MODEL,
        help=f"Smoking model path (default: {DEFAULT_SMOKING_MODEL}).",
    )
    parser.add_argument(
        "--person-model",
        type=Path,
        default=DEFAULT_PERSON_MODEL,
        help=f"Person model path (default: {DEFAULT_PERSON_MODEL}).",
    )
    parser.add_argument(
        "--smoking-conf",
        type=float,
        default=0.15,
        help="Confidence threshold for cigarette/smoke (default: 0.15).",
    )
    parser.add_argument(
        "--person-conf",
        type=float,
        default=0.25,
        help="Confidence threshold for people (default: 0.25).",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=512,
        help="Smoking inference image size; model was trained at 512 (default: 512).",
    )
    parser.add_argument(
        "--frame-skip",
        type=int,
        default=1,
        help="Run smoking inference every N frames (default: 1).",
    )
    parser.add_argument(
        "--person-skip",
        type=int,
        default=10,
        help="Run person inference every N frames (default: 10).",
    )
    parser.add_argument(
        "--person-imgsz",
        type=int,
        default=320,
        help="Image size for person inference; lower is faster (default: 320).",
    )
    parser.add_argument("--device", default=None, help="Ultralytics device, e.g. cpu or mps.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.frame_skip < 1:
        raise ValueError("--frame-skip must be at least 1")
    if args.person_skip < 1:
        raise ValueError("--person-skip must be at least 1")
    if args.imgsz < 32:
        raise ValueError("--imgsz must be at least 32")
    if args.person_imgsz < 32:
        raise ValueError("--person-imgsz must be at least 32")
    if not 0 < args.smoking_conf <= 1:
        raise ValueError("--smoking-conf must be between 0 and 1")
    if not 0 < args.person_conf <= 1:
        raise ValueError("--person-conf must be between 0 and 1")

    if not args.smoking_model.exists():
        raise FileNotFoundError(f"Smoking model not found: {args.smoking_model}")
    if not args.person_model.exists():
        raise FileNotFoundError(f"Person model not found: {args.person_model}")

    smoking_model = YOLO(str(args.smoking_model))
    person_model = YOLO(str(args.person_model))
    source = parse_source(args.source)
    capture = cv2.VideoCapture(source)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open video source: {source}")
    # Keep the displayed frame close to real time instead of processing an old queue.
    capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    print(
        "Loaded classes: "
        f"smoking={smoking_model.names}, person={person_model.names}. "
        "Press q in the camera window to close.",
        flush=True,
    )
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, 960, 720)

    smoking_results: list[Any] = []
    person_results: list[Any] = []
    frame_index = 0
    started_at = time.perf_counter()

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                raise RuntimeError(f"Unable to read a frame from source: {source}")

            if frame_index % args.frame_skip == 0:
                smoking_results = smoking_model.predict(
                    source=frame,
                    conf=args.smoking_conf,
                    imgsz=args.imgsz,
                    device=args.device,
                    verbose=False,
                )

            if frame_index % args.person_skip == 0:
                person_results = person_model.predict(
                    source=frame,
                    conf=args.person_conf,
                    imgsz=args.person_imgsz,
                    device=args.device,
                    verbose=False,
                )

            for result in smoking_results:
                draw_detections(frame, result, {"cigarette", "smoke"})
            for result in person_results:
                draw_detections(frame, result, {"person"})

            frame_index += 1
            elapsed = time.perf_counter() - started_at
            fps = frame_index / elapsed if elapsed > 0 else 0.0
            cv2.putText(
                frame,
                f"FPS {fps:.1f} | smoke 1/{args.frame_skip} | person 1/{args.person_skip}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow(WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
