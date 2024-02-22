# %%
import pydeck as pdk
import geopandas as gpd
from datetime import datetime
import pandas as pd


def SCOPE():
    bounds = [
        [
            [1.68153079591, 49.959999905],
            [1.68153079591, 58.6350001085],
            [-7.57216793459, 58.6350001085],
            [-7.57216793459, 49.959999905],
        ]
    ]
    return bounds


def INITIAL_VIEW_STATE():
    startup_view_params = pdk.ViewState(
        latitude=52.561928,
        longitude=-1.464854,
        zoom=9,
        max_zoom=16,
        pitch=60,
        bearing=0,
    )
    return startup_view_params


def PolygonLayer():
    polygon = pdk.Layer(
        "PolygonLayer",
        SCOPE(),
        stroked=False,
        # processes the data as a flat longitude-latitude pair
        get_polygon="-",
        get_fill_color=[0, 0, 0, 20],
    )
    return polygon


def GeoJsonLayer(data, elevation_dim=None, fill_dim=None):
    if not elevation_dim:
        elevation_dim = 1
    if not fill_dim:
        fill_dim = 1

    geojson = pdk.Layer(
        "GeoJsonLayer",
        data,
        opacity=0.5,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation=f"{elevation_dim} * 10",
        get_fill_color=f"[255, {fill_dim} * 255, {fill_dim} * 255]",
        get_line_color=[255, 255, 255],
        pickable=True,
    )
    return geojson


def IconLayer(data_path, icon_url):
    icon_data = {
        "url": icon_url,
        "width": 96,
        "height": 96,
        "anchorY": 96,
    }

    data = pd.read_csv(data_path)
    data["icon_data"] = None
    for i in data.index:
        data["icon_data"][i] = icon_data

    icon_layer = pdk.Layer(
        type="IconLayer",
        data=data,
        get_icon="icon_data",
        get_size=4,
        size_scale=5,
        get_position=["stop_lon", "stop_lat"],
        pickable=True,
    )

    view_state = pdk.data_utils.compute_view(data[["stop_lon", "stop_lat"]], 0.1)

    return icon_layer, view_state


def Visualiser(layers: list[object], view_state=None, tooltip: bool | dict = False):
    if view_state is None:
        view_state = INITIAL_VIEW_STATE()

    r = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    r.to_html(f"pydeck_examples/outputs/example_{timestamp}.html")

    return None


# %%
# Example of the PolygonLayer()
polygon = PolygonLayer()
Visualiser([polygon])


# %%
# Example of the GeoJsonLayer()
data = gpd.read_file("pydeck_examples/data/LAD_boundaries.geojson")
geojson = GeoJsonLayer(data)
Visualiser(layers=[geojson])


# %%
# Adding dims to layers
data = gpd.read_file("pydeck_examples/data/LSOA_leeds_punctuality_EXAMPLE.geojson")
geojson = GeoJsonLayer(data, "count", "mean")
# Note combined layers
Visualiser(layers=[polygon, geojson])


# %%
# Adding Tooltip
Visualiser(layers=[polygon, geojson], tooltip=True)


# %%
# Bespoke Tooltip
tooltip = {
    "html": "<b>LSOA name:</b> {LSOA21NM} <br/> <b>LSOA code:</b> {LSOA21CD} <br/> <b>Daily service stops:</b> {count} <br/> <b>Proportion punctual:</b> {mean}",  # noqa: E501
    "style": {
        "backgroundColor": "black",
        "color": "white",
        "font-family": "Arial",
    },
}
Visualiser(layers=[polygon, geojson], tooltip=tooltip)


# %%
# Adding Icons
icon_url = "https://upload.wikimedia.org/wikipedia/commons/c/ce/ISO_7001_PI_TF_006.svg"
data_path = "pydeck_examples/data/north_east_stops.csv"
icons, view_state = IconLayer(data_path, icon_url)
tooltip = {
    "html": "<b>Stop ID:</b> {stop_id} <br/> <b>Daily Service Stops:</b> {service_stops} <br/>",  # noqa: E501
    "style": {
        "backgroundColor": "black",
        "color": "white",
        "font-family": "Arial",
    },
}
Visualiser(layers=[icons], view_state=view_state, tooltip=tooltip)
