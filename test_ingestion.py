import logging
import sys
from src.data.ingestion import get_dataset

# Set up logging to see what is happening during ingestion
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stdout
)

if __name__ == "__main__":
    print("🚀 Starting data ingestion test...")
    try:
        # force_refresh=True ensures we actually download it instead of just looking for the cache
        df = get_dataset(force_refresh=True)
        print("\n✅ Dataset successfully loaded and cached!")
        print(f"📊 Total rows: {len(df)}")
        print(f"📋 Columns: {list(df.columns)}")
        print("\n🔍 Sample Data (Top 2 rows):")
        print(df.head(2))
    except Exception as e:
        print(f"\n❌ Error during ingestion: {e}")
