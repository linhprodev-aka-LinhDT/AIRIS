from __future__ import annotations

import numpy as np

from src.alert_manager import AlertManager


def test_alert_manager_saves_snapshot_and_enforces_cooldown(tmp_path) -> None:
    manager = AlertManager(snapshot_dir=tmp_path, cooldown_seconds=10)
    frame = np.zeros((100, 100, 3), dtype=np.uint8)

    first = manager.create_alert(frame, track_id=3, confidence=0.95)
    assert first["event_type"] == "SMOKING_DETECTED"
    assert first["track_id"] == 3
    assert first["snapshot_path"].endswith(".png")

    last_timestamp = manager._last_alert_time
    assert last_timestamp is not None
    assert manager.should_trigger(now=last_timestamp + 1) is False

    second = manager.create_alert(frame, track_id=3, confidence=0.96)
    assert second["snapshot_path"] != first["snapshot_path"]

    assert manager.should_trigger(now=last_timestamp + 11) is True
