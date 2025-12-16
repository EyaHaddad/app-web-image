from functools import lru_cache
from ..domain.interfaces import IImageProcessor
from ..infrastructure.image_processor import ImageProcessor

@lru_cache()
def get_image_processor() -> IImageProcessor:
    """Dependency provider for ImageProcessor"""
    return ImageProcessor()
