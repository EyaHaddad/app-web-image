from PIL import Image, ImageOps, ImageEnhance
import io
import cv2
import numpy as np
from typing import Optional, Tuple, Dict
import base64

# ==================== CONVERSION FUNCTIONS ====================

def pil_to_cv2(pil_img: Image.Image) -> np.ndarray:
    """Convert PIL Image to OpenCV format"""
    if pil_img.mode == 'L':  # Grayscale
        return np.array(pil_img)
    elif pil_img.mode == 'RGB':
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    elif pil_img.mode == 'RGBA':
        rgb_img = pil_img.convert('RGB')
        return cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)
    else:
        rgb_img = pil_img.convert('RGB')
        return cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)

def cv2_to_pil(cv2_img: np.ndarray) -> Image.Image:
    """Convert OpenCV array to PIL Image"""
    if len(cv2_img.shape) == 2:  # Grayscale
        return Image.fromarray(cv2_img, mode='L')
    elif cv2_img.shape[2] == 3:  # BGR to RGB
        return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    elif cv2_img.shape[2] == 4:  # BGRA to RGBA
        return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGRA2RGBA))
    else:
        # Default to RGB
        rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_img)

# ==================== MAIN PROCESSING FUNCTION ====================

def preprocess_image(
    image_bytes: bytes,
    grayscale: bool = False,
    resize: Tuple[Optional[int], Optional[int]] = (None, None),
    equalize: bool = False,
    normalize: bool = False,
    threshold: Optional[int] = None,
    threshold_type: str = "binary",
    blur_type: Optional[str] = None,
    blur_kernel: int = 5,
    edge_detection: Optional[str] = None,
    rotate_angle: Optional[float] = None,
    flip: Optional[str] = None,
    brightness: Optional[float] = None,
    contrast: Optional[float] = None,
    saturation: Optional[float] = None,
    sharpness: Optional[float] = None,
    gamma: Optional[float] = None,
) -> Image.Image:
    """
    Main image preprocessing function with all operations.
    
    Args:
        image_bytes: Image data as bytes
        grayscale: Convert to grayscale
        resize: Tuple of (width, height) for resizing
        equalize: Apply histogram equalization
        normalize: Normalize pixel values
        threshold: Threshold value for binarization
        threshold_type: Type of thresholding
        blur_type: Type of blur filter
        blur_kernel: Size of blur kernel
        edge_detection: Edge detection method
        rotate_angle: Rotation angle in degrees
        flip: Flip direction
        brightness: Brightness adjustment (-100 to 100)
        contrast: Contrast adjustment
        saturation: Saturation adjustment
        sharpness: Sharpness adjustment
        gamma: Gamma correction value
    
    Returns:
        Processed PIL Image
    """
    try:
        # Load image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to standard format if needed
        if img.mode not in ['RGB', 'L', 'RGBA']:
            img = img.convert('RGB')
        
        # Apply basic adjustments first (these work better before conversions)
        if brightness is not None and brightness != 0:
            enhancer = ImageEnhance.Brightness(img)
            factor = 1 + (brightness / 100) if brightness != 0 else 1.0
            img = enhancer.enhance(max(0.1, min(3.0, factor)))
        
        if contrast is not None and contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(max(0.1, min(3.0, contrast)))
        
        if saturation is not None and saturation != 1.0:
            if img.mode != 'RGB' and img.mode != 'RGBA':
                img = img.convert('RGB')
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(max(0.0, min(3.0, saturation)))
        
        if sharpness is not None and sharpness != 1.0:
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(max(0.0, min(3.0, sharpness)))
        
        # Apply gamma correction
        if gamma is not None and gamma != 1.0:
            img = apply_gamma_correction(img, gamma)
        
        # Convert to grayscale if requested
        if grayscale:
            if img.mode != 'L':
                img = ImageOps.grayscale(img)
        
        # Resize if requested
        if resize and (resize[0] or resize[1]):
            original_width, original_height = img.size
            new_width, new_height = resize
            
            # Calculate new dimensions while maintaining aspect ratio if only one dimension is given
            if new_width and new_width > 0 and (not new_height or new_height == 0):
                ratio = new_width / original_width
                new_height = int(original_height * ratio)
            elif new_height and new_height > 0 and (not new_width or new_width == 0):
                ratio = new_height / original_height
                new_width = int(original_width * ratio)
            else:
                new_width = new_width or original_width
                new_height = new_height or original_height
            
            # Ensure minimum size
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to OpenCV for advanced operations
        cv_img = pil_to_cv2(img)
        
        # Apply geometric transformations
        if rotate_angle is not None and rotate_angle != 0:
            height, width = cv_img.shape[:2]
            center = (width // 2, height // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
            cv_img = cv2.warpAffine(
                cv_img, rotation_matrix, (width, height),
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(255, 255, 255)
            )
        
        if flip:
            flip_code = {
                "horizontal": 1,
                "vertical": 0,
                "both": -1
            }.get(flip)
            if flip_code is not None:
                cv_img = cv2.flip(cv_img, flip_code)
        
        # Apply blur filters
        if blur_type:
            kernel_size = max(3, blur_kernel if blur_kernel % 2 == 1 else blur_kernel + 1)
            
            if blur_type == "gaussian":
                cv_img = cv2.GaussianBlur(cv_img, (kernel_size, kernel_size), 0)
            elif blur_type == "median":
                cv_img = cv2.medianBlur(cv_img, kernel_size)
            elif blur_type == "bilateral":
                cv_img = cv2.bilateralFilter(cv_img, kernel_size, 75, 75)
        
        # Apply histogram equalization
        if equalize:
            if len(cv_img.shape) == 2:  # Grayscale
                cv_img = cv2.equalizeHist(cv_img)
            else:  # Color - equalize Y channel in YUV
                yuv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2YUV)
                yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                cv_img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        
        # Apply thresholding
        if threshold is not None:
            # Convert to grayscale if needed
            if len(cv_img.shape) == 3:
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            
            if threshold_type == "binary":
                _, cv_img = cv2.threshold(cv_img, threshold, 255, cv2.THRESH_BINARY)
            elif threshold_type == "binary_inv":
                _, cv_img = cv2.threshold(cv_img, threshold, 255, cv2.THRESH_BINARY_INV)
            elif threshold_type == "adaptive_mean":
                cv_img = cv2.adaptiveThreshold(
                    cv_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )
            elif threshold_type == "adaptive_gaussian":
                cv_img = cv2.adaptiveThreshold(
                    cv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY, 11, 2
                )
            elif threshold_type == "otsu":
                _, cv_img = cv2.threshold(cv_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply edge detection
        if edge_detection:
            # Convert to grayscale if needed
            if len(cv_img.shape) == 3:
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            
            if edge_detection == "canny":
                cv_img = cv2.Canny(cv_img, 50, 150)
            elif edge_detection == "sobel":
                sobel_x = cv2.Sobel(cv_img, cv2.CV_64F, 1, 0, ksize=3)
                sobel_y = cv2.Sobel(cv_img, cv2.CV_64F, 0, 1, ksize=3)
                cv_img = np.sqrt(sobel_x**2 + sobel_y**2).astype(np.uint8)
            elif edge_detection == "laplacian":
                cv_img = cv2.Laplacian(cv_img, cv2.CV_64F)
                cv_img = np.absolute(cv_img).astype(np.uint8)
            elif edge_detection == "sobel_x":
                cv_img = cv2.Sobel(cv_img, cv2.CV_64F, 1, 0, ksize=3)
                cv_img = np.absolute(cv_img).astype(np.uint8)
            elif edge_detection == "sobel_y":
                cv_img = cv2.Sobel(cv_img, cv2.CV_64F, 0, 1, ksize=3)
                cv_img = np.absolute(cv_img).astype(np.uint8)
        
        # Apply normalization
        if normalize:
            cv_img = cv2.normalize(cv_img, None, 0, 255, cv2.NORM_MINMAX)
        
        # Convert back to PIL
        result_img = cv2_to_pil(cv_img)
        
        return result_img
    
    except Exception as e:
        raise RuntimeError(f"Image processing failed: {str(e)}")

# ==================== HELPER FUNCTIONS ====================

def apply_gamma_correction(image: Image.Image, gamma: float) -> Image.Image:
    """Apply gamma correction to an image"""
    import numpy as np
    
    # Convert to numpy array
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # Apply gamma
    img_array = np.power(img_array, gamma)
    
    # Convert back to 8-bit
    img_array = np.uint8(img_array * 255)
    
    # Convert back to PIL Image
    return Image.fromarray(img_array)

def get_histogram_data(image_bytes: bytes, channel: str = "all") -> Dict:
    """Calculate histogram data for an image"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        cv_img = pil_to_cv2(img)
        
        histograms = {}
        
        if channel == "gray" or len(cv_img.shape) == 2:
            if len(cv_img.shape) == 3:
                cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            hist = cv2.calcHist([cv_img], [0], None, [256], [0, 256])
            histograms["gray"] = hist.flatten().tolist()
        elif channel == "all":
            colors = ['blue', 'green', 'red']
            for i, color in enumerate(colors):
                hist = cv2.calcHist([cv_img], [i], None, [256], [0, 256])
                histograms[color] = hist.flatten().tolist()
        else:
            color_map = {"blue": 0, "green": 1, "red": 2}
            if channel in color_map:
                hist = cv2.calcHist([cv_img], [color_map[channel]], None, [256], [0, 256])
                histograms[channel] = hist.flatten().tolist()
        
        # Add basic statistics
        for channel_name, hist_values in histograms.items():
            hist_array = np.array(hist_values)
            histograms[f"{channel_name}_stats"] = {
                "mean": float(hist_array.mean()),
                "std": float(hist_array.std()),
                "min": int(hist_array.min()),
                "max": int(hist_array.max())
            }
        
        return histograms
    
    except Exception as e:
        raise RuntimeError(f"Histogram calculation failed: {str(e)}")

def segment_channels(image_bytes: bytes) -> Dict:
    """Separate RGB channels of an image"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        cv_img = pil_to_cv2(img)
        
        if len(cv_img.shape) == 2:
            # Grayscale image
            _, buffer = cv2.imencode('.png', cv_img)
            return {"gray": base64.b64encode(buffer).decode('utf-8')}
        
        # Split channels
        blue_channel, green_channel, red_channel = cv2.split(cv_img)
        
        # Create zero arrays for other channels
        zeros = np.zeros_like(blue_channel)
        
        # Create colored versions of each channel
        red_colored = cv2.merge([zeros, zeros, red_channel])  # Red
        green_colored = cv2.merge([zeros, green_channel, zeros])  # Green
        blue_colored = cv2.merge([blue_channel, zeros, zeros])  # Blue
        
        def encode_image(cv_image):
            _, buffer = cv2.imencode('.png', cv_image)
            return base64.b64encode(buffer).decode('utf-8')
        
        return {
            "red": encode_image(red_colored),
            "green": encode_image(green_colored),
            "blue": encode_image(blue_colored),
            "grayscale_red": encode_image(red_channel),
            "grayscale_green": encode_image(green_channel),
            "grayscale_blue": encode_image(blue_channel)
        }
    
    except Exception as e:
        raise RuntimeError(f"Channel segmentation failed: {str(e)}")

def detect_faces(image_bytes: bytes) -> Image.Image:
    """Detect faces in an image using Haar Cascade"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        cv_img = pil_to_cv2(img)
        
        # Load face cascade classifier
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Convert back to PIL
        return cv2_to_pil(cv_img)
    
    except Exception as e:
        raise RuntimeError(f"Face detection failed: {str(e)}")

# ==================== UTILITY FUNCTIONS ====================

def validate_image_file(file_bytes: bytes, max_size_mb: int = 10) -> bool:
    """Validate image file size and type"""
    # Check size
    if len(file_bytes) > max_size_mb * 1024 * 1024:
        return False
    
    # Try to open as image
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()  # Verify it's a valid image
        return True
    except:
        return False

def get_image_metadata(image_bytes: bytes) -> Dict:
    """Get basic metadata about an image"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        return {
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "width": img.width,
            "height": img.height,
            "has_alpha": 'A' in img.mode,
            "is_animated": getattr(img, "is_animated", False),
            "n_frames": getattr(img, "n_frames", 1),
            "file_size_bytes": len(image_bytes)
        }
    except Exception as e:
        raise RuntimeError(f"Metadata extraction failed: {str(e)}")
    
