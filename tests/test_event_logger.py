from __future__ import annotations

from src.event_logger import EventLogger


def test_event_logger_creates_database_and_records_event(tmp_path) -> None:
    database_path = tmp_path / "airis.db"
    logger = EventLogger(database_path=str(database_path))

    event_id = logger.log_event(
        "SMOKING_DETECTED",
        track_id=7,
        confidence=0.94,
        snapshot_path="snapshots/test.png",
        duration=12.5,
        metadata={"source": "test"},
    )

    assert event_id > 0
    rows = logger.get_events(limit=10)
    assert len(rows) == 1
    assert rows[0]["event_type"] == "SMOKING_DETECTED"
    assert rows[0]["track_id"] == 7
    assert rows[0]["confidence"] == 0.94
    assert rows[0]["snapshot_path"] == "snapshots/test.png"
