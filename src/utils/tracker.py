"""Simple object tracking for detected road signs."""

from typing import Dict, List, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
import time

if TYPE_CHECKING:
    from .types import Detection


@dataclass
class TrackedObject:
    """Represents a tracked object across frames."""
    track_id: int
    label: str
    confidence: float
    bbox: tuple  # (x1, y1, x2, y2)
    last_seen: float = field(default_factory=time.time)
    frame_count: int = 0


class SimpleTracker:
    """
    Simple tracker for road signs using IoU-based matching.
    Maintains object IDs across consecutive frames.
    """
    
    def __init__(self, iou_threshold: float = 0.3, max_age: int = 30, min_stable: int = 3):
        """
        Initialize tracker.
        
        Args:
            iou_threshold: Minimum IoU to consider a match
            max_age: Maximum frames to keep a track without updates
            min_stable: Minimum number of frames for a track to be considered stable
        """
        self.iou_threshold = iou_threshold
        self.max_age = max_age
        self.min_stable = min_stable
        self.tracks: Dict[int, TrackedObject] = {}
        self.next_id = 0
    
    def update(self, detections: List) -> List:
        """
        Update tracks with new detections.
        
        Args:
            detections: List of Detection objects
        
        Returns:
            List of Detection objects with updated track_id fields
        """
        current_time = time.time()
        
        # Remove old tracks
        self.tracks = {
            tid: track for tid, track in self.tracks.items()
            if (current_time - track.last_seen) < self.max_age
        }
        
        if not detections:
            return []
        
        # Match detections to existing tracks
        matched_tracks = set()
        updated_detections = []
        
        for detection in detections:
            bbox = detection.bbox
            label = detection.label
            confidence = detection.confidence
            
            best_match = None
            best_iou = self.iou_threshold
            
            # Find best matching track
            for tid, track in self.tracks.items():
                if tid in matched_tracks:
                    continue
                
                iou = self._calculate_iou(bbox, track.bbox)
                if iou > best_iou and track.label == label:
                    best_iou = iou
                    best_match = tid
            
            if best_match is not None:
                # Update existing track
                track = self.tracks[best_match]
                track.bbox = bbox
                track.confidence = confidence
                track.last_seen = current_time
                track.frame_count += 1
                matched_tracks.add(best_match)
                
                # Update detection with track_id
                detection.track_id = best_match
                updated_detections.append(detection)
            else:
                # Create new track
                new_track = TrackedObject(
                    track_id=self.next_id,
                    label=label,
                    confidence=confidence,
                    bbox=bbox,
                    last_seen=current_time,
                    frame_count=1
                )
                self.tracks[self.next_id] = new_track
                
                # Update detection with new track_id
                detection.track_id = self.next_id
                updated_detections.append(detection)
                self.next_id += 1
        
        return updated_detections
    
    @staticmethod
    def _calculate_iou(box1: tuple, box2: tuple) -> float:
        """Calculate Intersection over Union between two bounding boxes."""
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        # Calculate intersection area
        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)
        
        if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
            return 0.0
        
        inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
        
        # Calculate union area
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0.0
    
    def is_stable(self, track_id: int) -> bool:
        """
        Check if a track is stable (has been tracked for min_stable frames).
        
        Args:
            track_id: The track ID to check
        
        Returns:
            True if the track is stable, False otherwise
        """
        if track_id not in self.tracks:
            return False
        return self.tracks[track_id].frame_count >= self.min_stable
    
    def get_stable_tracks(self) -> List[TrackedObject]:
        """
        Get all stable tracks.
        
        Returns:
            List of TrackedObject instances that are stable
        """
        return [track for track in self.tracks.values() if track.frame_count >= self.min_stable]
    
    def reset(self):
        """Reset the tracker, clearing all tracks."""
        self.tracks.clear()
        self.next_id = 0

