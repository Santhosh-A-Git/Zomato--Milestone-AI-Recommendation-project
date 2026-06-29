from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os

from src.engine.orchestrator import RecommendationEngine
from src.api.routes import router

logger = logging.getLogger(__name__)

# Configure root logger if not already configured
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the dataset and initialize engine globally
    logger.info("Starting up FastAPI server...")
    try:
        app.state.engine = RecommendationEngine()
        logger.info("Recommendation Engine initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Recommendation Engine: {e}")
        app.state.engine = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI server...")
    app.state.engine = None

app = FastAPI(
    title="Zomato Recommendation API",
    description="AI-Powered Restaurant Recommendation System Backend",
    version="1.0.0",
    lifespan=lifespan
)

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."}
    )

# Include API routes
app.include_router(router, prefix="/api", tags=["recommendations"])

@app.get("/api/health", tags=["system"])
async def health_check():
    """Check if the API and engine are healthy."""
    is_ready = app.state.engine is not None and not app.state.engine.dataset.empty
    return {
        "status": "ok" if is_ready else "degraded",
        "engine_loaded": is_ready
    }

# Mount the static frontend directory at the root
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    logger.warning("Frontend directory not found. Serving API only.")
