import geopandas as gpd
from shapely import wkt
import pandas as pd
import pickle

def change_crs(gdf, target_crs):
    if isinstance(gdf.index, gpd.GeoSeries):
        gdf.index= gdf.index.to_crs(epsg=target_crs)
    for c in gdf.columns:
        if isinstance(gdf[c], gpd.GeoSeries):
            gdf[c] = gdf[c].to_crs(epsg=target_crs)
    return gdf

def load_geodataframe(path, geometry, file_type, from_crs, crs):
    # GeoParquet (z. B. versionierte Datenpakete der IGC.NRW-Datenpipelines) bringt sein
    # CRS mit; der Dateityp wird an der Endung erkannt, die übrigen Typen bleiben gleich.
    if str(path).endswith(".parquet"):
        gdf = gpd.read_parquet(path)
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=from_crs)
        return gdf.to_crs(epsg=25832)
    if file_type == "gpd":
        gdf = gpd.read_file(path)
    elif file_type == "xlsx":
        df = pd.read_excel(path)
        df[geometry] = df[geometry].apply(lambda x: wkt.loads(x) if isinstance(x, str) else x)
        gdf = gpd.GeoDataFrame(df, geometry=geometry)
        gdf = gdf.set_crs(epsg=from_crs)
    elif file_type == "pickle":
        with open(path, "rb") as file:
            gdf = pickle.load(file)
        if not isinstance(gdf, gpd.GeoDataFrame):
            gdf = gpd.GeoDataFrame(gdf, geometry="location")
        gdf = gdf.set_crs(epsg=from_crs)
    else:
        raise ValueError("Unsupported file type")
    gdf = gdf.to_crs(epsg=25832)
    return gdf

def filter_nuts(gdf, nuts_id):
    gdf = gdf.reset_index()
    gdf = gdf.set_index('NUTS_ID')
    keep = False
    cntr_code = gdf.loc[nuts_id, 'CNTR_CODE']
    levl_code = gdf.loc[nuts_id, 'LEVL_CODE']
    if cntr_code == 'DE':
        if levl_code == 2:
            #if 'DE9' in nuts_id: #Niedersachsen
            keep = True
        elif levl_code == 3:
            if 'DEA' in nuts_id: # NRW
                keep = True
    elif cntr_code in ['NL']:
        if levl_code == 2:
            keep = True
    return keep

def load_grid(path):
    """Vereinfachten Graphen laden: RUB-Pickle (``simple_grid_*.pkl``) oder GeoParquet mit den
    Spalten ``from_x``, ``from_y``, ``to_x``, ``to_y``, ``distance_km`` und Geometrie
    (EPSG:25832), z. B. ``road_simplified.parquet``/``waterway_simplified.parquet`` des
    Datenpakets ``transport-network`` (IGC.NRW). Ergebnis in der Form des Pickles."""
    from shapely.geometry import Point

    if not str(path).endswith(".parquet"):
        with open(path, "rb") as file:
            return pickle.load(file)
    edges = gpd.read_parquet(path).to_crs(epsg=25832)
    grid = gpd.GeoDataFrame(
        {
            "Point i": [Point(x, y) for x, y in zip(edges["from_x"], edges["from_y"])],
            "Point j": [Point(x, y) for x, y in zip(edges["to_x"], edges["to_y"])],
            "Distance_ij": edges["distance_km"].to_numpy(),
            "Link_ij": edges.geometry.to_numpy(),
        },
        geometry="Link_ij",
        crs=25832,
    )
    grid.index = pd.Index(grid["Link_ij"], name="Link_ij_index")
    return grid
