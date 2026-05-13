"""
Motion detection using Farneback optical flow.
"""

from datetime import datetime

import cv2
import numpy as np

from utils.config import Config


class MotionDetector:
    """Detect motion and intrusion activity in video frames."""

    def __init__(self):
        self.prev_gray = None
        self.intrusion_zone = None
        self.flow = None
        self.motion_threshold = Config.MOTION_THRESHOLD
        self.last_intrusion_time = None

    def reset(self):
        """Reset state between stream sessions."""
        self.prev_gray = None
        self.flow = None

    def detect(self, frame):
        """
        Detect motion in a frame using optical flow.

        Args:
            frame: Input frame in BGR format.

        Returns:
            Tuple of visualized frame and motion summary.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None:
            self.prev_gray = gray.copy()
            return frame.copy(), {
                "detected": False,
                "intensity": 0.0,
                "regions": [],
            }

        self.flow = cv2.calcOpticalFlowFarneback(
            self.prev_gray,
            gray,
            None,
            0.5,
            3,
            15,
            3,
            5,
            1.2,
            0,
        )

        magnitude, angle = cv2.cartToPolar(self.flow[..., 0], self.flow[..., 1])
        magnitude = cv2.normalize(magnitude, None, 0, 1, cv2.NORM_MINMAX)

        motion_frame = self._visualize_motion(frame, magnitude, angle)
        motion_detected = bool(np.any(magnitude > self.motion_threshold))
        motion_intensity = float(np.mean(magnitude))
        motion_regions = self._extract_motion_regions(magnitude)

        self.prev_gray = gray.copy()

        return motion_frame, {
            "detected": motion_detected,
            "intensity": motion_intensity,
            "regions": motion_regions,
        }

    def _visualize_motion(self, frame, magnitude, angle):
        """Overlay motion vectors and highlighted regions on a frame."""
        height, width = frame.shape[:2]
        motion_frame = frame.copy()
        step = 15

        for y in range(0, height, step):
            for x in range(0, width, step):
                if x >= magnitude.shape[1] or y >= magnitude.shape[0]:
                    continue

                mag = magnitude[y, x]
                ang = angle[y, x]
                if mag <= self.motion_threshold:
                    continue

                dx = int(mag * np.cos(ang) * 15)
                dy = int(mag * np.sin(ang) * 15)
                cv2.arrowedLine(
                    motion_frame,
                    (x, y),
                    (x + dx, y + dy),
                    (0, 255, 0),
                    1,
                    tipLength=0.3,
                )

        motion_mask = (magnitude > self.motion_threshold * 2).astype(np.uint8) * 255
        motion_mask = cv2.dilate(
            motion_mask,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
            iterations=2,
        )
        contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(motion_frame, contours, -1, (0, 255, 255), 2)
        return motion_frame

    def _extract_motion_regions(self, magnitude):
        """Extract bounding boxes for high-motion regions."""
        motion_mask = (magnitude > self.motion_threshold).astype(np.uint8) * 255
        motion_mask = cv2.dilate(
            motion_mask,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)),
            iterations=2,
        )

        contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area <= 100:
                continue

            x, y, width, height = cv2.boundingRect(contour)
            regions.append(
                {
                    "x": int(x),
                    "y": int(y),
                    "width": int(width),
                    "height": int(height),
                    "area": int(area),
                }
            )

        return regions

    def set_intrusion_zone(self, zone):
        """Set or clear a polygon intrusion zone."""
        if not zone:
            self.intrusion_zone = None
            return

        self.intrusion_zone = np.array(zone, dtype=np.int32)

    def check_intrusion(self, detections):
        """
        Check whether tracked people are inside the intrusion zone.

        Args:
            detections: List of detection dictionaries.

        Returns:
            Intrusion summary including alert cooldown status.
        """
        if self.intrusion_zone is None or not detections:
            return {
                "detected": False,
                "objects_in_zone": [],
                "zone": self.intrusion_zone.tolist() if self.intrusion_zone is not None else None,
                "should_alert": False,
            }

        objects_in_zone = []
        for detection in detections:
            if detection.get("class_name") != "person":
                continue

            center_x = detection["x"] + (detection["width"] / 2)
            center_y = detection["y"] + (detection["height"] / 2)

            if cv2.pointPolygonTest(self.intrusion_zone, (center_x, center_y), False) >= 0:
                objects_in_zone.append(detection)

        detected = len(objects_in_zone) > 0
        should_alert = False

        if detected:
            now = datetime.utcnow()
            if (
                self.last_intrusion_time is None
                or (now - self.last_intrusion_time).total_seconds() >= Config.INTRUSION_COOLDOWN
            ):
                should_alert = True
                self.last_intrusion_time = now

        return {
            "detected": detected,
            "objects_in_zone": objects_in_zone,
            "zone": self.intrusion_zone.tolist(),
            "should_alert": should_alert,
        }
