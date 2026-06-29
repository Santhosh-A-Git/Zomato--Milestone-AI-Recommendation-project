import pandas as pd
from pathlib import Path
import logging
# pyrefly: ignore [missing-import]
from src.config import settings

logger = logging.getLogger(__name__)

CACHE_FILE_NAME = "zomato_dataset.parquet"

def get_cache_file_path() -> Path:
    cache_dir = settings.get_cache_dir()
    return cache_dir / CACHE_FILE_NAME

def save_to_cache(df: pd.DataFrame) -> None:
    cache_path = get_cache_file_path()
    try:
        df.to_parquet(cache_path, index=False)
        logger.info(f"Dataset successfully cached at {cache_path}")
    except Exception as e:
        logger.warning(f"Failed to write cache at {cache_path}: {e}")

def load_from_cache() -> pd.DataFrame | None:
    cache_path = get_cache_file_path()
    if not cache_path.exists():
        return None
    try:
        df = pd.read_parquet(cache_path)
        logger.info(f"Dataset loaded from cache ({len(df)} rows)")
        return df
    except Exception as e:
        logger.warning(f"Failed to read cache at {cache_path}: {e}")
        # If cache is corrupted, we should delete it
        try:
            cache_path.unlink()
        except OSError:
            pass
        return None
