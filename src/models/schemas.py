from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from .enums import BudgetLevel

class UserPreferences(BaseModel):
    location: str
    budget: BudgetLevel = BudgetLevel.MEDIUM
    cuisine: Optional[str] = None
    min_rating: float = Field(3.5, ge=0.0, le=5.0)
    additional_preferences: Optional[str] = Field(None, max_length=500)

    @field_validator('location')
    def location_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Location is required and cannot be empty')
        return v

    @field_validator('additional_preferences')
    def truncate_additional_preferences(cls, v):
        if v is not None and len(v) > 500:
            return v[:500]
        return v

class Restaurant(BaseModel):
    restaurant_name: str
    location: str
    cuisines: List[str]
    cost_for_two: float
    rating: float
    votes: int
    highlights: List[str]
    restaurant_type: str

class Recommendation(BaseModel):
    rank: int
    restaurant_name: str
    cuisine: str
    rating: float
    cost_for_two: float
    explanation: str
    match_score: int = Field(ge=1, le=10)

class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]
    summary: str
