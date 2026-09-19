from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import requests
from ultralytics import YOLO

from config import CONFIG


@dataclass(frozen=True)
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]
    keypoints: tuple[tuple[float, float, float], ...] = ()


class YOLOPoseDetector:
    """Ultralytics pose detector that keeps only privacy-safe body landmarks."""

    def __init__(
        self,
        model_path: str | Path = CONFIG.pose_model_path,
        confidence_threshold: float = CONFIG.confidence_threshold,
        device: str = "cpu",
    ) -> None:
        self.model_path = str(model_path)
        self.confidence_threshold = confidence_threshold
        self.device = device
        self.logger = logging.getLogger(__name__)
        # Ultralytics downloads the official pose weights on first use when absent.
        self.model = YOLO(self.model_path if Path(self.model_path).exists() else "yolo11n-pose.pt")

    def detect(self, frame: np.ndarray) -> list[Detection]:
        results = self.model.predict(
            source=frame,
            conf=self.confidence_threshold,
            device=self.device,
            verbose=False,
            imgsz=640,
        )
        detections: list[Detection] = []
        for result in results:
            if result.boxes is None or result.keypoints is None:
                continue
            boxes = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            points = result.keypoints.data.cpu().numpy()
            for box, confidence, keypoint_set in zip(boxes, confs, points):
                detections.append(
                    Detection(
                        class_id=0,
                        class_name="person",
                        confidence=float(confidence),
                        bbox=(float(box[0]), float(box[1]), float(box[2]), float(box[3])),
                        keypoints=tuple(tuple(float(value) for value in point) for point in keypoint_set),
                    )
                )
        return detections

    @property
    def model_name(self) -> str:
        return self.model_path


def pose_smoking_evidence(detection: Detection) -> bool:
    """Return true when a visible wrist is close to the person's mouth."""
    if len(detection.keypoints) < 11:
        return False
    x1, y1, x2, y2 = detection.bbox
    body_width = max(x2 - x1, 1.0)
    nose_x, nose_y, nose_score = detection.keypoints[0]
    wrist_points = (detection.keypoints[9], detection.keypoints[10])
    if nose_score < 0.35:
        return False
    for wrist_x, wrist_y, wrist_score in wrist_points:
        if wrist_score < 0.35:
            continue
        distance = ((wrist_x - nose_x) ** 2 + (wrist_y - nose_y) ** 2) ** 0.5
        if distance <= body_width * 0.22:
            return True
    return False


class YOLODetector:
    """Wrapper around Ultralytics YOLO model for AIRIS detection pipeline."""

    def __init__(
        self,
        model_path: str | Path = CONFIG.model_path,
        confidence_threshold: float = CONFIG.confidence_threshold,
        iou_threshold: float = CONFIG.iou_threshold,
        device: str = "cpu",
        verbose: bool = False,
    ) -> None:
        self.model_path = str(model_path)
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.device = device
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        self.model: YOLO | None = None
        self._load_model()

    def _load_model(self) -> None:
        resolved_model = Path(self.model_path)
        if not resolved_model.exists():
            self.logger.warning(
                "Model file not found at %s. Falling back to the default Ultralytics pretrained YOLO model for architecture testing.",
                self.model_path,
            )
            fallback_model = "yolo11n.pt"
            self.model = YOLO(fallback_model)
            self.model_path = fallback_model
            return

        self.model = YOLO(str(resolved_model))
        self.logger.info("YOLO model loaded: %s", self.model_path)

    def detect(self, frame: np.ndarray) -> list[Detection]:
        if self.model is None:
            raise RuntimeError("YOLO model is not initialized.")

        results = self.model.predict(
            source=frame,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            device=self.device,
            verbose=self.verbose,
            imgsz=640,
        )

        detections: list[Detection] = []
        for result in results:
            if result.boxes is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            names = getattr(result.names, "__getitem__", lambda idx: str(idx))

            for box, confidence, class_id in zip(boxes, confs, class_ids):
                class_name = names(class_id) if callable(names) else str(class_id)
                detections.append(
                    Detection(
                        class_id=int(class_id),
                        class_name=str(class_name),
                        confidence=float(confidence),
                        bbox=(float(box[0]), float(box[1]), float(box[2]), float(box[3])),
                    )
                )

        return detections

    @property
    def model_name(self) -> str:
        return self.model_path


class RoboflowDetector:
    """Detector backed by a public Roboflow Serverless model."""

    def __init__(
        self,
        model_id: str = "smoking-detection-3gefl/4",
        api_key: str | None = None,
        api_url: str = "https://serverless.roboflow.com",
        confidence_threshold: float = CONFIG.confidence_threshold,
        client: Any | None = None,
    ) -> None:
        self.model_id = model_id
        self.api_url = api_url.rstrip("/")
        self.confidence_threshold = confidence_threshold
        self.logger = logging.getLogger(__name__)
        self._api_key = api_key or os.environ.get("ROBOFLOW_API_KEY")

        if client is not None:
            self.client = client
            return

        if not self._api_key:
            raise ValueError("ROBOFLOW_API_KEY must be set to use the Roboflow detector.")

        try:
            from inference_sdk import InferenceConfiguration, InferenceHTTPClient
        except ImportError:
            self.client = None
            self.logger.info("inference-sdk unavailable; using the Roboflow HTTP API fallback.")
        else:
            self.client = InferenceHTTPClient(api_url=self.api_url, api_key=self._api_key).configure(
                InferenceConfiguration(api_key_transport="header")
            )

    def detect(self, frame: np.ndarray) -> list[Detection]:
        if self.client is not None:
            result = self.client.infer(frame, model_id=self.model_id)
        else:
            ok, encoded_frame = cv2.imencode(".jpg", frame)
            if not ok:
                raise RuntimeError("Could not encode the frame for Roboflow inference.")

            response = requests.post(
                f"{self.api_url}/{self.model_id}",
                files={"file": ("frame.jpg", encoded_frame.tobytes(), "image/jpeg")},
                headers={"Authorization": f"Bearer {self._api_key}"},
                params={"confidence": self.confidence_threshold},
                timeout=30,
            )
            response.raise_for_status()
            result = response.json()

        predictions = result.get("predictions", [])
        detections: list[Detection] = []

        for prediction in predictions:
            confidence = float(prediction.get("confidence", 0.0))
            if confidence < self.confidence_threshold:
                continue

            center_x = float(prediction["x"])
            center_y = float(prediction["y"])
            width = float(prediction["width"])
            height = float(prediction["height"])
            detections.append(
                Detection(
                    class_id=int(prediction.get("class_id", -1)),
                    class_name=str(prediction.get("class", "unknown")),
                    confidence=confidence,
                    bbox=(
                        center_x - width / 2.0,
                        center_y - height / 2.0,
                        center_x + width / 2.0,
                        center_y + height / 2.0,
                    ),
                )
            )

        return detections

    @property
    def model_name(self) -> str:
        return self.model_id
