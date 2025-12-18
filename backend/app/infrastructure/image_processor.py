from PIL import Image, ImageOps, ImageEnhance
import io
import cv2
import numpy as np
from typing import Optional, Tuple, Dict, List
import base64
import matplotlib
matplotlib.use('Agg')  # Backend non-interactif
import matplotlib.pyplot as plt
import seaborn as sns
from ..domain.interfaces import IImageProcessor
from ..domain.models import ImageProcessingParams, HistogramData, SegmentationResult, HistogramStats

class ImageProcessor(IImageProcessor):
    """Implementation of IImageProcessor using PIL and OpenCV"""

    def process_image(self, image_bytes: bytes, params: ImageProcessingParams) -> bytes:
        try:
            # Load image
            img = Image.open(io.BytesIO(image_bytes))
            
            # Convert to standard format if needed
            if img.mode not in ['RGB', 'L', 'RGBA']:
                img = img.convert('RGB')
            
            # Apply basic adjustments first
            if params.brightness is not None and params.brightness != 0:
                enhancer = ImageEnhance.Brightness(img)
                factor = 1 + (params.brightness / 100) if params.brightness != 0 else 1.0
                img = enhancer.enhance(max(0.1, min(3.0, factor)))
            
            if params.contrast is not None and params.contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(max(0.1, min(3.0, params.contrast)))
            
            if params.saturation is not None and params.saturation != 1.0:
                if img.mode != 'RGB' and img.mode != 'RGBA':
                    img = img.convert('RGB')
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(max(0.0, min(3.0, params.saturation)))
            
            if params.sharpness is not None and params.sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(max(0.0, min(3.0, params.sharpness)))
            
            # Apply gamma correction
            if params.gamma is not None and params.gamma != 1.0:
                img = self._apply_gamma_correction(img, params.gamma)
            
            # Convert to grayscale if requested
            if params.grayscale:
                if img.mode != 'L':
                    img = ImageOps.grayscale(img)
            
            # Resize if requested
            if params.resize_width or params.resize_height:
                original_width, original_height = img.size
                new_width = params.resize_width
                new_height = params.resize_height
                
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
            cv_img = self._pil_to_cv2(img)
            
            # Apply geometric transformations
            if params.rotate_angle is not None and params.rotate_angle != 0:
                height, width = cv_img.shape[:2]
                center = (width // 2, height // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, params.rotate_angle, 1.0)
                cv_img = cv2.warpAffine(
                    cv_img, rotation_matrix, (width, height),
                    borderMode=cv2.BORDER_CONSTANT,
                    borderValue=(255, 255, 255)
                )
            
            if params.flip:
                flip_code = {
                    "horizontal": 1,
                    "vertical": 0,
                    "both": -1
                }.get(params.flip)
                if flip_code is not None:
                    cv_img = cv2.flip(cv_img, flip_code)
            
            # Apply blur filters
            if params.blur_type:
                kernel_size = max(3, params.blur_kernel if params.blur_kernel % 2 == 1 else params.blur_kernel + 1)
                
                if params.blur_type == "gaussian":
                    cv_img = cv2.GaussianBlur(cv_img, (kernel_size, kernel_size), 0)
                elif params.blur_type == "median":
                    cv_img = cv2.medianBlur(cv_img, kernel_size)
                elif params.blur_type == "bilateral":
                    cv_img = cv2.bilateralFilter(cv_img, kernel_size, 75, 75)
            
            # Apply histogram equalization
            if params.equalize:
                if len(cv_img.shape) == 2:  # Grayscale
                    cv_img = cv2.equalizeHist(cv_img)
                else:  # Color - equalize Y channel in YUV
                    yuv = cv2.cvtColor(cv_img, cv2.COLOR_BGR2YUV)
                    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
                    cv_img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
            
            # Apply histogram stretching
            if params.stretch:
                if len(cv_img.shape) == 2:  # Grayscale
                    p2, p98 = np.percentile(cv_img, (2, 98))
                    cv_img = np.clip((cv_img - p2) / (p98 - p2) * 255, 0, 255).astype(np.uint8)
                else:  # Color - stretch each channel
                    for i in range(3):
                        p2, p98 = np.percentile(cv_img[:,:,i], (2, 98))
                        if p98 > p2:
                            cv_img[:,:,i] = np.clip((cv_img[:,:,i] - p2) / (p98 - p2) * 255, 0, 255).astype(np.uint8)
            
            # Apply thresholding
            if params.threshold is not None:
                # Convert to grayscale if needed
                if len(cv_img.shape) == 3:
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                
                if params.threshold_type == "binary":
                    _, cv_img = cv2.threshold(cv_img, params.threshold, 255, cv2.THRESH_BINARY)
                elif params.threshold_type == "binary_inv":
                    _, cv_img = cv2.threshold(cv_img, params.threshold, 255, cv2.THRESH_BINARY_INV)
                elif params.threshold_type == "adaptive_mean":
                    cv_img = cv2.adaptiveThreshold(
                        cv_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                        cv2.THRESH_BINARY, 11, 2
                    )
                elif params.threshold_type == "adaptive_gaussian":
                    cv_img = cv2.adaptiveThreshold(
                        cv_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                        cv2.THRESH_BINARY, 11, 2
                    )
                elif params.threshold_type == "otsu":
                    _, cv_img = cv2.threshold(cv_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Apply edge detection
            if params.edge_detection:
                # Convert to grayscale if needed
                if len(cv_img.shape) == 3:
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                
                if params.edge_detection == "canny":
                    cv_img = cv2.Canny(cv_img, 50, 150)
                elif params.edge_detection == "sobel":
                    sobel_x = cv2.Sobel(cv_img, cv2.CV_64F, 1, 0, ksize=3)
                    sobel_y = cv2.Sobel(cv_img, cv2.CV_64F, 0, 1, ksize=3)
                    cv_img = np.sqrt(sobel_x**2 + sobel_y**2).astype(np.uint8)
                elif params.edge_detection == "laplacian":
                    cv_img = cv2.Laplacian(cv_img, cv2.CV_64F)
                    cv_img = np.absolute(cv_img).astype(np.uint8)
                elif params.edge_detection == "sobel_x":
                    cv_img = cv2.Sobel(cv_img, cv2.CV_64F, 1, 0, ksize=3)
                    cv_img = np.absolute(cv_img).astype(np.uint8)
                elif params.edge_detection == "sobel_y":
                    cv_img = cv2.Sobel(cv_img, cv2.CV_64F, 0, 1, ksize=3)
                    cv_img = np.absolute(cv_img).astype(np.uint8)
            
            # Apply normalization
            if params.normalize:
                cv_img = cv2.normalize(cv_img, None, 0, 255, cv2.NORM_MINMAX)
            
            # Convert back to PIL
            result_img = self._cv2_to_pil(cv_img)
            
            # Return bytes
            buf = io.BytesIO()
            result_img.save(buf, format="PNG", optimize=True)
            buf.seek(0)
            return buf.getvalue()
        
        except Exception as e:
            raise RuntimeError(f"Image processing failed: {str(e)}")

    def get_histogram(self, image_bytes: bytes, channel: str) -> HistogramData:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            cv_img = self._pil_to_cv2(img)
            
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
            
            # Create HistogramData object
            data = HistogramData()
            for channel_name, hist_values in histograms.items():
                hist_array = np.array(hist_values)
                stats = HistogramStats(
                    mean=float(hist_array.mean()),
                    std=float(hist_array.std()),
                    min=int(hist_array.min()),
                    max=int(hist_array.max())
                )
                if channel_name == "gray":
                    data.gray = hist_values
                    data.gray_stats = stats
                elif channel_name == "red":
                    data.red = hist_values
                    data.red_stats = stats
                elif channel_name == "green":
                    data.green = hist_values
                    data.green_stats = stats
                elif channel_name == "blue":
                    data.blue = hist_values
                    data.blue_stats = stats
            
            return data
        
        except Exception as e:
            raise RuntimeError(f"Histogram calculation failed: {str(e)}")
    
    def generate_histogram_image(self, image_bytes: bytes, channel: str) -> bytes:
        """Generate a histogram visualization as a PNG image using matplotlib and seaborn"""
        try:
            img = Image.open(io.BytesIO(image_bytes))
            cv_img = self._pil_to_cv2(img)
            
            # Set seaborn style for better aesthetics
            sns.set_style("whitegrid")
            sns.set_palette("husl")
            
            # Create figure with better size and DPI
            fig, ax = plt.subplots(figsize=(12, 7), dpi=120)
            
            # Process and draw histogram based on channel
            if channel == "gray" or len(cv_img.shape) == 2:
                if len(cv_img.shape) == 3:
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                hist = cv2.calcHist([cv_img], [0], None, [256], [0, 256])
                hist = hist.flatten()
                
                # Limiter l'axe Y au 98ème percentile pour éviter les pics excessifs
                y_max = np.percentile(hist[hist > 0], 98) * 1.15
                
                # Dessiner l'histogramme
                ax.fill_between(range(256), hist, alpha=0.7, color='gray', edgecolor='black', linewidth=1.5)
                ax.set_ylim(0, y_max)
                title = f"Histogramme - Niveaux de gris"
                
                # Calculer les statistiques
                mean_val = np.mean(cv_img)
                std_val = np.std(cv_img)
                min_val = np.min(cv_img)
                max_val = np.max(cv_img)
            
            elif channel == "all":
                colors = ['blue', 'green', 'red']
                color_labels = ['Bleu', 'Vert', 'Rouge']
                all_hist = []
                
                for channel_idx, (color, label) in enumerate(zip(colors, color_labels)):
                    hist = cv2.calcHist([cv_img], [channel_idx], None, [256], [0, 256])
                    hist = hist.flatten()
                    all_hist.extend(hist)
                    ax.plot(range(256), hist, color=color, label=label, linewidth=2, alpha=0.8)
                    ax.fill_between(range(256), hist, alpha=0.2, color=color)
                
                # Limiter l'axe Y
                y_max = np.percentile([h for h in all_hist if h > 0], 98) * 1.15
                ax.set_ylim(0, y_max)
                ax.legend(loc='upper right', framealpha=0.9, fontsize=11)
                title = f"Histogramme - RGB"
                
                mean_val = np.mean(cv_img)
                std_val = np.std(cv_img)
                min_val = np.min(cv_img)
                max_val = np.max(cv_img)
            
            else:
                color_map_idx = {"blue": 0, "green": 1, "red": 2}
                color_map_color = {"blue": 'blue', "green": 'green', "red": 'red'}
                color_map_label = {"blue": 'Bleu', "green": 'Vert', "red": 'Rouge'}
                
                if channel in color_map_idx:
                    hist = cv2.calcHist([cv_img], [color_map_idx[channel]], None, [256], [0, 256])
                    hist = hist.flatten()
                    
                    # Limiter l'axe Y
                    y_max = np.percentile(hist[hist > 0], 98) * 1.15
                    
                    ax.fill_between(range(256), hist, alpha=0.6, color=color_map_color[channel], 
                                   edgecolor=color_map_color[channel], linewidth=2)
                    ax.set_ylim(0, y_max)
                    title = f"Histogramme - Canal {color_map_label[channel]}"
                    
                    # Statistiques du canal
                    channel_data = cv_img[:, :, color_map_idx[channel]]
                    mean_val = np.mean(channel_data)
                    std_val = np.std(channel_data)
                    min_val = np.min(channel_data)
                    max_val = np.max(channel_data)
            
            # Configuration des axes et du graphique
            ax.set_xlabel('Valeur de pixel (0-255)', fontsize=13, fontweight='bold')
            ax.set_ylabel('Fréquence', fontsize=13, fontweight='bold')
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlim(0, 255)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Ajouter une boîte de statistiques
            stats_text = f'Statistiques:\n'
            stats_text += f'Moyenne: {mean_val:.1f}\n'
            stats_text += f'Écart-type: {std_val:.1f}\n'
            stats_text += f'Min: {int(min_val)}\n'
            stats_text += f'Max: {int(max_val)}'
            
            ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
                   fontsize=10, verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black', linewidth=1.5))
            
            plt.tight_layout()
            
            # Sauvegarder en bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='white', edgecolor='none')
            buf.seek(0)
            result = buf.getvalue()
            plt.close(fig)
            
            return result
        
        except Exception as e:
            raise RuntimeError(f"Histogram image generation failed: {str(e)}")

    def generate_histogram_image_old(self, image_bytes: bytes, channel: str) -> bytes:
        """Old OpenCV-based histogram generation (kept for reference)"""
        try:
            img = Image.open(io.BytesIO(image_bytes))
            cv_img = self._pil_to_cv2(img)
            
            # Create a larger figure for better visualization (800x600)
            fig_height, fig_width = 600, 900
            fig = np.ones((fig_height, fig_width, 3), dtype=np.uint8) * 255
            
            # Define plot area
            plot_left = 80
            plot_right = 850
            plot_top = 50
            plot_bottom = 500
            plot_width = plot_right - plot_left
            plot_height = plot_bottom - plot_top
            
            # Draw plot background with light grid
            cv2.rectangle(fig, (plot_left, plot_top), (plot_right, plot_bottom), (240, 240, 240), -1)
            
            # Draw grid lines
            for i in range(0, 256, 16):
                x = plot_left + int((i / 256) * plot_width)
                cv2.line(fig, (x, plot_top), (x, plot_bottom), (200, 200, 200), 1)
            
            for i in range(0, plot_height, 50):
                cv2.line(fig, (plot_left, plot_top + i), (plot_right, plot_top + i), (200, 200, 200), 1)
            
            # Draw axes
            cv2.line(fig, (plot_left, plot_bottom), (plot_right, plot_bottom), (0, 0, 0), 2)  # X axis
            cv2.line(fig, (plot_left, plot_top), (plot_left, plot_bottom), (0, 0, 0), 2)  # Y axis
            
            # Process and draw histogram based on channel
            if channel == "gray" or len(cv_img.shape) == 2:
                if len(cv_img.shape) == 3:
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                hist = cv2.calcHist([cv_img], [0], None, [256], [0, 256])
                hist = cv2.normalize(hist, hist).flatten() * plot_height
                
                # Draw histogram bars with filled area
                for i in range(256):
                    x = plot_left + int((i / 256) * plot_width)
                    y = plot_bottom - int(hist[i])
                    cv2.line(fig, (x, plot_bottom), (x, y), (80, 80, 80), 2)
            
            elif channel == "all":
                colors_bgr = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # BGR format
                
                for channel_idx, color_bgr in enumerate(colors_bgr):
                    hist = cv2.calcHist([cv_img], [channel_idx], None, [256], [0, 256])
                    hist = cv2.normalize(hist, hist).flatten() * plot_height
                    
                    for i in range(256):
                        x = plot_left + int((i / 256) * plot_width)
                        y = plot_bottom - int(hist[i])
                        cv2.line(fig, (x, plot_bottom), (x, y), color_bgr, 1)
            
            else:
                color_map = {"blue": 0, "green": 1, "red": 2}
                color_bgr_map = {"blue": (255, 0, 0), "green": (0, 255, 0), "red": (0, 0, 255)}
                
                if channel in color_map:
                    hist = cv2.calcHist([cv_img], [color_map[channel]], None, [256], [0, 256])
                    hist = cv2.normalize(hist, hist).flatten() * plot_height
                    color_bgr = color_bgr_map[channel]
                    
                    for i in range(256):
                        x = plot_left + int((i / 256) * plot_width)
                        y = plot_bottom - int(hist[i])
                        cv2.line(fig, (x, plot_bottom), (x, y), color_bgr, 2)
            
            # Add axis labels
            cv2.putText(fig, "0", (plot_left - 15, plot_bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            cv2.putText(fig, "256", (plot_right - 25, plot_bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            cv2.putText(fig, "Pixel Values", (plot_left + plot_width // 2 - 60, fig_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(fig, "Frequency", (10, plot_top + plot_height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            
            # Add title
            title = f"Histogram - {channel.upper()}"
            cv2.putText(fig, title, (plot_left + 10, plot_top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
            
            # Add statistics box
            stats_x, stats_y = plot_right + 20, plot_top + 50
            
            # Calculate statistics for the displayed channel
            if channel == "gray" or len(cv_img.shape) == 2:
                if len(cv_img.shape) == 3:
                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                mean_val = np.mean(cv_img)
                std_val = np.std(cv_img)
                min_val = np.min(cv_img)
                max_val = np.max(cv_img)
            else:
                color_map = {"blue": 0, "green": 1, "red": 2}
                if channel in color_map:
                    channel_data = cv_img[:, :, color_map[channel]]
                    mean_val = np.mean(channel_data)
                    std_val = np.std(channel_data)
                    min_val = np.min(channel_data)
                    max_val = np.max(channel_data)
                else:
                    mean_val = std_val = min_val = max_val = 0
            
            # Draw stats box background
            cv2.rectangle(fig, (stats_x - 5, stats_y - 5), (stats_x + 40, stats_y + 100), (245, 245, 245), -1)
            cv2.rectangle(fig, (stats_x - 5, stats_y - 5), (stats_x + 40, stats_y + 100), (100, 100, 100), 1)
            
            # Draw stats text
            cv2.putText(fig, "Stats:", (stats_x, stats_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            cv2.putText(fig, f"Mean: {mean_val:.1f}", (stats_x, stats_y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            cv2.putText(fig, f"Std: {std_val:.1f}", (stats_x, stats_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            cv2.putText(fig, f"Min: {int(min_val)}", (stats_x, stats_y + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            cv2.putText(fig, f"Max: {int(max_val)}", (stats_x, stats_y + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
            
            # Convert to PNG bytes
            _, buffer = cv2.imencode('.png', fig)
            return buffer.tobytes()
        
        except Exception as e:
            raise RuntimeError(f"Histogram image generation failed: {str(e)}")

    def segment_image(self, image_bytes: bytes) -> SegmentationResult:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            cv_img = self._pil_to_cv2(img)
            
            if len(cv_img.shape) == 2:
                # Grayscale image
                _, buffer = cv2.imencode('.png', cv_img)
                encoded = base64.b64encode(buffer).decode('utf-8')
                return SegmentationResult(
                    red=encoded, green=encoded, blue=encoded,
                    grayscale_red=encoded, grayscale_green=encoded, grayscale_blue=encoded,
                    gray=encoded
                )
            
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
            
            return SegmentationResult(
                red=encode_image(red_colored),
                green=encode_image(green_colored),
                blue=encode_image(blue_colored),
                grayscale_red=encode_image(red_channel),
                grayscale_green=encode_image(green_channel),
                grayscale_blue=encode_image(blue_channel)
            )
        
        except Exception as e:
            raise RuntimeError(f"Channel segmentation failed: {str(e)}")

    def detect_faces(self, image_bytes: bytes) -> bytes:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            cv_img = self._pil_to_cv2(img)
            
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
            result_img = self._cv2_to_pil(cv_img)
            
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            buf.seek(0)
            return buf.getvalue()
        
        except Exception as e:
            raise RuntimeError(f"Face detection failed: {str(e)}")

    # Helper methods
    def _pil_to_cv2(self, pil_img: Image.Image) -> np.ndarray:
        if pil_img.mode == 'L':
            return np.array(pil_img)
        elif pil_img.mode == 'RGB':
            return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        elif pil_img.mode == 'RGBA':
            rgb_img = pil_img.convert('RGB')
            return cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)
        else:
            rgb_img = pil_img.convert('RGB')
            return cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2BGR)

    def _cv2_to_pil(self, cv2_img: np.ndarray) -> Image.Image:
        if len(cv2_img.shape) == 2:
            return Image.fromarray(cv2_img, mode='L')
        elif cv2_img.shape[2] == 3:
            return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
        elif cv2_img.shape[2] == 4:
            return Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGRA2RGBA))
        else:
            rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb_img)

    def _apply_gamma_correction(self, image: Image.Image, gamma: float) -> Image.Image:
        img_array = np.array(image, dtype=np.float32) / 255.0
        img_array = np.power(img_array, gamma)
        img_array = np.uint8(img_array * 255)
        return Image.fromarray(img_array)

    def crop_image(self, image_bytes: bytes, x: int, y: int, width: int, height: int) -> bytes:
        """
        Crop an image to the specified region.
        
        Args:
            image_bytes: Original image bytes
            x: Left coordinate (pixels)
            y: Top coordinate (pixels)
            width: Width of the crop region
            height: Height of the crop region
            
        Returns:
            Cropped image bytes
        """
        try:
            img = Image.open(io.BytesIO(image_bytes))
            
            # Ensure coordinates and dimensions are positive integers
            x = max(0, int(x))
            y = max(0, int(y))
            width = max(1, int(width))
            height = max(1, int(height))
            
            # Get image dimensions
            img_width, img_height = img.size
            
            # Validate crop region is within image bounds
            if x >= img_width or y >= img_height:
                raise ValueError("Crop region is outside image bounds")
            
            # Adjust crop region to fit within image
            x2 = min(x + width, img_width)
            y2 = min(y + height, img_height)
            
            # Ensure minimum size
            if x2 <= x or y2 <= y:
                raise ValueError("Crop region has invalid dimensions")
            
            # Crop the image (PIL uses (left, top, right, bottom))
            cropped = img.crop((x, y, x2, y2))
            
            # Convert to bytes
            buf = io.BytesIO()
            cropped.save(buf, format="PNG")
            buf.seek(0)
            return buf.getvalue()
            
        except Exception as e:
            raise RuntimeError(f"Crop operation failed: {str(e)}")
