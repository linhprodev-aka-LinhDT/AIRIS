from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class SchoolSummary(BaseModel):
    school_id: str
    school_name: str
    zone_count: int = 0
    camera_count: int = 0
    score: int = 0
    improvement: int = 0
    coverage: float = 0.0
    smoke_density: float = 0.0
    status: str = "unknown"
    achievements: list[str] = Field(default_factory=list)


class ZoneSummary(BaseModel):
    zone_id: str
    school_id: str
    zone_name: str
    camera_id: str | None = None
    location: dict[str, Any] = Field(default_factory=dict)
    event_count: int = 0
    smoke_density: float = 0.0
    last_event: str | None = None
    status: str = "unknown"
    coverage: float = 0.0


class CameraSummary(BaseModel):
    camera_id: str
    school_id: str
    name: str
    zone_id: str | None = None
    status: str = "offline"
    stream_url: str | None = None
    health: float = 0.0


class EventSummary(BaseModel):
    event_id: str | None = None
    school_id: str | None = None
    zone_id: str | None = None
    camera_id: str | None = None
    event_type: str | None = None
    timestamp: str | None = None
    confidence: float | None = None
    duration: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DashboardStatistics(BaseModel):
    total_events: int = 0
    smoke_events: int = 0
    smoking_behavior_events: int = 0
    active_cameras: int = 0
    monitored_zones: int = 0
    smoke_free_zones: int = 0
    hourly: list[dict[str, Any]] = Field(default_factory=list)
    daily: list[dict[str, Any]] = Field(default_factory=list)
    weekly: list[dict[str, Any]] = Field(default_factory=list)
    monthly: list[dict[str, Any]] = Field(default_factory=list)


class HeatmapPoint(BaseModel):
    zone_id: str
    school_id: str
    smoke_density: float = 0.0
    level: str = "low"
    event_count: int = 0


class LeaderboardEntry(BaseModel):
    school_id: str
    school_name: str
    score: int = 0
    improvement: int = 0
    coverage: float = 0.0


class Achievement(BaseModel):
    id: str
    title: str
    description: str
    school_id: str
    badge: str


class ApiHealth(BaseModel):
    status: str = "ok"
    demo_mode: bool = True
    timestamp: str
