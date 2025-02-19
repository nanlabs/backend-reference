from geopandas import GeoDataFrame as gpd
from config import DISTRICTS_URL

def fetch_districts():
    """Fetches district data from Buenos Aires' open data API."""
    try:
        return gpd.read_file(DISTRICTS_URL)
    except Exception as e:
        raise ValueError(f"Failed to fetch districts data: {str(e)}")
