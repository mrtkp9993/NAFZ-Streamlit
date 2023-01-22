from turtle import width

import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

pd.options.plotting.backend = "plotly"

st.set_page_config(
    page_title="NAFZ Earthquake Data Analysis, Visualization and Modeling - Murat Koptur",
    page_icon="☑️",
    layout="wide",
)
st.set_option("deprecation.showPyplotGlobalUse", False)

st.title("NAFZ Earthquake Data Analysis, Visualization and Modeling")
st.write("[muratkoptur.com](https://muratkoptur.com)")
st.write("[LinkedIn/muratkoptur](https://www.linkedin.com/in/muratkoptur/)")
st.markdown("---")

st.header("Raw Data")
st.write("Data Source: [SeismicPortal](http://www.seismicportal.eu)")

data_urls = [
    "https://www.seismicportal.eu/fdsnws/event/1/query?limit=4000&minlat=40.1727&maxlat=40.9139&minlon=24.9446&maxlon=30.9414&format=json&nodata=204&minmag=4",
    "https://www.seismicportal.eu/fdsnws/event/1/query?limit=4000&minlat=39.3112&maxlat=40.5724&minlon=35.9319&maxlon=41.1301&format=json&nodata=204&minmag=4",
    "https://www.seismicportal.eu/fdsnws/event/1/query?limit=4000&minlat=39.9273&maxlat=40.578&minlon=34.0891&maxlon=35.9319&format=json&nodata=204&minmag=4",
    "https://www.seismicportal.eu/fdsnws/event/1/query?limit=4000&minlat=40.7325&maxlat=40.8154&minlon=30.9338&maxlon=31.5057&format=json&nodata=204&minmag=4",
    "https://www.seismicportal.eu/fdsnws/event/1/query?limit=4000&minlat=40.617&maxlat=41.1407&minlon=31.2532&maxlon=36.6608&format=json&nodata=204&minmag=4",
    "https://www.seismicportal.eu/fdsnws/event/1/query?limit=4000&minlat=40.5743&maxlat=40.6674&minlon=30.417&maxlon=31.2635&format=json&nodata=204&minmag=4",
]


@st.cache
def load_data():
    datas = []
    for url in data_urls:
        data = requests.get(url)
        assert data.status_code == 200
        data = data.json()["features"]
        data = pd.json_normalize(data, sep="_")
        datas.append(data)
    return pd.concat(datas)


with st.spinner("Loading Data ..."):
    data = load_data()

st.plotly_chart(
    px.scatter_geo(
        data,
        lat="properties_lat",
        lon="properties_lon",
        color="properties_mag",
        size="properties_mag",
        hover_data=[
            "id",
            "properties_lastupdate",
            "properties_magtype",
            "properties_flynn_region",
        ],
    )
    .update_geos(
        projection_type="natural earth",
        lataxis_range=[38, 42],
        lonaxis_range=[24, 44],
    )
    .update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}),
    use_container_width=True,
)
st.dataframe(data, use_container_width=True)
