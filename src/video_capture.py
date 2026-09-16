from __future__ import annotations

import logging
from typing import Optional

import cv2
import numpy as np

from config import CONFIG


class VideoCapture:
    """Thin wrapper around OpenCV VideoCapture with project-level error handling."""

    def __init__(self, source: int | str = CONFIG.source, *, api_preference: int = cv2.CAP_ANY) -> None:
        self.source = source
        self.api_preference = api_preference
        self._capture: Optional[cv2.VideoCapture] = None
        self.logger = logging.getLogger(__name__)

    def open(self) -> bool:
        if self._capture is not None and self._capture.isOpened():
            return True

        self._capture = cv2.VideoCapture(self.source, self.api_preference)
        if not self._capture or not self._capture.isOpened():
            message = f"Unable to open video source: {self.source}"
            self.logger.error(message)
            raise RuntimeError(message)

        self.logger.info("Video source opened: %s", self.source)
        return True

    def read(self) -> tuple[bool, Optional[np.ndarray]]:
        if self._capture is None:
            self.open()

        if self._capture is None or not self._capture.isOpened():
            return False, None

        ok, frame = self._capture.read()
        if not ok or frame is None:
            return False, None

        return True, frame

    def release(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None
            self.logger.info("Video source released: %s", self.source)

    @property
    def is_open(self) -> bool:
        return self._capture is not None and self._capture.isOpened()

    def __enter__(self) -> "VideoCapture":
        self.open()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()

