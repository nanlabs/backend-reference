import os
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

# 1️⃣ Load the Shapefile (Make sure you have extracted it)

# Build the path to the shapefile
script_dir = Path(__file__).resolve().parent.parent
shapefile_path = os.path.join(script_dir, "data/countries/ne_10m_admin_0_countries.shp")

world = gpd.read_file(shapefile_path)

# 2️⃣ Display the first rows of the dataset
print(world.head())

# 3️⃣ Display the data in table form
print(world[["NAME", "POP_EST", "CONTINENT"]].head(10))  # Only the first 10 rows

# 4️⃣ Plot the basic map
fig, ax = plt.subplots(figsize=(12, 6))
world.plot(ax=ax, color="lightgray", edgecolor="black")

plt.title("World Map with Geopandas")
plt.show()

## Heatmap 

fig, ax = plt.subplots(figsize=(12, 6))
world.plot(column="POP_EST", cmap="plasma", linewidth=0.5, edgecolor="black", legend=True, ax=ax)

plt.title("World Population Heatmap")
plt.show()

# Select a country (for example, Argentina)
argentina = world[world["NAME"] == "Argentina"]

# Create a 500 km buffer around it
argentina_buffer = argentina.copy()
argentina_buffer.geometry = argentina.geometry.buffer(5)  # Depends on the projection

# Plot
fig, ax = plt.subplots(figsize=(6, 8))
world.plot(ax=ax, color="lightgray", edgecolor="black")
argentina.plot(ax=ax, color="blue", edgecolor="black")
argentina_buffer.plot(ax=ax, color="red", alpha=0.3)

plt.title("500km Buffer Around Argentina")
plt.show()


# 5️⃣ Filter countries with more than 100M inhabitants and highlight them
large_countries = world[world["POP_EST"] < 100_000_000]

fig, ax = plt.subplots(figsize=(12, 6))
world.plot(ax=ax, color="lightgray", edgecolor="black", label="Other countries")  # Background map
large_countries.plot(ax=ax, color="yellow", edgecolor="black", label="> 100M inhabitants")  # Large countries in red

# 6️⃣ Add country names to the map
for x, y, label in zip(
    large_countries.geometry.centroid.x, 
    large_countries.geometry.centroid.y, 
    large_countries.NAME
):
    ax.text(x, y, label, fontsize=9, ha="center", color="black")

# Add legend
ax.legend()

plt.title("Countries with More Than 100M Inhabitants")
plt.show()

# 7️⃣ Save the map as an image
plt.savefig("world_map.png", dpi=300)

# 8️⃣ Save the data in GeoJSON format
world.to_file("world.geojson", driver="GeoJSON")

# 9️⃣ Read the saved GeoJSON and display its data
world_geojson = gpd.read_file("world.geojson")
print(world_geojson.head())

print("✅ All done: Map displayed, data saved in 'world.geojson' and 'world_map.png'")

