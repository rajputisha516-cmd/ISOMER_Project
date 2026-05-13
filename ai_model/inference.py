"""
YOLOv8 Segmentation Model Inference
Loads and runs the model for object detection and segmentation
"""

import cv2
import numpy as np
from ultralytics import YOLO
import os

class YOLOv8Inference:
    """YOLOv8 Segmentation Model Inference"""
    
    def __init__(self, model_name='yolov8n-seg', confidence=0.5):
        """
        Initialize YOLOv8 model
        
        Args:
            model_name: Model name (yolov8n-seg, yolov8s-seg, etc.)
            confidence: Confidence threshold for detections
        """
        self.model_name = model_name
        self.confidence = confidence
        self.model = None
        self.device = 'cuda' if cv2.cuda.getCudaEnabledDeviceCount() > 0 else 'cpu'
        
    def load_model(self):
        """Load the YOLOv8 model"""
        try:
            print(f"Loading {self.model_name} on {self.device}...")
            self.model = YOLO(f'{self.model_name}.pt')
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def infer(self, frame):
        """
        Run inference on a frame
        
        Args:
            frame: Input frame (BGR format)
        
        Returns:
            results: YOLO detection results
            annotated_frame: Frame with detections drawn
        """
        if self.model is None:
            self.load_model()
        
        # Run inference
        results = self.model(
            frame,
            conf=self.confidence,
            verbose=False,
            device=self.device
        )
        
        return results[0] if results else None
    
    def get_detections(self, result):
        """
        Extract detections from model output
        
        Args:
            result: YOLOv8 result object
        
        Returns:
            List of detections with details
        """
        detections = []
        
        if result is None or result.boxes is None:
            return detections
        
        for idx, box in enumerate(result.boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            cls_name = result.names[cls]
            
            detection = {
                'class': cls_name,
                'class_id': cls,
                'confidence': conf,
                'bbox': [x1, y1, x2, y2],
                'area': (x2 - x1) * (y2 - y1)
            }
            
            # Add mask if available
            if result.masks is not None and idx < len(result.masks):
                mask = result.masks[idx].cpu().numpy()
                detection['mask'] = mask
            
            detections.append(detection)
        
        return detections

if __name__ == '__main__':
    # Example usage
    inferencer = YOLOv8Inference('yolov8n-seg')
    inferencer.load_model()
    
    # Test with webcam
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        result = inferencer.infer(frame)
        detections = inferencer.get_detections(result)
        
        print(f"Detected {len(detections)} objects")
        
        annotated = result.plot() if result else frame
        cv2.imshow('YOLOv8 Detection', annotated)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
