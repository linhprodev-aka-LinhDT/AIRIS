from __future__ import annotations

from typing import Any


def sanitize_event(event: dict[str, Any]) -> dict[str, Any]:
    """Return event data with personal identifiers removed."""
    sanitized = dict(event)
    sanitized.pop("track_id", None)
    sanitized.pop("student_id", None)
    sanitized.pop("face_embedding", None)
    sanitized.pop("face", None)
    sanitized.pop("person_profile", None)
    sanitized.pop("smoker_history", None)
    sanitized["metadata"] = {"source": sanitized.get("metadata", {}).get("source", "AIRIS")} if isinstance(sanitized.get("metadata"), dict) else {}
    return sanitized


def sanitize_school_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "school_id": payload.get("school_id"),
        "school_name": payload.get("school_name"),
        "score": payload.get("score"),
        "improvement": payload.get("improvement"),
        "coverage": payload.get("coverage"),
        "smoke_density": payload.get("smoke_density"),
        "status": payload.get("status"),
        "achievements": payload.get("achievements", []),
    }
