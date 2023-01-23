import pandas as pd
import plotly.express as px
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
st.write("Data Source: [AFAD](https://deprem.afad.gov.tr)")


@st.cache(show_spinner=False)
def load_data():
    data = pd.read_csv("dataset.csv")
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
