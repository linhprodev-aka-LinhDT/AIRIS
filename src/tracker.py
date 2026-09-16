from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from src.detector import Detection


@dataclass
class Track:
    track_id: int
    class_name: str
    bbox: tuple[float, float, float, float]
    confidence: float
    age: int = 0
    hits: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> "Track":
        return Track(
            track_id=self.track_id,
            class_name=self.class_name,
            bbox=self.bbox,
            confidence=self.confidence,
            age=self.age,
            hits=self.hits,
            metadata=dict(self.metadata),
        )


class Tracker:
    """Simple, deterministic tracker for AIRIS that keeps a stable track_id for each moving person."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._tracks: dict[int, Track] = {}
        self._next_track_id = 1

    def update(self, detections: list[Detection]) -> list[Track]:
        if not detections:
            return []

        active_tracks: list[Track] = []
        used_track_ids: set[int] = set()

        for detection in detections:
            if detection.class_name.lower() not in {"person", "people"}:
                continue

            best_match = self._find_best_match(detection, used_track_ids)
            if best_match is None:
                track = self._create_track(detection)
                active_tracks.append(track.snapshot())
                used_track_ids.add(track.track_id)
                continue

            track = self._tracks[best_match]
            track.bbox = detection.bbox
            track.confidence = detection.confidence
            track.age += 1
            track.hits += 1
            used_track_ids.add(best_match)
            active_tracks.append(track.snapshot())

        return active_tracks

    def _create_track(self, detection: Detection) -> Track:
        track = Track(
            track_id=self._next_track_id,
            class_name=detection.class_name,
            bbox=detection.bbox,
            confidence=detection.confidence,
            age=1,
            hits=1,
            metadata={"source_class_id": detection.class_id},
        )
        self._next_track_id += 1
        self._tracks[track.track_id] = track
        self.logger.info("Track created: id=%s class=%s", track.track_id, track.class_name)
        return track

    def _find_best_match(self, detection: Detection, used_track_ids: set[int]) -> int | None:
        best_track_id: int | None = None
        best_distance: float | None = None

        for track_id, track in self._tracks.items():
            if track_id in used_track_ids:
                continue

            distance = self._bbox_distance(track.bbox, detection.bbox)
            if best_distance is None or distance < best_distance:
                best_distance = distance
                best_track_id = track_id

        if best_track_id is None:
            return None

        threshold = 25.0
        if best_distance is not None and best_distance <= threshold:
            return best_track_id
        return None

    @staticmethod
    def _bbox_distance(box_a: tuple[float, float, float, float], box_b: tuple[float, float, float, float]) -> float:
        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        center_a = ((ax1 + ax2) / 2.0, (ay1 + ay2) / 2.0)
        center_b = ((bx1 + bx2) / 2.0, (by1 + by2) / 2.0)

        dx = center_a[0] - center_b[0]
        dy = center_a[1] - center_b[1]
        return float((dx ** 2 + dy ** 2) ** 0.5)

    @property
    def tracks(self) -> list[Track]:
        return [track.snapshot() for track in self._tracks.values()]
