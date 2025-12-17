from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse
import io
import time
from typing import Optional
from backend.app.domain.interfaces import IImageProcessor
from backend.app.domain.models import ImageProcessingParams
from backend.app.api.dependencies import get_image_processor

router = APIRouter()

@router.post("/preprocess")
async def preprocess_image_endpoint(
    file: UploadFile = File(..., description="Image file to process"),
    grayscale: str = Form("false", description="Convert to grayscale"),
    resize_width: str = Form("0", description="Resize width (0 to keep original)"),
    resize_height: str = Form("0", description="Resize height (0 to keep original)"),
    equalize: str = Form("false", description="Histogram equalization"),
    normalize: str = Form("false", description="Normalize pixel values"),
    threshold: str = Form("", description="Threshold value (0-255)"),
    threshold_type: str = Form("binary", description="Threshold type"),
    blur_type: str = Form("", description="Blur type (gaussian, median, bilateral)"),
    blur_kernel: str = Form("5", description="Blur kernel size"),
    edge_detection: str = Form("", description="Edge detection method"),
    rotate_angle: str = Form("", description="Rotation angle in degrees"),
    flip: str = Form("", description="Flip type (horizontal, vertical, both)"),
    brightness: str = Form("", description="Brightness adjustment (-100 to 100)"),
    contrast: str = Form("", description="Contrast adjustment"),
    saturation: str = Form("", description="Saturation adjustment"),
    sharpness: str = Form("", description="Sharpness adjustment"),
    gamma: str = Form("", description="Gamma correction"),
    processor: IImageProcessor = Depends(get_image_processor)
):
    """
    Process an image with various transformations.
    """
    try:
        # Read file
        contents = await file.read()
        
        # Validate file size (max 10MB)
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Build params object
        params = ImageProcessingParams()
        
        # Boolean parameters
        if grayscale.lower() == 'true': params.grayscale = True
        if equalize.lower() == 'true': params.equalize = True
        if normalize.lower() == 'true': params.normalize = True
        
        # Resize
        if resize_width != "0": params.resize_width = int(resize_width)
        if resize_height != "0": params.resize_height = int(resize_height)
        
        # Threshold
        if threshold and threshold != "":
            params.threshold = int(threshold)
            params.threshold_type = threshold_type
        
        # Blur
        if blur_type and blur_type != "":
            params.blur_type = blur_type
            params.blur_kernel = int(blur_kernel)
        
        # Edge detection
        if edge_detection and edge_detection != "":
            params.edge_detection = edge_detection
        
        # Transformations
        if rotate_angle and rotate_angle != "":
            params.rotate_angle = float(rotate_angle)
        
        if flip and flip != "":
            params.flip = flip
        
        # Adjustments
        if brightness and brightness != "": params.brightness = float(brightness)
        if contrast and contrast != "": params.contrast = float(contrast)
        if saturation and saturation != "": params.saturation = float(saturation)
        if sharpness and sharpness != "": params.sharpness = float(sharpness)
        if gamma and gamma != "": params.gamma = float(gamma)
        
        # Process image
        start_time = time.time()
        result_bytes = processor.process_image(contents, params)
        processing_time = time.time() - start_time
        
        return StreamingResponse(
            io.BytesIO(result_bytes),
            media_type="image/png",
            headers={
                "X-Processing-Time": f"{processing_time:.3f}s",
                "X-Original-Filename": file.filename,
                "Content-Disposition": f"attachment; filename=processed_{file.filename}"
            }
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@router.post("/histogram")
async def histogram_endpoint(
    file: UploadFile = File(..., description="Image file"),
    channel: str = Form("all", description="Channel to analyze (all, red, green, blue, gray)"),
    processor: IImageProcessor = Depends(get_image_processor)
):
    """
    Calculate and return histogram data for an image.
    """
    try:
        contents = await file.read()
        histogram_data = processor.get_histogram(contents, channel)
        return histogram_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Histogram error: {str(e)}")

@router.post("/segment")
async def segment_endpoint(
    file: UploadFile = File(..., description="Image file"),
    processor: IImageProcessor = Depends(get_image_processor)
):
    """
    Separate RGB channels of an image.
    """
    try:
        contents = await file.read()
        channels = processor.segment_image(contents)
        return channels
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segmentation error: {str(e)}")

@router.post("/detect_faces")
async def detect_faces_endpoint(
    file: UploadFile = File(..., description="Image file"),
    processor: IImageProcessor = Depends(get_image_processor)
):
    """
    Detect faces in an image and return image with bounding boxes.
    """
    try:
        contents = await file.read()
        result_bytes = processor.detect_faces(contents)
        
        return StreamingResponse(
            io.BytesIO(result_bytes),
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment; filename=faces_detected.png"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Face detection error: {str(e)}")

@router.post("/test")
async def test_endpoint(
    file: UploadFile = File(..., description="Test image")
):
    """
    Simple test endpoint to verify API is working.
    """
    try:
        contents = await file.read()
        
        # Just return image info without processing
        from PIL import Image
        import io
        
        img = Image.open(io.BytesIO(contents))
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
            "image_info": {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height
            },
            "message": "API is working correctly!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test error: {str(e)}")


@router.post("/crop")
async def crop_image_endpoint(
    file: UploadFile = File(..., description="Image file to crop"),
    x: str = Form("0", description="Left coordinate (pixels)"),
    y: str = Form("0", description="Top coordinate (pixels)"),
    width: str = Form("100", description="Crop width (pixels)"),
    height: str = Form("100", description="Crop height (pixels)"),
    processor: IImageProcessor = Depends(get_image_processor)
):
    """
    Crop an image to a specified rectangular region.
    
    Parameters:
    - x: Left coordinate of the crop region (pixels)
    - y: Top coordinate of the crop region (pixels)
    - width: Width of the crop region (pixels)
    - height: Height of the crop region (pixels)
    """
    try:
        # Read file
        contents = await file.read()
        
        # Validate file size (max 10MB)
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Parse parameters
        try:
            x_coord = int(x)
            y_coord = int(y)
            crop_width = int(width)
            crop_height = int(height)
        except ValueError:
            raise HTTPException(status_code=400, detail="Crop parameters must be integers")
        
        # Validate parameters
        if crop_width <= 0 or crop_height <= 0:
            raise HTTPException(status_code=400, detail="Width and height must be positive")
        
        # Perform crop
        result = processor.crop_image(contents, x_coord, y_coord, crop_width, crop_height)
        
        # Return as image
        return StreamingResponse(
            io.BytesIO(result),
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=cropped_image.png"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop failed: {str(e)}")