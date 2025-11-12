from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from ..core.image_utils import preprocess_image
import io

router = APIRouter()


@router.post("/preprocess")
async def preprocess(
    file: UploadFile = File(...),
    grayscale: bool = Form(False),
    resize_width: int = Form(0),
    resize_height: int = Form(0),
    equalize: bool = Form(False),
):
    try:
        contents = await file.read()
        resize = (resize_width or None, resize_height or None)
        img = preprocess_image(contents, grayscale=grayscale, resize=resize, equalize=equalize)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
