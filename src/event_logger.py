from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import CONFIG


class EventLogger:
    """SQLite-backed logger for AIRIS event records without storing personal identities."""

    def __init__(self, database_path: str | Path = CONFIG.database_path) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    track_id INTEGER,
                    confidence REAL,
                    snapshot_path TEXT,
                    duration REAL,
                    metadata TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        self.logger.info("SQLite database ready: %s", self.database_path)

    def log_event(
        self,
        event_type: str,
        *,
        track_id: int | None = None,
        confidence: float | None = None,
        snapshot_path: str | None = None,
        duration: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        now = datetime.now(timezone.utc).isoformat()
        payload = json.dumps(metadata or {}, ensure_ascii=True)

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO events (timestamp, event_type, track_id, confidence, snapshot_path, duration, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    event_type,
                    track_id,
                    confidence,
                    snapshot_path,
                    duration,
                    payload,
                ),
            )
            return int(cursor.lastrowid)

    def get_events(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM events
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def clear_events(self) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM events")
