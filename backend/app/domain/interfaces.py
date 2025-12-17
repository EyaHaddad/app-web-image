from abc import ABC, abstractmethod
from typing import Any, Dict
from .models import ImageProcessingParams, HistogramData, SegmentationResult

class IImageProcessor(ABC):
    """Interface for image processing operations"""
    
    @abstractmethod
    def process_image(self, image_bytes: bytes, params: ImageProcessingParams) -> bytes:
        """Process an image with given parameters"""
        pass

    @abstractmethod
    def get_histogram(self, image_bytes: bytes, channel: str) -> HistogramData:
        """Get histogram data for an image"""
        pass

    @abstractmethod
    def generate_histogram_image(self, image_bytes: bytes, channel: str) -> bytes:
        """Generate a histogram visualization as a PNG image"""
        pass

    @abstractmethod
    def segment_image(self, image_bytes: bytes) -> SegmentationResult:
        """Segment image into channels"""
        pass

    @abstractmethod
    def detect_faces(self, image_bytes: bytes) -> bytes:
        """Detect faces in an image"""
        pass
