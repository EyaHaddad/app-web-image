import sys
import os
from pathlib import Path

# Fix Python path to find the app module
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("🚀 Starting Image Processing API...")
    yield
    logger.info("🛑 Shutting down Image Processing API...")

# Create FastAPI app
app = FastAPI(
    title="Image Processing API",
    description="API for image preprocessing operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins - adjust for production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to import routers - with proper error handling
try:
    # Try relative import first
    from .api.preprocess import router as preprocess_router
    logger.info("✅ Successfully imported preprocess router")
except ImportError:
    try:
        # Try absolute import
        from api.preprocess import router as preprocess_router
        logger.info("✅ Successfully imported preprocess router (absolute)")
    except ImportError as e:
        logger.error(f"❌ Failed to import routers: {e}")
        # Create a simple test router for debugging
        from fastapi import APIRouter
        preprocess_router = APIRouter()
        
        @preprocess_router.get("/test")
        async def test():
            return {"message": "Test endpoint - imports failed"}
        
        @preprocess_router.post("/preprocess")
        async def dummy_preprocess():
            return {"error": "Import failed - check logs"}

# Include router
app.include_router(preprocess_router, prefix="/api", tags=["Image Processing"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🖼️ Image Processing API",
        "version": "1.0.0",
        "endpoints": {
            "preprocess": "/api/preprocess",
            "histogram": "/api/histogram",
            "segment": "/api/segment",
            "detect_faces": "/api/detect_faces",
            "test": "/api/test",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "image-processing-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )