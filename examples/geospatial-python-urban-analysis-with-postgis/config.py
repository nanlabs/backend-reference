from pathlib import Path

# Add the necessary imports
PROJECT_ROOT = Path(__file__).resolve().parent

POPULATION_DENSITY_RASTER = PROJECT_ROOT / "data/census/caba/census.tif"

print(POPULATION_DENSITY_RASTER)
# API URLs
BUS_STOPS_URL = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/transporte-y-obras-publicas/colectivos-paradas/paradas-de-colectivo.geojson"
DISTRICTS_URL = "https://cdn.buenosaires.gob.ar/datosabiertos/datasets/ministerio-de-educacion/comunas/comunas.geojson"
 # Standard coordinate reference system (CRS)
EPSG_TARGET = 3857 