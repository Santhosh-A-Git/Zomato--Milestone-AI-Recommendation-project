import pandas as pd
import logging
from typing import List
# pyrefly: ignore [missing-import]
from src.models.schemas import UserPreferences
# pyrefly: ignore [missing-import]
from src.models.enums import BudgetLevel
logger = logging.getLogger(__name__)

def get_available_locations(df: pd.DataFrame) -> List[str]:
    """Return a sorted list of unique available locations."""
    if df.empty or 'location' not in df.columns:
        return []
    locations = df['location'].dropna().unique()
    # Return title-cased for UI display
    return sorted([loc.title() for loc in locations])

def get_available_cuisines(df: pd.DataFrame) -> List[str]:
    """Return a sorted list of unique available cuisines."""
    if df.empty or 'cuisines' not in df.columns:
        return []
    
    unique_cuisines = set()
    for cuisines_raw in df['cuisines'].dropna():
        if isinstance(cuisines_raw, str):
            continue
        try:
            for cuisine in list(cuisines_raw):
                unique_cuisines.add(cuisine.title())
        except TypeError:
            pass
    
    return sorted(list(unique_cuisines))

def _apply_filters(
    df: pd.DataFrame, 
    location: str, 
    min_cost: float, 
    max_cost: float, 
    cuisine: str | None, 
    min_rating: float
) -> pd.DataFrame:
    """Apply strict filters to the dataframe."""
    filtered = df.copy()
    
    # 1. Location (Case insensitive)
    loc_lower = location.lower().strip()
    filtered = filtered[filtered['location'].str.lower() == loc_lower]
    
    # 2. Budget
    if min_cost > 0.0:
        filtered = filtered[filtered['cost_for_two'] >= min_cost]
    if max_cost < float('inf'):
        filtered = filtered[filtered['cost_for_two'] <= max_cost]
        
    # 3. Rating
    if min_rating > 0.0:
        filtered = filtered[filtered['rating'] >= min_rating]
        
    # 4. Cuisine (Containment check)
    if cuisine:
        cuisine_list = [c.strip().lower() for c in cuisine.split(',')]
        def match_cuisine(row_cuisines):
            if isinstance(row_cuisines, str):
                return False
            try:
                row_cuisines_lower = [c.lower() for c in list(row_cuisines)]
                return any(c in row_cuisines_lower for c in cuisine_list)
            except TypeError:
                return False
            
        filtered = filtered[filtered['cuisines'].apply(match_cuisine)]
        
    return filtered

def filter_restaurants(df: pd.DataFrame, prefs: UserPreferences) -> pd.DataFrame:
    """
    Filter restaurants based on user preferences.
    Applies progressive constraint relaxation if < 3 results are found.
    Caps results at top 20 candidates (sorted by rating and votes).
    """
    if df.empty:
        return df

    # Initial strict filtering
    filtered = _apply_filters(
        df,
        location=prefs.location,
        min_cost=prefs.budget.min_cost,
        max_cost=prefs.budget.max_cost,
        cuisine=prefs.cuisine,
        min_rating=prefs.min_rating
    )

    # Relaxation strategy if < 3 results
    if len(filtered) < 3:
        logger.warning(f"Only {len(filtered)} results found for strict criteria. Relaxing constraints...")
        
        # Step 1: Widen budget (drop budget constraint)
        logger.info("Relaxation Step 1: Dropping budget constraint")
        filtered_step1 = _apply_filters(
            df, 
            location=prefs.location, 
            min_cost=0.0, 
            max_cost=float('inf'), 
            cuisine=prefs.cuisine, 
            min_rating=prefs.min_rating
        )
        if len(filtered_step1) >= 3:
            filtered = filtered_step1
        else:
            # Step 2: Lower min_rating by 0.5 (and keep budget dropped)
            new_rating = max(0.0, prefs.min_rating - 0.5)
            logger.info(f"Relaxation Step 2: Lowering min_rating to {new_rating}")
            filtered_step2 = _apply_filters(
                df, 
                location=prefs.location, 
                min_cost=0.0, 
                max_cost=float('inf'), 
                cuisine=prefs.cuisine, 
                min_rating=new_rating
            )
            if len(filtered_step2) >= 3:
                filtered = filtered_step2
            else:
                # Step 3: Drop cuisine filter entirely
                logger.info("Relaxation Step 3: Dropping cuisine filter")
                filtered_step3 = _apply_filters(
                    df, 
                    location=prefs.location, 
                    min_cost=0.0, 
                    max_cost=float('inf'), 
                    cuisine=None, 
                    min_rating=new_rating
                )
                filtered = filtered_step3

    if len(filtered) == 0:
        logger.warning(f"No restaurants found matching location '{prefs.location}' even after relaxation.")
        return filtered
        
    # Deduplicate by restaurant name to prevent LLM from returning duplicate branches
    filtered['clean_name'] = filtered['restaurant_name'].str.lower().str.strip()
    filtered = filtered.drop_duplicates(subset=['clean_name'], keep='first')
    filtered = filtered.drop(columns=['clean_name'])
    
    # Cap at top 20 candidates, sorted by rating descending, then by votes descending
    filtered = filtered.sort_values(by=['rating', 'votes'], ascending=[False, False])
    return filtered.head(20)
