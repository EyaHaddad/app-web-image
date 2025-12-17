from pydantic import BaseModel, Field
from typing import Optional, Tuple, List, Dict, Any, Union

class ImageProcessingParams(BaseModel):
    """Parameters for image processing operations"""
    grayscale: bool = False
    resize_width: Optional[int] = None
    resize_height: Optional[int] = None
    equalize: bool = False
    stretch: bool = False
    normalize: bool = False
    threshold: Optional[int] = None
    threshold_type: str = "binary"
    blur_type: Optional[str] = None
    blur_kernel: int = 5
    edge_detection: Optional[str] = None
    rotate_angle: Optional[float] = None
    flip: Optional[str] = None
    brightness: Optional[float] = None
    contrast: Optional[float] = None
    saturation: Optional[float] = None
    sharpness: Optional[float] = None
    gamma: Optional[float] = None

class HistogramStats(BaseModel):
    mean: float
    std: float
    min: int
    max: int

class HistogramData(BaseModel):
    gray: Optional[List[int]] = None
    red: Optional[List[int]] = None
    green: Optional[List[int]] = None
    blue: Optional[List[int]] = None
    gray_stats: Optional[HistogramStats] = None
    red_stats: Optional[HistogramStats] = None
    green_stats: Optional[HistogramStats] = None
    blue_stats: Optional[HistogramStats] = None

class SegmentationResult(BaseModel):
    red: str
    green: str
    blue: str
    grayscale_red: str
    grayscale_green: str
    grayscale_blue: str
    gray: Optional[str] = None
