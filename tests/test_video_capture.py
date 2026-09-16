from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from src.video_capture import VideoCapture


def _create_test_video(path: Path) -> None:
    writer = cv2.VideoWriter(
        str(path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        10,
        (64, 64),
    )
    assert writer.isOpened()

    for i in range(5):
        frame = np.full((64, 64, 3), 30 + i * 10, dtype=np.uint8)
        cv2.putText(
            frame,
            f"frame {i}",
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
        writer.write(frame)

    writer.release()


def test_video_capture_reads_generated_video(tmp_path: Path) -> None:
    video_path = tmp_path / "test_video.mp4"
    _create_test_video(video_path)

    capture = VideoCapture(str(video_path))
    assert capture.open() is True

    ok, frame = capture.read()
    assert ok is True
    assert frame is not None
    assert frame.shape[:2] == (64, 64)

    capture.release()


def test_video_capture_raises_for_invalid_source() -> None:
    capture = VideoCapture("this_file_does_not_exist.mp4")

    with pytest.raises(RuntimeError, match="Unable to open video source"):
        capture.open()
