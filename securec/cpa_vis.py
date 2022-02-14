import math
import numpy as np

from bokeh.plotting import figure, show
from bokeh.models import Title
from bokeh.palettes import Category20_20

from .cpa import pearson_pointwise_multi


def plot_traces_vs_correlation(
    traces,
    intermediates,
    plotpoints=20,
):
    # Compute data
    intermediates = intermediates.T
    plotpoints = min(plotpoints, len(traces))
    data = np.zeros((256, plotpoints))
    for i in range(0, plotpoints):
        j = math.ceil(i / plotpoints * len(traces))
        data[:, i] = np.max(
            np.abs(pearson_pointwise_multi(traces[:j, :], intermediates[:j, :])), axis=1
        )

    source = {
        "xs": len(data)
        * [list(range(0, len(traces), math.ceil(len(traces) / plotpoints)))],
        "ys": [corr for corr in data],
        "legend": list(range(256)),
        "color": (math.ceil(256 / 20) * Category20_20)[:256],
    }
    correlations = np.sort(data[:, -1])
    # Create figure
    p = figure(
        sizing_mode="stretch_width",
        height=300,
        tooltips=[("guess", "@legend"), ("correlation", "$y")],
    )
    p.multi_line(xs="xs", ys="ys", color="color", source=source)
    p.add_layout(
        Title(
            text=f"correlation ratio = {1 - correlations[-2] / correlations[-1]:.3f}",
            text_font_size="12pt",
        ),
        "above",
    )
    p.add_layout(
        Title(text=f"max correlation = {correlations[-1]:.3f}", text_font_size="12pt"),
        "above",
    )
    p.add_layout(Title(text="Traces vs Correlation", text_font_size="16pt"), "above")
    show(p)
