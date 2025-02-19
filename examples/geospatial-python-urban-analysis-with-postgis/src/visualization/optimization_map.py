import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd

def plot_optimal_stops(bus_stops, optimal_stops, districts):
    """
        Plots optimal bus stop locations on a map.
        Args:
            bus_stops (GeoDataFrame): Existing bus stop locations
            optimal_stops (GeoDataFrame): Calculated optimal stop locations
            districts (GeoDataFrame): District boundaries
        Raises:
            Exception: If plotting operations fail
    """
    try:
        fig, ax = plt.subplots(figsize=(12, 12))

        # Plot districts and existing bus stops
        districts.plot(ax=ax, color="white", edgecolor="black", alpha=0.5)
        bus_stops.plot(ax=ax, color="red", markersize=5, alpha=0.5, label="Existing Bus Stops")

        # Plot optimal stops
        optimal_stops.plot(ax=ax, color="green", markersize=10, alpha=0.8, label="Optimal Stops")

        # Add basemap (CartoDB Positron) using contextily
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)

        # Labels and legend
        plt.title("Optimal Bus Stop Placement in Buenos Aires")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend()
        plt.show()
    except Exception as e:
        raise Exception(f"Failed to plot optimal bus stops: {str(e)}") from e