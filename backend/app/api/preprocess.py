from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import io
import time
from typing import Optional
from fastapi import APIRouter
from ..core.image_utils import (preprocess_image,
    get_histogram_data,
    segment_channels,
    detect_faces)



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
    gamma: str = Form("", description="Gamma correction")
):
    """
    Process an image with various transformations.
    
    This endpoint accepts an image file and applies selected preprocessing operations.
    Returns the processed image as a PNG file.
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
        
        # Prepare parameters
        params = {}
        
        # Boolean parameters
        bool_params = ['grayscale', 'equalize', 'normalize']
        for param in bool_params:
            if locals()[param].lower() == 'true':
                params[param] = True
        
        # Resize
        if resize_width != "0" or resize_height != "0":
            params['resize'] = (
                int(resize_width) if resize_width != "0" else None,
                int(resize_height) if resize_height != "0" else None
            )
        
        # Threshold
        if threshold and threshold != "":
            params['threshold'] = int(threshold)
            params['threshold_type'] = threshold_type
        
        # Blur
        if blur_type and blur_type != "":
            params['blur_type'] = blur_type
            params['blur_kernel'] = int(blur_kernel)
        
        # Edge detection
        if edge_detection and edge_detection != "":
            params['edge_detection'] = edge_detection
        
        # Transformations
        if rotate_angle and rotate_angle != "":
            params['rotate_angle'] = float(rotate_angle)
        
        if flip and flip != "":
            params['flip'] = flip
        
        # Adjustments
        float_params = ['brightness', 'contrast', 'saturation', 'sharpness', 'gamma']
        for param in float_params:
            value = locals()[param]
            if value and value != "":
                try:
                    params[param] = float(value)
                except ValueError:
                    pass
        
        # Process image
        start_time = time.time()
        result_image = preprocess_image(contents, **params)
        processing_time = time.time() - start_time
        
        # Convert to bytes
        buf = io.BytesIO()
        result_image.save(buf, format="PNG", optimize=True)
        buf.seek(0)
        
        return StreamingResponse(
            buf,
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
    channel: str = Form("all", description="Channel to analyze (all, red, green, blue, gray)")
):
    """
    Calculate and return histogram data for an image.
    """
    try:
        contents = await file.read()
        histogram_data = get_histogram_data(contents, channel)
        return JSONResponse(histogram_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Histogram error: {str(e)}")

@router.post("/segment")
async def segment_endpoint(
    file: UploadFile = File(..., description="Image file")
):
    """
    Separate RGB channels of an image.
    """
    try:
        contents = await file.read()
        channels = segment_channels(contents)
        return JSONResponse(channels)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Segmentation error: {str(e)}")

@router.post("/detect_faces")
async def detect_faces_endpoint(
    file: UploadFile = File(..., description="Image file")
):
    """
    Detect faces in an image and return image with bounding boxes.
    """
    try:
        contents = await file.read()
        result_image = detect_faces(contents)
        
        buf = io.BytesIO()
        result_image.save(buf, format="PNG")
        buf.seek(0)
        
        return StreamingResponse(
            buf,
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