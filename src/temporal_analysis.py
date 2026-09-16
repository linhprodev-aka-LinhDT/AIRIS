from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TemporalState(str, Enum):
    UNKNOWN = "UNKNOWN"
    POSSIBLE_SMOKING = "POSSIBLE_SMOKING"
    SMOKING = "SMOKING"
    COOLDOWN = "COOLDOWN"


@dataclass
class TemporalDecision:
    track_id: int
    state: TemporalState
    triggered: bool
    confidence: float
    evidence_frames: int
    metadata: dict[str, Any] = field(default_factory=dict)


class TemporalAnalyzer:
    """State machine for smoking evidence accumulation per track_id."""

    def __init__(
        self,
        threshold: int = 5,
        cooldown_frames: int = 10,
        confidence_threshold: float = 0.7,
        min_evidence_frames: int = 2,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.threshold = threshold
        self.cooldown_frames = cooldown_frames
        self.confidence_threshold = confidence_threshold
        self.min_evidence_frames = min_evidence_frames
        self._history: dict[int, dict[str, Any]] = {}

    def update(self, track_id: int, smoking_evidence: bool, confidence: float) -> TemporalDecision:
        state_data = self._history.setdefault(
            track_id,
            {
                "state": TemporalState.UNKNOWN,
                "consecutive_frames": 0,
                "cooldown": 0,
                "evidence_frames": 0,
            },
        )

        if state_data["cooldown"] > 0:
            state_data["cooldown"] -= 1
            if state_data["cooldown"] > 0:
                state_data["state"] = TemporalState.COOLDOWN
                return TemporalDecision(
                    track_id=track_id,
                    state=state_data["state"],
                    triggered=False,
                    confidence=confidence,
                    evidence_frames=state_data["evidence_frames"],
                    metadata={
                        "consecutive_frames": state_data["consecutive_frames"],
                        "cooldown": state_data["cooldown"],
                    },
                )

            state_data["state"] = TemporalState.UNKNOWN
            state_data["consecutive_frames"] = 0
            state_data["evidence_frames"] = 0

        strong_evidence = smoking_evidence and confidence >= self.confidence_threshold

        if strong_evidence:
            state_data["consecutive_frames"] += 1
            state_data["evidence_frames"] += 1
        else:
            state_data["consecutive_frames"] = 0
            state_data["evidence_frames"] = 0
            state_data["state"] = TemporalState.UNKNOWN

        if strong_evidence and state_data["consecutive_frames"] >= self.min_evidence_frames:
            state_data["state"] = TemporalState.POSSIBLE_SMOKING

        triggered = False
        if strong_evidence and state_data["consecutive_frames"] >= self.threshold:
            state_data["state"] = TemporalState.SMOKING
            state_data["cooldown"] = self.cooldown_frames
            triggered = True
            self.logger.info("Smoking alert triggered for track_id=%s", track_id)

        decision = TemporalDecision(
            track_id=track_id,
            state=state_data["state"],
            triggered=triggered,
            confidence=confidence,
            evidence_frames=state_data["evidence_frames"],
            metadata={
                "consecutive_frames": state_data["consecutive_frames"],
                "cooldown": state_data["cooldown"],
            },
        )

        return decision
