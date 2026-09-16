from __future__ import annotations

from src.detector import Detection
from src.tracker import Track, Tracker


def test_tracker_assigns_unique_track_ids() -> None:
    tracker = Tracker()

    detections = [
        Detection(class_id=0, class_name="person", confidence=0.92, bbox=(10.0, 20.0, 30.0, 60.0)),
        Detection(class_id=0, class_name="person", confidence=0.93, bbox=(40.0, 25.0, 60.0, 65.0)),
    ]

    tracks = tracker.update(detections)
    assert len(tracks) == 2
    assert {track.track_id for track in tracks} == {1, 2}
    for track in tracks:
        assert track.class_name in {"person"}
        assert track.bbox
        assert 0.0 <= track.confidence <= 1.0


def test_tracker_keeps_same_id_for_same_person_across_frames() -> None:
    tracker = Tracker()

    first_frame = [Detection(class_id=0, class_name="person", confidence=0.90, bbox=(0.0, 0.0, 100.0, 200.0))]
    second_frame = [Detection(class_id=0, class_name="person", confidence=0.91, bbox=(5.0, 2.0, 105.0, 202.0))]

    first_tracks = tracker.update(first_frame)
    second_tracks = tracker.update(second_frame)

    assert len(first_tracks) == 1
    assert len(second_tracks) == 1
    assert first_tracks[0].track_id == second_tracks[0].track_id
    assert second_tracks[0].bbox != first_tracks[0].bbox
