from PIL import Image, ImageOps
import io


def preprocess_image(image_bytes: bytes, grayscale=False, resize=(None, None), equalize=False):
    img = Image.open(io.BytesIO(image_bytes))
    # Convert or keep
    if grayscale:
        img = ImageOps.grayscale(img)
    else:
        img = img.convert("RGB")

    # Resize if requested
    if resize and (resize[0] or resize[1]):
        w, h = img.size
        rw, rh = resize
        if rw and rw > 0 and (not rh or rh == 0):
            new_w = rw
            new_h = int(h * (rw / w))
        elif rh and rh > 0 and (not rw or rw == 0):
            new_h = rh
            new_w = int(w * (rh / h))
        else:
            new_w = rw or w
            new_h = rh or h
        img = img.resize((max(1, int(new_w)), max(1, int(new_h))))

    # Histogram equalization
    if equalize:
        try:
            img = ImageOps.equalize(img)
        except Exception:
            pass

    return img
