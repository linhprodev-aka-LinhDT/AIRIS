from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite
from typing import Any

from config import CONFIG


@dataclass(frozen=True)
class AirQualityReading:
    sensor_id: str
    zone_id: str
    timestamp: str
    pm25: float | None = None
    co_ppm: float | None = None
    co2_ppm: float | None = None
    voc_index: float | None = None
    smoke_alarm: bool = False

    @classmethod
    def now(cls, sensor_id: str, zone_id: str, **values: Any) -> "AirQualityReading":
        return cls(sensor_id=sensor_id, zone_id=zone_id, timestamp=datetime.now(timezone.utc).isoformat(), **values)


class SensorVerifier:
    """Correlates an anonymous camera event with the latest zone sensor reading."""

    def __init__(self, window_seconds: int = CONFIG.sensor_verification_window_seconds) -> None:
        self.window_seconds = window_seconds
        self._latest: dict[str, AirQualityReading] = {}

    def ingest(self, reading: AirQualityReading) -> AirQualityReading:
        self._latest[reading.zone_id] = reading
        return reading

    def latest(self, zone_id: str | None = None) -> list[AirQualityReading]:
        if zone_id is None:
            return list(self._latest.values())
        reading = self._latest.get(zone_id)
        return [reading] if reading else []

    def verify(self, zone_id: str, event_timestamp: str | None = None) -> dict[str, Any]:
        reading = self._latest.get(zone_id)
        if reading is None:
            return {"status": "unverified", "reason": "no_reading"}
        abnormal = reading.smoke_alarm or any(
            value is not None and isfinite(value) and value >= threshold
            for value, threshold in ((reading.pm25, CONFIG.smoke_pm25_threshold), (reading.co_ppm, CONFIG.smoke_co_threshold))
        )
        return {
            "status": "corroborated" if abnormal else "normal",
            "sensor_id": reading.sensor_id,
            "zone_id": reading.zone_id,
            "timestamp": reading.timestamp,
            "pm25": reading.pm25,
            "co_ppm": reading.co_ppm,
            "smoke_alarm": reading.smoke_alarm,
        }