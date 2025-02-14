import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd

def plot_bus_stops(bus_stops, comunas, stops_by_comuna, comuna_max, comuna_min):
    """Generates a map displaying the distribution of bus stops per district."""
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot districts and bus stops
    comunas.plot(ax=ax, color="white", edgecolor="black", alpha=0.5)
    bus_stops.plot(ax=ax, color="red", markersize=5, alpha=0.5, label="Bus Stops")

    # Get geometries of the districts with the most and least bus stops
    max_comuna_geom = comunas[comunas["comuna"] == comuna_max["comuna"]]
    min_comuna_geom = comunas[comunas["comuna"] == comuna_min["comuna"]]

    # Highlight districts with the most and least stops
    max_comuna_geom.plot(ax=ax, edgecolor="green", linewidth=3, facecolor="none", label="Most Stops")
    min_comuna_geom.plot(ax=ax, edgecolor="blue", linewidth=3, facecolor="none", label="Least Stops")

    # Add a basemap
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

    # Add text labels for each district
    for _, row in stops_by_comuna.iterrows():
        comuna_name = row["comuna"]
        stop_count = row["cantidad_paradas"]
        
        centroid = comunas[comunas["comuna"] == comuna_name].geometry.centroid.iloc[0]
        ax.text(centroid.x, centroid.y, f"Comuna {comuna_name}\n{stop_count} stops", 
                fontsize=10, color="black", ha="center", bbox=dict(facecolor="white", alpha=0.5))

    # Labels and legend
    plt.title("Bus Stop Distribution per District in Buenos Aires")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.show()
