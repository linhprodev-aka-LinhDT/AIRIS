from __future__ import annotations

from src.temporal_analysis import TemporalAnalyzer, TemporalState


def test_temporal_state_has_progressive_transitions() -> None:
    analyzer = TemporalAnalyzer(threshold=5, cooldown_frames=2)

    for _ in range(4):
        result = analyzer.update(track_id=7, smoking_evidence=True, confidence=0.9)
        assert result.state in {TemporalState.UNKNOWN, TemporalState.POSSIBLE_SMOKING}
        assert result.triggered is False

    result = analyzer.update(track_id=7, smoking_evidence=True, confidence=0.9)
    assert result.state == TemporalState.SMOKING
    assert result.triggered is True

    next_result = analyzer.update(track_id=7, smoking_evidence=True, confidence=0.9)
    assert next_result.state == TemporalState.COOLDOWN
    assert next_result.triggered is False


def test_temporal_analysis_is_isolated_per_track() -> None:
    analyzer = TemporalAnalyzer(threshold=3, cooldown_frames=1)

    for _ in range(2):
        result = analyzer.update(track_id=1, smoking_evidence=True, confidence=0.92)
        assert result.state in {TemporalState.UNKNOWN, TemporalState.POSSIBLE_SMOKING}

    result = analyzer.update(track_id=1, smoking_evidence=True, confidence=0.92)
    assert result.state in {TemporalState.POSSIBLE_SMOKING, TemporalState.SMOKING}

    other_result = analyzer.update(track_id=2, smoking_evidence=False, confidence=0.2)
    assert other_result.state == TemporalState.UNKNOWN
