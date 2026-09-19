from __future__ import annotations

from datetime import datetime, timezone
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
from src.api.schemas import AirQualityReadingPayload
from src.sensors import AirQualityReading, SensorVerifier

router = APIRouter()
sensor_verifier = SensorVerifier()


@router.get("/health")
async def api_health() -> dict[str, Any]:
    return {
        "status": "ok",
        "demo_mode": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sensor_zones": len(sensor_verifier.latest()),
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


@router.post("/sensors/readings")
async def ingest_sensor_reading(payload: AirQualityReadingPayload) -> dict[str, Any]:
    reading = AirQualityReading(
        sensor_id=payload.sensor_id,
        zone_id=payload.zone_id,
        timestamp=payload.timestamp or datetime.now(timezone.utc).isoformat(),
        pm25=payload.pm25,
        co_ppm=payload.co_ppm,
        co2_ppm=payload.co2_ppm,
        voc_index=payload.voc_index,
        smoke_alarm=payload.smoke_alarm,
    )
    sensor_verifier.ingest(reading)
    return {"reading": reading.__dict__, "verification": sensor_verifier.verify(reading.zone_id)}


@router.get("/sensors/readings")
async def get_sensor_readings(zone_id: str | None = None) -> dict[str, Any]:
    return {"readings": [reading.__dict__ for reading in sensor_verifier.latest(zone_id)]}


@router.get("/sensors/verify/{zone_id}")
async def verify_sensor_zone(zone_id: str) -> dict[str, Any]:
    return {"verification": sensor_verifier.verify(zone_id)}


@router.get("/awareness/questions")
async def get_awareness_questions() -> dict[str, Any]:
    return {
        "questions": [
            {
                "question_id": "air-1",
                "question": "Khi cảm biến báo khói bất thường, hành động phù hợp nhất là gì?",
                "options": ["Bỏ qua", "Báo đội ứng trực và ban quản lý", "Tắt cảm biến"],
                "points": 10,
            },
            {
                "question_id": "privacy-1",
                "question": "AIRIS lưu dữ liệu nào sau khi xử lý camera?",
                "options": ["Video nhận diện khuôn mặt", "Hồ sơ cá nhân", "Sự kiện tổng hợp dạng văn bản"],
                "points": 10,
            },
        ]
    }
