import pandas as pd
import plotly.graph_objects as go

from consts import Column, DATE_STRING_FORMAT


def plot_body_composition_chart(df: pd.DataFrame) -> go.Figure:
    sorted_df = df.sort_index()
    last_fat = sorted_df.iloc[0][Column.TOTAL_FAT]
    last_lean = sorted_df.iloc[0][Column.TOTAL_LEAN]
    starting_mass = sorted_df.iloc[0][Column.TOTAL_BMC] + last_fat + last_lean
    x = [f"{sorted_df.iloc[0].name.strftime(DATE_STRING_FORMAT)} Start Weight"]
    y = [starting_mass]
    measure = ["relative"]

    for date, row in sorted_df.iloc[1:].iterrows():
        x.append(f"{date.strftime(DATE_STRING_FORMAT)} Fat Delta")
        y.append(row[Column.TOTAL_FAT] - last_fat)
        measure.append("relative")
        x.append(f"{date.strftime(DATE_STRING_FORMAT)} Lean Delta")
        y.append(row[Column.TOTAL_LEAN] - last_lean)
        measure.append("relative")

        last_fat = row[Column.TOTAL_FAT]
        last_lean = row[Column.TOTAL_LEAN]

    ending_mass = (
        df.iloc[-1][Column.TOTAL_LEAN]
        + df.iloc[-1][Column.TOTAL_BMC]
        + df.iloc[-1][Column.TOTAL_FAT]
    )
    y.append(ending_mass)
    x.append("Current Mass")
    measure.append("total")

    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=measure,
            x=x,
            textposition="outside",
            # text=["+60", "+80", "", "-40", "-20", "Total"],
            y=y,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        )
    )
    fig.update_layout(yaxis_title="Mass (g)", showlegend=False)

    return fig
