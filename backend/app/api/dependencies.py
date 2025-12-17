from functools import lru_cache
from backend.app.domain.interfaces import IImageProcessor
from backend.app.infrastructure.image_processor import ImageProcessor

@lru_cache()
def get_image_processor() -> IImageProcessor:
    """Dependency provider for ImageProcessor"""
    return ImageProcessor()
