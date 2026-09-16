from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from src.services.demo_data import (
    DEMO_CAMERAS,
    DEMO_EVENTS,
    DEMO_SCHOOLS,
    DEMO_ZONES,
    get_demo_achievements,
    get_demo_heatmap,
    get_demo_leaderboard,
    get_demo_statistics,
)
from src.services.privacy import sanitize_event, sanitize_school_payload

router = APIRouter()


@router.get("/health")
async def api_health() -> dict[str, Any]:
    return {
        "status": "ok",
        "demo_mode": True,
        "timestamp": "2026-09-16T00:00:00Z",
    }


@router.get("/schools")
async def get_schools() -> dict[str, Any]:
    items = [sanitize_school_payload(item) for item in DEMO_SCHOOLS]
    return {"schools": items}


@router.get("/schools/{school_id}")
async def get_school(school_id: str) -> dict[str, Any]:
    school = next((item for item in DEMO_SCHOOLS if item["school_id"] == school_id), DEMO_SCHOOLS[0])
    return {"school": sanitize_school_payload(school)}


@router.get("/zones")
async def get_zones() -> dict[str, Any]:
    return {"zones": DEMO_ZONES}


@router.get("/zones/{zone_id}")
async def get_zone(zone_id: str) -> dict[str, Any]:
    zone = next((item for item in DEMO_ZONES if item["zone_id"] == zone_id), DEMO_ZONES[0])
    return {"zone": zone}


@router.get("/events")
async def get_events() -> dict[str, Any]:
    return {"events": [sanitize_event(item) for item in DEMO_EVENTS]}


@router.get("/statistics")
async def get_statistics() -> dict[str, Any]:
    return get_demo_statistics()


@router.get("/heatmap")
async def get_heatmap() -> dict[str, Any]:
    return get_demo_heatmap()


@router.get("/leaderboard")
async def get_leaderboard() -> dict[str, Any]:
    return {"leaderboard": get_demo_leaderboard()}


@router.get("/achievements")
async def get_achievements() -> dict[str, Any]:
    return {"achievements": get_demo_achievements()}


@router.get("/cameras")
async def get_cameras() -> dict[str, Any]:
    return {"cameras": DEMO_CAMERAS}


@router.get("/cameras/{camera_id}")
async def get_camera(camera_id: str) -> dict[str, Any]:
    camera = next((item for item in DEMO_CAMERAS if item["camera_id"] == camera_id), DEMO_CAMERAS[0])
    return {"camera": camera}
