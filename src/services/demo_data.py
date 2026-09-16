from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


DEMO_SCHOOLS = [
    {
        "school_id": "school-a",
        "school_name": "School A",
        "zone_count": 5,
        "camera_count": 5,
        "score": 245,
        "improvement": 32,
        "coverage": 0.97,
        "smoke_density": 0.22,
        "status": "good",
        "achievements": ["Smoke-Free Zone", "7 Days Improvement", "High Monitoring Coverage"],
    },
    {
        "school_id": "school-b",
        "school_name": "School B",
        "zone_count": 4,
        "camera_count": 4,
        "score": 198,
        "improvement": 18,
        "coverage": 0.90,
        "smoke_density": 0.31,
        "status": "moderate",
        "achievements": ["Community Participation", "Consistency Award"],
    },
]


def _iso_now(offset_hours: int = 0) -> str:
    dt = datetime.now(timezone.utc) + timedelta(hours=offset_hours)
    return dt.isoformat()


DEMO_ZONES = [
    {
        "zone_id": "zone-a",
        "school_id": "school-a",
        "zone_name": "Building A Yard",
        "camera_id": "cam-1",
        "location": {"x": 20, "y": 30, "label": "North Yard"},
        "event_count": 4,
        "smoke_density": 0.18,
        "last_event": _iso_now(-3),
        "status": "low",
        "coverage": 0.98,
    },
    {
        "zone_id": "zone-b",
        "school_id": "school-a",
        "zone_name": "Cafeteria",
        "camera_id": "cam-2",
        "location": {"x": 50, "y": 62, "label": "Main Hall"},
        "event_count": 6,
        "smoke_density": 0.34,
        "last_event": _iso_now(-1),
        "status": "medium",
        "coverage": 0.95,
    },
    {
        "zone_id": "zone-c",
        "school_id": "school-b",
        "zone_name": "Parking Lot",
        "camera_id": "cam-3",
        "location": {"x": 65, "y": 40, "label": "South Edge"},
        "event_count": 7,
        "smoke_density": 0.42,
        "last_event": _iso_now(-2),
        "status": "high",
        "coverage": 0.88,
    },
    {
        "zone_id": "zone-d",
        "school_id": "school-b",
        "zone_name": "Sports Field",
        "camera_id": "cam-4",
        "location": {"x": 35, "y": 75, "label": "Field"},
        "event_count": 3,
        "smoke_density": 0.21,
        "last_event": _iso_now(-5),
        "status": "low",
        "coverage": 0.96,
    },
]


DEMO_CAMERAS = [
    {"camera_id": "cam-1", "school_id": "school-a", "name": "Camera 1", "zone_id": "zone-a", "status": "online", "stream_url": "demo://school-a/cam-1", "health": 0.98},
    {"camera_id": "cam-2", "school_id": "school-a", "name": "Camera 2", "zone_id": "zone-b", "status": "online", "stream_url": "demo://school-a/cam-2", "health": 0.96},
    {"camera_id": "cam-3", "school_id": "school-b", "name": "Camera 3", "zone_id": "zone-c", "status": "degraded", "stream_url": "demo://school-b/cam-3", "health": 0.88},
    {"camera_id": "cam-4", "school_id": "school-b", "name": "Camera 4", "zone_id": "zone-d", "status": "online", "stream_url": "demo://school-b/cam-4", "health": 0.94},
]


DEMO_EVENTS = [
    {
        "event_id": "evt-1001",
        "school_id": "school-a",
        "zone_id": "zone-b",
        "camera_id": "cam-2",
        "event_type": "SMOKING_DETECTED",
        "timestamp": _iso_now(-1),
        "confidence": 0.93,
        "duration": 14.2,
        "metadata": {"source": "DEMO", "state": "SMOKING", "severity": "medium"},
    },
    {
        "event_id": "evt-1002",
        "school_id": "school-a",
        "zone_id": "zone-a",
        "camera_id": "cam-1",
        "event_type": "SMOKE_DETECTED",
        "timestamp": _iso_now(-3),
        "confidence": 0.79,
        "duration": 6.1,
        "metadata": {"source": "DEMO", "state": "POSSIBLE_SMOKING", "severity": "low"},
    },
    {
        "event_id": "evt-1003",
        "school_id": "school-b",
        "zone_id": "zone-c",
        "camera_id": "cam-3",
        "event_type": "SMOKING_DETECTED",
        "timestamp": _iso_now(-2),
        "confidence": 0.91,
        "duration": 18.4,
        "metadata": {"source": "DEMO", "state": "SMOKING", "severity": "high"},
    },
    {
        "event_id": "evt-1004",
        "school_id": "school-b",
        "zone_id": "zone-d",
        "camera_id": "cam-4",
        "event_type": "SMOKE_DETECTED",
        "timestamp": _iso_now(-5),
        "confidence": 0.68,
        "duration": 4.2,
        "metadata": {"source": "DEMO", "state": "POSSIBLE_SMOKING", "severity": "low"},
    },
]


def get_demo_statistics() -> dict[str, Any]:
    return {
        "total_events": 14,
        "smoke_events": 9,
        "smoking_behavior_events": 5,
        "active_cameras": 4,
        "monitored_zones": 8,
        "smoke_free_zones": 5,
        "hourly": [
            {"hour": "00:00", "events": 1},
            {"hour": "06:00", "events": 2},
            {"hour": "09:00", "events": 4},
            {"hour": "12:00", "events": 3},
            {"hour": "15:00", "events": 2},
            {"hour": "18:00", "events": 2},
        ],
        "daily": [
            {"date": "Mon", "events": 4},
            {"date": "Tue", "events": 3},
            {"date": "Wed", "events": 5},
            {"date": "Thu", "events": 2},
        ],
        "weekly": [
            {"week": "W1", "events": 18},
            {"week": "W2", "events": 14},
            {"week": "W3", "events": 12},
            {"week": "W4", "events": 9},
        ],
        "monthly": [
            {"month": "Jan", "events": 26},
            {"month": "Feb", "events": 21},
            {"month": "Mar", "events": 18},
            {"month": "Apr", "events": 14},
        ],
    }


def get_demo_heatmap() -> dict[str, Any]:
    return {
        "zones": [
            {"zone_id": "zone-a", "school_id": "school-a", "smoke_density": 0.18, "level": "low", "event_count": 4},
            {"zone_id": "zone-b", "school_id": "school-a", "smoke_density": 0.34, "level": "medium", "event_count": 6},
            {"zone_id": "zone-c", "school_id": "school-b", "smoke_density": 0.42, "level": "high", "event_count": 7},
            {"zone_id": "zone-d", "school_id": "school-b", "smoke_density": 0.21, "level": "low", "event_count": 3},
        ]
    }


def get_demo_leaderboard() -> list[dict[str, Any]]:
    return [
        {"school_id": "school-a", "school_name": "School A", "score": 245, "improvement": 32, "coverage": 0.97},
        {"school_id": "school-b", "school_name": "School B", "score": 198, "improvement": 18, "coverage": 0.90},
    ]


def get_demo_achievements() -> list[dict[str, Any]]:
    return [
        {"id": "achievement-1", "title": "7 Days Smoke-Free", "description": "No smoke event for 7 consecutive days.", "school_id": "school-a", "badge": "🏆"},
        {"id": "achievement-2", "title": "High Monitoring Coverage", "description": "Monitoring coverage above 95%.", "school_id": "school-a", "badge": "📹"},
        {"id": "achievement-3", "title": "Community Participation", "description": "Participation in community smoke-free campaign.", "school_id": "school-b", "badge": "🤝"},
    ]
