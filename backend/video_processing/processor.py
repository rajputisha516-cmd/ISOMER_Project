"""
Video processing with YOLOv8 segmentation.
"""

import cv2
import numpy as np
from ultralytics import YOLO

from utils.config import Config


class VideoProcessor:
    """Processes frames with YOLOv8 segmentation and object detection."""

    def __init__(self, model_name="yolov8n-seg"):
        self.model_name = model_name
        self.model = None
        self.colors = self._generate_colors(80)
        self.class_filter = None
        self.load_model()

    def load_model(self):
        """Load the YOLOv8 segmentation model."""
        try:
            self.model = YOLO(f"{self.model_name}.pt")
            name_to_id = {name: idx for idx, name in self.model.names.items()}
            self.class_filter = [
                name_to_id[name]
                for name in Config.CLASSES_TO_DETECT
                if name in name_to_id
            ] or None
            print(f"Model {self.model_name} loaded successfully")
        except Exception as exc:
            print(f"Error loading model: {exc}")
            raise

    def process_frame(self, frame):
        """
        Run inference and draw segmentation overlays and bounding boxes.

        Args:
            frame: Input BGR frame.

        Returns:
            Tuple of annotated frame and compact detection payload.
        """
        result = self.model(
            frame,
            conf=Config.MODEL_CONFIDENCE,
            iou=Config.NMS_THRESHOLD,
            imgsz=Config.INFERENCE_IMAGE_SIZE,
            classes=self.class_filter,
            max_det=Config.MAX_DETECTIONS,
            verbose=False,
        )[0]

        output_frame = frame.copy()

        if Config.DRAW_SEGMENTATION_MASKS and result.masks is not None:
            masks = result.masks.data.cpu().numpy()
            for index, mask in enumerate(masks):
                resized_mask = cv2.resize(
                    mask,
                    (output_frame.shape[1], output_frame.shape[0]),
                    interpolation=cv2.INTER_NEAREST,
                )
                binary_mask = resized_mask > 0.5
                if not np.any(binary_mask):
                    continue

                color = np.array(self.colors[index % len(self.colors)], dtype=np.uint8)
                output_frame[binary_mask] = (
                    output_frame[binary_mask] * 0.7 + color * 0.3
                ).astype(np.uint8)

        detections = []

        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_idx = int(box.cls[0])
                class_name = result.names[class_idx]
                confidence = float(box.conf[0])

                detections.append(
                    {
                        "class_name": class_name,
                        "class_id": class_idx,
                        "confidence": confidence,
                        "x": x1,
                        "y": y1,
                        "width": x2 - x1,
                        "height": y2 - y1,
                        "area": (x2 - x1) * (y2 - y1),
                    }
                )

        return self.annotate_frame(output_frame, detections), detections

    def annotate_frame(self, frame, detections):
        """Draw cached detections on top of a frame."""
        output_frame = frame.copy()

        for detection in detections:
            class_idx = detection["class_id"]
            x1 = detection["x"]
            y1 = detection["y"]
            x2 = x1 + detection["width"]
            y2 = y1 + detection["height"]
            color = self.colors[class_idx % len(self.colors)]

            cv2.rectangle(output_frame, (x1, y1), (x2, y2), color, 2)

            label = f"{detection['class_name']} {detection['confidence']:.2f}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
            cv2.rectangle(
                output_frame,
                (x1, y1 - label_size[1] - 4),
                (x1 + label_size[0], y1),
                color,
                -1,
            )
            cv2.putText(
                output_frame,
                label,
                (x1, y1 - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
            )

        return output_frame

    def _generate_colors(self, num_classes):
        """Generate distinct colors for different classes."""
        colors = []
        for index in range(num_classes):
            hue = int(180 * index / num_classes)
            saturation = 200 + (index % 3) * 20
            value = 200 + (index % 4) * 14

            hsv = np.uint8([[[hue, saturation, value]]])
            bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
            colors.append(tuple(map(int, bgr)))

        return colors

    def draw_segmentation_mask(self, frame, mask, color=(0, 255, 0), alpha=0.5):
        """Overlay a binary mask on top of a frame."""
        output = frame.copy()
        binary_mask = mask > 0
        output[binary_mask] = (
            output[binary_mask] * (1 - alpha) + np.array(color, dtype=np.uint8) * alpha
        ).astype(np.uint8)
        return output
