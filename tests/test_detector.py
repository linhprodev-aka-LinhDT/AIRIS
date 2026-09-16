from __future__ import annotations

import numpy as np

from src.detector import Detection, RoboflowDetector, YOLODetector


def test_detector_returns_detection_objects() -> None:
    detector = YOLODetector(model_path="yolo11n.pt", confidence_threshold=0.25, iou_threshold=0.45, device="cpu")

    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    detections = detector.detect(frame)

    assert isinstance(detections, list)
    for detection in detections:
        assert isinstance(detection, Detection)
        assert detection.class_id >= 0
        assert isinstance(detection.class_name, str)
        assert 0.0 <= detection.confidence <= 1.0
        assert len(detection.bbox) == 4


def test_roboflow_detector_maps_predictions_and_filters_confidence() -> None:
    class FakeClient:
        def infer(self, frame: np.ndarray, model_id: str) -> dict[str, list[dict[str, float | str]]]:
            assert frame.shape == (100, 120, 3)
            assert model_id == "smoking-detection-3gefl/4"
            return {
                "predictions": [
                    {"x": 50, "y": 40, "width": 20, "height": 10, "confidence": 0.9, "class": "smoking", "class_id": 1},
                    {"x": 10, "y": 10, "width": 8, "height": 8, "confidence": 0.1, "class": "smoking", "class_id": 1},
                ]
            }

    detector = RoboflowDetector(client=FakeClient(), confidence_threshold=0.25)
    detections = detector.detect(np.zeros((100, 120, 3), dtype=np.uint8))

    assert len(detections) == 1
    assert detections[0] == Detection(1, "smoking", 0.9, (40.0, 35.0, 60.0, 45.0))
