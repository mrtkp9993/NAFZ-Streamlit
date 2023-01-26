import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from scipy import stats

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
st.write(
    "Data Source: [AFAD](https://deprem.afad.gov.tr), [ESHM20](http://hazard.efehr.org/en/Documentation/specific-hazard-models/europe/eshm2020-overview/eshm20-unified-earthquake-catalogue/)"
)


@st.cache(show_spinner=False)
def load_data():
    data = pd.read_csv("dataset_3.csv")
    data["magnitude"] = data["magnitude"].round(1)
    data["date"] = pd.to_datetime(data[["year", "month", "day", "hour", "minute"]])
    data = data.sort_values("date")
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
        hover_data=["depth"],
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
    data2 = data.groupby("year")["magnitude"].count().reset_index(name="Count")
    data2.year = data2.year.astype(str)
    st.plotly_chart(
        px.histogram(data2, x="year", y="Count")
        .update_layout(yaxis_title="Count")
        .update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}),
        use_container_width=True,
    )

with hist3:
    st.plotly_chart(
        px.histogram(
            data[data["Last Quake"] < 100],
            x="Last Quake",
            labels={"Last Quake": "Last Quake (Days)"},
        ).update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        ),
        use_container_width=True,
    )

st.header("Viz")

st.plotly_chart(
    px.scatter(data, x="date", y="magnitude", color="magnitude").update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    ),
    use_container_width=True,
)

st.plotly_chart(
    px.scatter(
        data,
        x="date",
        y="longitude",
        marginal_x="histogram",
        marginal_y="histogram",
        opacity=0.2,
    ).update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    ),
    use_container_width=True,
)

st.plotly_chart(
    px.scatter(
        data,
        x="date",
        y="latitude",
        marginal_x="histogram",
        marginal_y="histogram",
        opacity=0.2,
    ).update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    ),
    use_container_width=True,
)

st.plotly_chart(
    px.scatter(
        data,
        x="date",
        y="depth",
        marginal_x="histogram",
        marginal_y="histogram",
        opacity=0.2,
    ).update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    ),
    use_container_width=True,
)

st.header("Gutenberg-Richter Law")

with st.spinner("Calculating..."):
    magnitudes = np.arange(3.5, 8, 0.5)
    counts = np.zeros(magnitudes.shape[0])
    i = 0
    for m in magnitudes:
        counts[i] = data[data["magnitude"] >= m]["magnitude"].count()
        i += 1
    norm = np.sum(counts)
    counts_n = counts / norm
    counts_n_f = counts_n[counts_n != 0]
    magnitudes_f = magnitudes[counts_n != 0]
    reg = stats.linregress(magnitudes_f, np.log10(counts_n_f))

    trace1 = go.Scatter(
        x=magnitudes_f,
        y=counts_n_f,
        mode="markers",
        name="Observed",
    )

    trace2 = go.Scatter(
        x=magnitudes_f, y=10 ** (reg.intercept + reg.slope * magnitudes_f), name="Model"
    )

    fig = make_subplots()
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    fig.update_yaxes(type="log", showgrid=False, title="normalized counts")
    fig.update_xaxes(showgrid=False, title="m")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"$a = {reg.intercept:.2f} \pm {reg.intercept_stderr:.2f}$")
    st.markdown(f"$b = {reg.slope:.2f} \pm {reg.stderr:.2f}$")
    st.markdown(f"$R^2 = {reg.rvalue**2:.2f}$")
