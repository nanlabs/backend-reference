# 🌍 Geospatial Urban Analysis Project

## 📌 Overview

This project focuses on **geospatial data analysis** for urban environments, particularly analyzing **pedestrian zones, transportation networks, census data, and geographic boundaries**. The dataset includes **shapefiles, GeoJSON, Parquet, and raster files**, allowing advanced **spatial processing and visualization**.

The project uses **PostgreSQL with PostGIS**, **Docker**, and **GeoPandas**, enabling **efficient spatial queries, ETL pipelines, and geospatial machine learning models**.

### ✨ **Key Features**

- 🏙 **Urban Infrastructure Analysis**: Analyzes bike paths, subway entrances, and school locations.
- 📊 **Geospatial Data Processing**: Supports various spatial formats (Shapefile, GeoJSON, Parquet, Raster).
- 🔄 **ETL Pipelines**: Extract, transform, and load urban data into **PostGIS**.
- 🤖 **Geospatial Machine Learning**: Clustering models to optimize urban planning decisions.
- 🗺 **Interactive Mapping**: Generates visualizations using **Folium and Matplotlib**.

---

## 🛠 **Requirements**

Before running the project, ensure you have the following dependencies installed:

### 💻 **System Requirements**

- 🐳 **Docker** (for PostgreSQL with PostGIS)
- 🐍 **Python 3.8+**

### 📦 **Python Dependencies**

All required Python libraries are listed in `requirements.txt`. Install them using:

```sh
pip install -r requirements.txt
```

Main dependencies:

- 🌍 **GeoPandas**: Geospatial data processing.
- 🗄 **PostgreSQL & PostGIS**: Geospatial database support.
- 📈 **Matplotlib & Folium**: Data visualization.
- 🤖 **Scikit-learn**: Clustering and machine learning models.

---

## 🚀 **Setup & Installation**

### 📂 **1. Clone the Repository**

```sh
git clone git@github.com:nanlabs/backend-reference.git
cd examples/geospatial-python-urban-analysis-with-postgis
```

### 🏗 **2. Set Up a Virtual Environment**

Create and activate a Python virtual environment:

```sh
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate  # On Windows
```

Once activated, install dependencies:

```sh
pip install -r requirements.txt
```

### 🐳 **3. Set Up Docker with PostgreSQL and PostGIS**

Ensure that **Docker** is installed and running. Then, start the database with:

```sh
docker-compose up -d
```

This will:

- 🛢 Start a **PostgreSQL database** with **PostGIS** extensions enabled.
- 📌 Create the necessary **database schema** for storing geospatial data.

## 📖 **Working with Notebooks**

To start the analysis and visualization:

```sh
jupyter notebook
```

Then, open one of the notebooks in the `notebooks/` directory.

The notebooks cover:

- 🌍 **Geospatial Data Exploration**: Loading and visualizing spatial datasets.
- 🚇 **Urban Accessibility Analysis**: Assessing accessibility of public transport.
- 🤖 **Clustering and Machine Learning**: Applying spatial clustering algorithms.


### 📌 **Pipelines Overview**
The project includes **several geospatial data processing pipelines**, located in `src/pipelines/`:

- 🚌 **`bus_stop_analysis.py`**: Analyzes bus stops and their spatial distribution.
- 📍 **`optimal_stop_pipeline.py`**: Computes the best locations for public transportation stops.
- 🗺 **`shapefile_to_raster.py`**: Converts vector-based shapefiles into raster format for GIS applications.

### ⚙️ **Running Pipelines**
To execute a pipeline, use the following command:

```sh
PYTHON=. python -m src.pipelines.bus_stop_analysis
```

Replace `bus_stop_analysis` with the pipeline you want to run.

Each pipeline processes geospatial data **efficiently**, ensuring the data is ready for **urban planning and visualization**.

---

## 🏗 **Project Structure**

```sh
.
├── Dockerfile                   # 🐳 Docker configuration for Python environment
├── docker-compose.yml           # 🛢 PostgreSQL + PostGIS setup
├── requirements.txt             # 📦 Python dependencies
├── config.py                    # ⚙️ Configuration settings
├── data/                        # 🌍 Raw geospatial datasets
├── notebooks/                   # 📖 Jupyter Notebooks for geospatial analysis
├── scripts/                     # 🔄 Data processing scripts
├── src/                         # 🏗 Source code
│   ├── database/                # 🗄 Database connection and queries
│   ├── etl/                     # 🔄 ETL pipeline for spatial data
│   ├── ml/                      # 🤖 Machine learning models for clustering
│   ├── pipelines/               # 📌 Spatial data processing workflows
│   ├── visualization/           # 🗺 Map and data visualization modules
```

---
