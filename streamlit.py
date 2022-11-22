from datetime import date, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from charts.waterfall import plot_body_composition_chart
from consts import DATE_STRING_FORMAT, Column
from helpers import is_local, to_string, validate_uploaded_file

st.set_page_config(
    page_title="DEXA Scan Analysis",
    page_icon="🏋️",
)

st.title("DEXA Scan Analysis")

# Load and validate data
uploaded_file = st.file_uploader("Choose a DEXA CSV file")
if is_local():
    df = pd.read_csv("scans.csv")
elif not uploaded_file:
    st.stop()
else:
    df = pd.read_csv(uploaded_file)

try:
    validate_uploaded_file(df)
except AssertionError as e:
    st.error(f"File does not contain required column: {e}")
    st.stop()

# Clean data
df[Column.SCAN_DATE.value] = pd.to_datetime(df[Column.SCAN_DATE.value]).dt.floor("D")
df = df.set_index(Column.SCAN_DATE.value)
if len(df.index) < 2:
    st.error("Not enough scans for a report. ", icon="🚨")
    st.stop()

# Filters
filter_cols = st.columns(4)
with filter_cols[0]:
    one_year_ago = date.today() - timedelta(days=365)
    min_date = st.date_input("From Date", value=one_year_ago)
with filter_cols[1]:
    max_date = st.date_input("To Date")

# Set some handy dates
scan_dates = list(df.index.values)
scan_dates.sort()
latest_date = scan_dates[-1]
prev_date = scan_dates[-2]
first_date = scan_dates[0]

# Raw Data
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(df)

# TOP LINE METRICS
# % Body Fat Metric
current_fat_perc = df.loc[latest_date][Column.TOTAL_FAT_PERC.value]
prev_fat_perc = df.loc[prev_date][Column.TOTAL_FAT_PERC.value]
delta_fat_perc = current_fat_perc - prev_fat_perc
st.metric(
    "Current % Body Fat",
    current_fat_perc,
    f"{delta_fat_perc:.2f} absolute",
    help=f"Change from the last data point on {to_string(prev_date)}",
)

# Charts
st.subheader("Total % Body Fat")
fig = px.area(
    df,
    y=Column.TOTAL_FAT_PERC.value,
    markers=True,
    labels={Column.TOTAL_FAT_PERC.value: "% Fat", Column.SCAN_DATE.value: "Scan Date"},
)
fig.update_yaxes(rangemode="tozero")
fig.update_xaxes(range=[min_date, max_date])
st.plotly_chart(fig)

st.subheader("Total Lean Mass")
fig = px.area(
    df,
    y=Column.TOTAL_LEAN.value,
    markers=True,
    labels={
        Column.TOTAL_LEAN.value: "Lean Mass (g)",
        Column.SCAN_DATE.value: "Scan Date",
    },
)
fig.update_xaxes(range=[min_date, max_date])
st.plotly_chart(fig)

st.subheader("Total Fat Mass")
fig = px.area(
    df,
    y=Column.TOTAL_FAT.value,
    markers=True,
    labels={Column.TOTAL_FAT.value: "Fat (g)", Column.SCAN_DATE.value: "Scan Date"},
)
fig.update_xaxes(range=[min_date, max_date])
st.plotly_chart(fig)

# Waterfall Chart
st.subheader("Body Comp Change over Time")
fig = plot_body_composition_chart(df)
st.plotly_chart(fig, use_container_width=True)

# Left vs Right
st.subheader("Left Arm vs Right Arm Lean mass")
fig = px.line(
    df,
    y=[Column.LEFT_ARM_FAT.value, Column.RIGHT_ARM_FAT.value],
    markers=True,
    labels={Column.SCAN_DATE.value: "Scan Date"},
)
fig.update_yaxes(rangemode="tozero")
fig.update_xaxes(range=[min_date, max_date])
st.plotly_chart(fig)
