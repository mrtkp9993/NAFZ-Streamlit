from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from st_aggrid import AgGrid

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
st.write("Data Source: [AFAD](https://deprem.afad.gov.tr)")


@st.cache(show_spinner=False)
def load_data():
    data = pd.read_csv("dataset.csv")
    data["magnitude"] = data["magnitude"].round(1)
    data["date"] = pd.to_datetime(data["date"], infer_datetime_format=True)
    data = data[data["date"] < "2023-01-01"]
    data["Last Quake"] = data.date.diff().map(lambda x: x.total_seconds() / 86400)
    return data


with st.spinner("Loading Data ..."):
    data = load_data()


st.plotly_chart(
    px.scatter_geo(
        data[data["magnitude"] >= 5.0],
        lat="latitude",
        lon="longitude",
        color="magnitude",
        size="magnitude",
        hover_data=[
            "location",
            "depth",
            "idsource",
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

st.header("Histograms")

hist1, hist2, hist3 = st.columns(3)

with hist1:
    st.plotly_chart(
        px.histogram(data, x="magnitude", histnorm="probability density").update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        ),
        use_container_width=True,
    )

with hist2:
    data2 = (
        data.groupby(data["date"].map(lambda x: x.year))["eventID"]
        .count()
        .reset_index(name="Count")
    )
    data2.date = data2.date.astype(str)
    st.plotly_chart(
        px.histogram(data2, x="date", y="Count")
        .update_layout(yaxis_title="Count")
        .update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}),
        use_container_width=True,
    )

with hist3:
    st.plotly_chart(
        px.histogram(data[data["Last Quake"] < 100], x="Last Quake").update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        ),
        use_container_width=True,
    )
