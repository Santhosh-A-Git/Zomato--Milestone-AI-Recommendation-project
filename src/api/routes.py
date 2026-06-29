from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from src.models.schemas import UserPreferences, RecommendationResponse
from src.filters.restaurant_filter import get_available_locations, get_available_cuisines

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/locations", response_model=List[str])
async def get_locations():
    """Get a list of all available locations for the frontend dropdown."""
    try:
        from src.api.main import app
        engine = app.state.engine
        if not engine or engine.dataset.empty:
            return []
        locations = get_available_locations(engine.dataset)
        return locations
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/cuisines", response_model=List[str])
async def get_cuisines():
    """Get a list of all available cuisines for the frontend dropdown."""
    try:
        from src.api.main import app
        engine = app.state.engine
        if not engine or engine.dataset.empty:
            return []
        cuisines = get_available_cuisines(engine.dataset)
        return cuisines
    except Exception as e:
        logger.error(f"Error fetching cuisines: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(prefs: UserPreferences):
    """
    Get top restaurant recommendations based on user preferences.
    """
    try:
        from src.api.main import app
        engine = app.state.engine
        if not engine:
            raise HTTPException(status_code=503, detail="Engine not ready")
        
        # Get recommendations synchronously
        response = engine.get_recommendations(prefs)
        return response
    except ValueError as e:
        logger.error(f"Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while generating recommendations.")
