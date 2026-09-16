from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
DATABASE_DIR = DATA_DIR / "database"
INPUT_DIR = DATA_DIR / "input"


@dataclass(frozen=True)
class AppConfig:
    project_name: str = "AIRIS"
    model_path: str = str(MODELS_DIR / "yolo11n.pt")
    source: int | str = 0
    confidence_threshold: float = 0.25
    iou_threshold: float = 0.45
    tracking_max_age: int = 30
    tracking_min_hits: int = 3
    temporal_threshold: int = 5
    temporal_min_evidence_frames: int = 2
    alert_cooldown_seconds: float = 20.0
    enable_hand_mouth: bool = False
    save_snapshots: bool = True
    show_preview: bool = False
    log_level: str = "INFO"
    database_path: str = str(DATABASE_DIR / "airis.db")
    snapshot_dir: str = str(SNAPSHOT_DIR)
    input_dir: str = str(INPUT_DIR)
    debug: bool = False


CONFIG = AppConfig()
