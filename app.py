"""Interactive Central Limit Theorem simulation dashboard."""

from dataclasses import dataclass
from typing import Callable

import numpy as np
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Central Limit Theorem Explorer",
    page_icon="📊",
    layout="wide",
)


@dataclass(frozen=True)
class Distribution:
    """A distribution sampler and its theoretical moments."""

    name: str
    description: str
    mean: float
    standard_deviation: float
    sample: Callable[[tuple[int, ...]], np.ndarray]


st.title("📊 Central Limit Theorem Explorer")
st.markdown(
    "See how averages from repeated random samples become approximately normal—even "
    "when the population is skewed or discrete."
)

with st.sidebar:
    st.header("Simulation controls")
    distribution_name = st.selectbox(
        "Population distribution", ["Exponential", "Uniform", "Binomial"]
    )
    sample_size = st.slider("Sample size (n)", 1, 200, 30)
    simulation_count = st.slider(
        "Number of simulated samples", 500, 20_000, 5_000, step=500
    )
    seed = st.number_input("Random seed", 0, 1_000_000, 42)
    st.divider()
    st.subheader("Distribution parameters")

    rng = np.random.default_rng(seed)
    if distribution_name == "Exponential":
        scale = st.slider("Scale (mean)", 0.5, 5.0, 1.0, 0.1)
        distribution = Distribution(
            name="Exponential",
            description="A continuous, strongly right-skewed population.",
            mean=scale,
            standard_deviation=scale,
            sample=lambda size: rng.exponential(scale=scale, size=size),
        )
    elif distribution_name == "Uniform":
        lower = st.slider("Lower bound", -10.0, 0.0, 0.0, 0.5)
        upper = st.slider("Upper bound", 0.5, 10.0, 10.0, 0.5)
        distribution = Distribution(
            name="Uniform",
            description="A continuous population with equal density across its range.",
            mean=(lower + upper) / 2,
            standard_deviation=(upper - lower) / np.sqrt(12),
            sample=lambda size: rng.uniform(lower, upper, size=size),
        )
    else:
        trials = st.slider("Trials per observation", 1, 50, 10)
        probability = st.slider("Success probability", 0.05, 0.95, 0.30, 0.05)
        distribution = Distribution(
            name="Binomial",
            description="A discrete population counting successes across fixed trials.",
            mean=trials * probability,
            standard_deviation=np.sqrt(trials * probability * (1 - probability)),
            sample=lambda size: rng.binomial(trials, probability, size=size),
        )


# One population draw supports the left chart; the matrix represents repeated samples.
population = distribution.sample((50_000,))
samples = distribution.sample((simulation_count, sample_size))
sample_means = samples.mean(axis=1)

theoretical_mean = distribution.mean
simulated_mean = float(sample_means.mean())
theoretical_se = distribution.standard_deviation / np.sqrt(sample_size)
simulated_se = float(sample_means.std(ddof=1))

st.info(
    f"**{distribution.name}:** {distribution.description} Each point in the sampling "
    f"distribution is the mean of **{sample_size}** observations."
)

mean_col, sim_mean_col, se_col, sim_se_col = st.columns(4)
mean_col.metric("Theoretical mean", f"{theoretical_mean:.3f}")
sim_mean_col.metric(
    "Simulated mean", f"{simulated_mean:.3f}", f"{simulated_mean - theoretical_mean:+.3f}"
)
se_col.metric("Theoretical SE", f"{theoretical_se:.3f}")
sim_se_col.metric(
    "Simulated SE", f"{simulated_se:.3f}", f"{simulated_se - theoretical_se:+.3f}"
)

population_chart = go.Figure()
population_chart.add_histogram(
    x=population,
    histnorm="probability density",
    nbinsx=50,
    name="Population",
    marker_color="#2563EB",
    opacity=0.8,
)
population_chart.add_vline(
    x=theoretical_mean,
    line_dash="dash",
    line_color="#F97316",
    annotation_text="Theoretical mean",
)
population_chart.update_layout(
    title="Underlying population distribution",
    xaxis_title="Observation",
    yaxis_title="Density",
    showlegend=False,
    bargap=0.03,
)

sampling_chart = go.Figure()
sampling_chart.add_histogram(
    x=sample_means,
    histnorm="probability density",
    nbinsx=50,
    name="Simulated sample means",
    marker_color="#14B8A6",
    opacity=0.75,
)
x_min = min(float(sample_means.min()), theoretical_mean - 4 * theoretical_se)
x_max = max(float(sample_means.max()), theoretical_mean + 4 * theoretical_se)
x_values = np.linspace(x_min, x_max, 500)
normal_density = np.exp(
    -0.5 * ((x_values - theoretical_mean) / theoretical_se) ** 2
) / (theoretical_se * np.sqrt(2 * np.pi))
sampling_chart.add_trace(
    go.Scatter(
        x=x_values,
        y=normal_density,
        mode="lines",
        name="CLT normal approximation",
        line={"color": "#F97316", "width": 3},
    )
)
sampling_chart.add_vline(
    x=theoretical_mean, line_dash="dash", line_color="#7C3AED"
)
sampling_chart.update_layout(
    title="Sampling distribution of the sample mean",
    xaxis_title="Sample mean",
    yaxis_title="Density",
    legend={"orientation": "h", "y": 1.12, "x": 0},
    bargap=0.03,
)

left, right = st.columns(2)
left.plotly_chart(population_chart, use_container_width=True)
right.plotly_chart(sampling_chart, use_container_width=True)

st.subheader("What to notice")
st.markdown(
    f"""
- The sample means are centered near the theoretical population mean, **{theoretical_mean:.3f}**.
- Their theoretical spread is $SE(\\bar{{X}})=\\sigma/\\sqrt{{n}}={theoretical_se:.3f}$; the simulation gives **{simulated_se:.3f}**.
- Increase **sample size** to see the sampling distribution narrow and better match the orange normal curve.
- Increase **simulated samples** to reduce Monte Carlo noise in the histogram and metrics.
"""
)

with st.expander("Why does this happen?"):
    st.markdown(
        r"""
The Central Limit Theorem says that, under broad conditions, the standardized mean

$$Z = \frac{\bar{X}-\mu}{\sigma/\sqrt{n}}$$

approaches a standard normal distribution as $n$ increases. The original observations
do **not** need to be normally distributed. Sample size controls the mathematical
approximation; the number of simulations only controls how clearly we see it here.
"""
    )
