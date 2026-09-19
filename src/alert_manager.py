from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from config import CONFIG


class AlertManager:
    """Handles smoking alerts, snapshots, and future ESP32 integration hooks."""

    def __init__(self, snapshot_dir: str | Path = CONFIG.snapshot_dir, cooldown_seconds: float = CONFIG.alert_cooldown_seconds, save_snapshots: bool = True) -> None:
        self.snapshot_dir = Path(snapshot_dir)
        self.cooldown_seconds = cooldown_seconds
        self.save_snapshots = save_snapshots
        self.logger = logging.getLogger(__name__)
        self._last_alert_time: float | None = None
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)

    def should_trigger(self, now: float | None = None) -> bool:
        if now is None:
            now = datetime.now(timezone.utc).timestamp()

        if self._last_alert_time is None:
            return True
        return (now - self._last_alert_time) >= self.cooldown_seconds

    def create_alert(
        self,
        frame: np.ndarray,
        track_id: int,
        confidence: float,
        *,
        event_type: str = "SMOKING_DETECTED",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        metadata = metadata or {}

        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%d_%H%M%S_%f")
        snapshot_path = self.snapshot_dir / f"alert_{event_type.lower()}_{track_id}_{timestamp}.png"

        saved_snapshot: str | None = None
        if self.save_snapshots:
            cv2.imwrite(str(snapshot_path), frame)
            saved_snapshot = str(snapshot_path)
            self.logger.info("Alert snapshot saved: %s", snapshot_path)

        self._last_alert_time = now.timestamp()

        return {
            "event_type": event_type,
            "track_id": track_id,
            "confidence": confidence,
            "snapshot_path": saved_snapshot,
            "timestamp": now.isoformat(),
            "metadata": metadata,
        }

    def draw_alert_overlay(self, frame: np.ndarray, track_id: int, confidence: float) -> np.ndarray:
        overlay = frame.copy()
        height, width = overlay.shape[:2]
        label = f"SMOKING ALERT - Track {track_id} - conf {confidence:.2f}"

        cv2.putText(
            overlay,
            label,
            (10, max(30, height - 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.rectangle(overlay, (0, 0), (width - 1, height - 1), (0, 0, 255), 3)
        return overlay
