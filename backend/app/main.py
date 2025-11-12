from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .api.preprocess import router as preprocess_router

app = FastAPI(title="Image Preprocessing API")

app.include_router(preprocess_router, prefix="/api")


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})
