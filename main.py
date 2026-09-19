from __future__ import annotations

import argparse
import logging
from pathlib import Path

import cv2
import numpy as np

from config import CONFIG
from src.alert_manager import AlertManager
from src.detector import RoboflowDetector, YOLODetector, YOLOPoseDetector, pose_smoking_evidence
from src.event_logger import EventLogger
from src.temporal_analysis import TemporalAnalyzer, TemporalState
from src.tracker import Tracker
from src.video_capture import VideoCapture


def configure_logging(level: str = CONFIG.log_level) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AIRIS detection pipeline")
    parser.add_argument("--source", type=str, default=str(CONFIG.source), help="Camera index or path to video file")
    parser.add_argument("--backend", choices=("yolo", "roboflow", "pose"), default="pose", help="Detection backend")
    parser.add_argument("--model", type=str, default=CONFIG.model_path, help="Path to YOLO model")
    parser.add_argument("--model-id", default="smoking-detection-3gefl/4", help="Roboflow model ID")
    parser.add_argument("--api-url", default="https://serverless.roboflow.com", help="Roboflow inference API URL")
    parser.add_argument("--conf", type=float, default=CONFIG.confidence_threshold, help="Detection confidence threshold")
    parser.add_argument("--show", action="store_true", default=CONFIG.show_preview, help="Show preview window")
    parser.add_argument("--save", action="store_true", default=CONFIG.save_snapshots, help="Opt in to temporary alert snapshots")
    return parser.parse_args()


def _parse_source(value: str) -> int | str:
    return int(value) if value.isdigit() else value


def _is_smoke_like(class_name: str) -> bool:
    normalized = class_name.lower()
    smoke_keywords = {"smoke", "cigarette", "cigarette_smoke", "smoking", "vape", "e-cigarette"}
    return normalized in smoke_keywords or any(keyword in normalized for keyword in ("smoke", "cigarette", "vape"))


def _box_overlap(box_a: tuple[float, float, float, float], box_b: tuple[float, float, float, float]) -> bool:
    ax1, ay1, ax2, ay2 = box_a
    bx1, by1, bx2, by2 = box_b

    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


def _draw_detection(frame: np.ndarray, label: str, bbox: tuple[float, float, float, float], color: tuple[int, int, int]) -> None:
    x1, y1, x2, y2 = map(int, bbox)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(frame, label, (x1, max(20, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)


def main() -> int:
    configure_logging()
    args = parse_args()

    logging.info("AIRIS starting")
    logging.info("Source: %s", args.source)
    logging.info("Backend: %s", args.backend)
    logging.info("Model: %s", args.model_id if args.backend == "roboflow" else args.model)
    logging.info("Confidence threshold: %.2f", args.conf)

    try:
        if args.backend == "roboflow":
            detector = RoboflowDetector(model_id=args.model_id, api_url=args.api_url, confidence_threshold=args.conf)
        elif args.backend == "pose":
            detector = YOLOPoseDetector(confidence_threshold=args.conf, device="cpu")
        else:
            detector = YOLODetector(model_path=args.model, confidence_threshold=args.conf, device="cpu")
    except (RuntimeError, ValueError) as exc:
        logging.error("Detector initialization failed: %s", exc)
        return 1

    try:
        capture = VideoCapture(_parse_source(args.source))
        capture.open()
    except RuntimeError as exc:
        logging.error(str(exc))
        return 1

    tracker = Tracker()
    temporal_analyzer = TemporalAnalyzer(
        threshold=CONFIG.temporal_threshold,
        cooldown_frames=max(1, int(CONFIG.alert_cooldown_seconds)),
        confidence_threshold=CONFIG.confidence_threshold,
        min_evidence_frames=CONFIG.temporal_min_evidence_frames,
    )
    alert_manager = AlertManager(snapshot_dir=CONFIG.snapshot_dir, cooldown_seconds=CONFIG.alert_cooldown_seconds, save_snapshots=args.save)
    event_logger = EventLogger(database_path=CONFIG.database_path)

    try:
        while True:
            ok, frame = capture.read()
            if not ok or frame is None:
                logging.info("End of video stream reached.")
                break

            detections = detector.detect(frame)
            tracks = tracker.update(detections)

            track_decisions: dict[int, object] = {}
            for track in tracks:
                smoke_evidence = pose_smoking_evidence(next((d for d in detections if d.class_name == "person" and d.bbox == track.bbox), detections[0])) if detections else False
                for detection in detections:
                    if _is_smoke_like(detection.class_name) and _box_overlap(track.bbox, detection.bbox):
                        smoke_evidence = True
                        break

                decision = temporal_analyzer.update(track.track_id, smoke_evidence, track.confidence)
                track_decisions[track.track_id] = decision

                if decision.state == TemporalState.SMOKING and alert_manager.should_trigger():
                    alert_payload = alert_manager.create_alert(
                        frame,
                        track.track_id,
                        track.confidence,
                        event_type="SMOKING_DETECTED",
                        metadata={
                            "track_id": track.track_id,
                            "bbox": track.bbox,
                            "state": decision.state.value,
                        },
                    )
                    event_logger.log_event(
                        "SMOKING_DETECTED",
                        track_id=track.track_id,
                        confidence=track.confidence,
                        snapshot_path=alert_payload["snapshot_path"],
                        metadata=alert_payload["metadata"],
                    )
                    frame = alert_manager.draw_alert_overlay(frame, track.track_id, track.confidence)

                label = f"track:{track.track_id} {decision.state.value}"
                _draw_detection(frame, label, track.bbox, (0, 255, 255))

            for detection in detections:
                _draw_detection(frame, detection.class_name, detection.bbox, (0, 255, 0))

            if args.show:
                cv2.imshow("AIRIS", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            if args.save:
                pass

    finally:
        capture.release()
        if args.show:
            cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
