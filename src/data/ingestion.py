import pandas as pd
import logging
# pyrefly: ignore [missing-import]
from src.config import settings
# pyrefly: ignore [missing-import]
from src.data.cache import load_from_cache, save_to_cache

logger = logging.getLogger(__name__)

def preprocess_dataset(df: pd.DataFrame) -> pd.DataFrame:
    if len(df) == 0:
        raise ValueError("Dataset is empty after loading")

    rename_map = {}
    
    # Pass 1: map existing columns and gather location candidates
    loc_candidates = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl in ['restaurant name', 'name', 'restaurant_name']:
            rename_map[c] = 'restaurant_name'
        elif cl in ['city', 'location', 'place name', 'locality']:
            loc_candidates[cl] = c
        elif cl in ['cuisines', 'cuisine']:
            rename_map[c] = 'cuisines'
        elif cl in ['average cost for two', 'cost', 'prices', 'approx_cost(for two people)', 'cost_for_two']:
            rename_map[c] = 'cost_for_two'
        elif cl in ['aggregate rating', 'dining rating', 'rate', 'rating']:
            rename_map[c] = 'rating'
        elif cl in ['votes', 'dining votes']:
            rename_map[c] = 'votes'
        elif cl in ['highlights', 'features']:
            rename_map[c] = 'highlights'
        elif cl in ['establishment', 'restaurant type']:
            rename_map[c] = 'restaurant_type'

    # Pass 2: assign location based on granularity priority
    if loc_candidates:
        if 'locality' in loc_candidates:
            rename_map[loc_candidates['locality']] = 'location'
        elif 'place name' in loc_candidates:
            rename_map[loc_candidates['place name']] = 'location'
        elif 'location' in loc_candidates:
            rename_map[loc_candidates['location']] = 'location'
        elif 'city' in loc_candidates:
            rename_map[loc_candidates['city']] = 'location'

    df = df.rename(columns=rename_map)

    required_cols = ['restaurant_name', 'location', 'cuisines', 'cost_for_two', 'rating', 'votes']
    missing = [c for c in required_cols if c not in df.columns]
    
    for c in missing:
        logger.warning(f"Required column '{c}' is missing from the dataset. Adding default.")
        if c in ['rating', 'cost_for_two', 'votes']:
            df[c] = 0.0
        else:
            df[c] = ""
            
    # Drop rows without restaurant name
    df = df.dropna(subset=['restaurant_name'])

    # Clean location
    df['location'] = df['location'].astype(str).str.lower().str.strip()

    # Clean rating (extract numeric part, e.g. "4.1 /5" -> 4.1)
    df['rating'] = df['rating'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

    # Clean cost (remove any non-numeric characters)
    df['cost_for_two'] = df['cost_for_two'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df['cost_for_two'] = pd.to_numeric(df['cost_for_two'], errors='coerce')
    median_cost = df['cost_for_two'].median()
    if pd.isna(median_cost):
        median_cost = 500.0
    df['cost_for_two'] = df['cost_for_two'].fillna(median_cost)

    # Clean votes
    df['votes'] = pd.to_numeric(df['votes'], errors='coerce').fillna(0).astype(int)

    # Clean cuisines into a list of strings
    df['cuisines'] = df['cuisines'].fillna("")
    df['cuisines'] = df['cuisines'].astype(str).apply(
        lambda x: [c.strip() for c in x.split(',') if c.strip() and c.strip().lower() != 'nan']
    )

    if 'highlights' in df.columns:
        df['highlights'] = df['highlights'].fillna("")
        df['highlights'] = df['highlights'].astype(str).apply(
            lambda x: [c.strip() for c in x.replace('[', '').replace(']', '').replace("'", "").split(',') if c.strip() and c.strip().lower() != 'nan']
        )
    else:
        df['highlights'] = [[] for _ in range(len(df))]

    if 'restaurant_type' not in df.columns:
        df['restaurant_type'] = "Unknown"

    final_cols = required_cols + ['highlights', 'restaurant_type']
    return df[final_cols]


def get_dataset(force_refresh: bool = False) -> pd.DataFrame:
    if not force_refresh:
        cached_df = load_from_cache()
        if cached_df is not None:
            return cached_df
            
    logger.info(f"Downloading dataset {settings.huggingface_dataset} from HuggingFace...")
    try:
        from datasets import load_dataset as hf_load_dataset
        dataset = hf_load_dataset(settings.huggingface_dataset)
        split = 'train' if 'train' in dataset else list(dataset.keys())[0]
        df = dataset[split].to_pandas()
    except Exception as e:
        logger.error(f"Failed to download dataset: {e}")
        cached_df = load_from_cache()
        if cached_df is not None:
            logger.info("Using cached dataset as fallback.")
            return cached_df
        raise RuntimeError(f"Could not load dataset from HF and no cache available: {e}")

    df_clean = preprocess_dataset(df)
    save_to_cache(df_clean)
    
    return df_clean
