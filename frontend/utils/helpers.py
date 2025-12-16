import io
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def image_to_bytes(image: Image.Image, format: str = 'PNG') -> bytes:
    """Convertit une image PIL en bytes avec format spécifique"""
    buf = io.BytesIO()
    image.save(buf, format=format, optimize=True)
    buf.seek(0)
    return buf.getvalue()

def create_split_view(original_img, processed_img, show_labels=True):
    """Crée une vue divisée pour comparer avant/après"""
    
    # Créer une image composite
    width1, height1 = original_img.size
    width2, height2 = processed_img.size
    
    # Redimensionner pour avoir la même hauteur
    max_height = max(height1, height2)
    scale1 = max_height / height1
    scale2 = max_height / height2
    
    new_width1 = int(width1 * scale1)
    new_width2 = int(width2 * scale2)
    
    original_resized = original_img.resize((new_width1, max_height), Image.LANCZOS)
    processed_resized = processed_img.resize((new_width2, max_height), Image.LANCZOS)
    
    # Créer l'image composite
    total_width = new_width1 + new_width2 + 10  # +10 pour l'espace
    composite = Image.new('RGB', (total_width, max_height), (240, 240, 240))
    
    composite.paste(original_resized, (0, 0))
    composite.paste(processed_resized, (new_width1 + 10, 0))
    
    # Ajouter des labels
    if show_labels:
        draw = ImageDraw.Draw(composite)
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), "AVANT", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0), font=font)
        draw.text((new_width1 + 20, 10), "APRÈS", fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0), font=font)
    
    return composite
