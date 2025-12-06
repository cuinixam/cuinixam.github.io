# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "pandas==2.2.3",
#     "numpy==2.2.1",
#     "scipy==1.14.1",
#     "matplotlib==3.10.1",
#     "plotly==5.24.1",
# ]
# ///

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Statistical Analysis of Experimental Data
    ## A Practical Guide to Processing and Interpreting Scientific Measurements

    ### Overview

    This notebook demonstrates how to analyze experimental data using basic statistical methods.
    We'll work through an example to show the practical steps involved in exploring data,
    assessing distributions, and ranking samples based on multiple parameters.

    **Analysis Steps:**

    - Descriptive statistics (mean, median, standard deviation, etc.)
    - Normality testing (Shapiro-Wilk, Anderson-Darling)
    - Variability analysis across samples
    - Data normalization for multi-parameter comparison
    - Performance ranking

    ### Example Dataset: Microscale Combustion Calorimetry (MCC)

    We'll use data from fire-starter briquette research to illustrate these concepts.

    ⚠️This example data was adapted from published literature for educational purposes.

    Various compositions were tested, measuring four key parameters:

    - **Residue (%)**: Amount of material left after combustion (lower = better efficiency)
    - **THR (kJ/g)**: Total Heat Release (higher = more energy)
    - **HRC (J/g·K)**: Heat Release Capacity (higher = more intense combustion)
    - **Time1 (s)**: Time to ignition (lower = faster ignition)

    > **Source:**
    > Victoria Bejenari, Daniela Rusu, Ion Anghel, Ioana-Emilia Șofran, Gabriela Lisa,
    > "Fire-starting briquettes with high spent coffee-ground content and various wax types,"
    > *Biofuels, Bioproducts and Biorefining*, 19(6), 2025, 2076-2091.
    > https://doi.org/10.1002/bbb.2810
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 1. Data Loading and Preparation
    """)
    return


@app.cell
def _():
    import io
    from dataclasses import dataclass

    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    from scipy import stats
    from scipy.stats import kurtosis, skew

    return dataclass, go, io, kurtosis, np, pd, plt, px, skew, stats


@app.cell
def _(dataclass, kurtosis, np, skew):
    @dataclass
    class ParameterData:
        """Holds information about a single parameter."""

        name: str  # Column name in DataFrame (e.g., "Residue")
        units: str  # Units of the parameter (e.g., "%", "kJ/g")
        description: str  # Brief parameter description
        values: np.ndarray  # Actual measurement values

        @property
        def display_name(self) -> str:
            """Display name with units (e.g., "Residue (%)")."""
            return f"{self.name} ({self.units})" if self.units else self.name

        @property
        def count(self) -> int:
            """Number of non-NaN values."""
            return int(np.sum(~np.isnan(self.values)))

        @property
        def has_data(self) -> bool:
            """Check if parameter has valid data."""
            return self.count > 0

    @dataclass
    class DescriptiveStats:
        """Calculates and stores descriptive statistics for a parameter."""

        parameter: ParameterData

        def __post_init__(self):
            """Calculate all statistics after initialization."""
            self._calculate_stats()

        def _calculate_stats(self):
            """Compute all statistical measures."""
            vals = self.parameter.values[~np.isnan(self.parameter.values)]

            if len(vals) == 0:
                # Set defaults for empty data
                self.mean = self.median = self.std = 0.0
                self.min_val = self.max_val = 0.0
                self.q1 = self.q3 = 0.0
                self.skewness = self.kurtosis = 0.0
                self.cv = 0.0
                self.iqr = 0.0
                return

            # Central tendency
            self.mean = float(np.mean(vals))
            self.median = float(np.median(vals))
            self.std = float(np.std(vals, ddof=1))  # Sample std dev

            # Range
            self.min_val = float(np.min(vals))
            self.max_val = float(np.max(vals))

            # Quartiles
            self.q1 = float(np.percentile(vals, 25))
            self.q3 = float(np.percentile(vals, 75))
            self.iqr = self.q3 - self.q1

            # Distribution shape
            self.skewness = float(skew(vals))
            self.kurtosis = float(kurtosis(vals))

            # Coefficient of variation
            self.cv = (self.std / self.mean * 100) if self.mean != 0 else 0.0

        def get_variability_text(self) -> str:
            """Interpret variability based on CV."""
            if self.cv > 50:
                return f"**high variability** (CV={self.cv:.1f}%), indicating inconsistent measurements across samples"
            elif self.cv < 15:
                return f"**low variability** (CV={self.cv:.1f}%), indicating consistent measurements across samples"
            else:
                return f"**moderate variability** (CV={self.cv:.1f}%)"

        def get_skewness_text(self) -> str:
            """Interpret skewness."""
            if abs(self.skewness) < 0.5:
                return f"approximately **symmetric** (skewness={self.skewness:.2f}), with balanced data around the center"
            elif self.skewness > 0.5:
                return f"**right-skewed** (skewness={self.skewness:.2f}), with a longer tail toward higher values and mean > median"
            else:
                return f"**left-skewed** (skewness={self.skewness:.2f}), with a longer tail toward lower values and mean < median"

        def get_kurtosis_text(self) -> str:
            """Interpret kurtosis."""
            if self.kurtosis > 1:
                return f"**heavy tails** (kurtosis={self.kurtosis:.2f}), suggesting presence of outliers or extreme values"
            elif self.kurtosis < -1:
                return f"**light tails** (kurtosis={self.kurtosis:.2f}), with fewer outliers than a normal distribution"
            else:
                return f"tail behavior is similar to a normal distribution (kurtosis={self.kurtosis:.2f})"

        def generate_description(self) -> str:
            """Generate complete descriptive text for the parameter."""
            param_name = self.parameter.display_name

            central_text = f"The {param_name} values range from {self.min_val:.2f} to {self.max_val:.2f}, with a mean of {self.mean:.2f} and median of {self.median:.2f}. "
            var_text = f"The data shows {self.get_variability_text()}. "
            skew_text = f"The distribution is {self.get_skewness_text()}. "
            kurt_text = f"The distribution has {self.get_kurtosis_text()}. "
            iqr_text = f"The interquartile range (IQR) is {self.iqr:.2f}, representing the spread of the middle 50% of data."

            return central_text + var_text + skew_text + kurt_text + iqr_text

        def to_dict(self) -> dict:
            """Convert statistics to dictionary format."""
            return {
                "count": self.parameter.count,
                "mean": self.mean,
                "std": self.std,
                "cv": self.cv,
                "min": self.min_val,
                "25%": self.q1,
                "50%": self.median,
                "75%": self.q3,
                "max": self.max_val,
                "skewness": self.skewness,
                "kurtosis": self.kurtosis,
            }

    return DescriptiveStats, ParameterData


@app.cell
def _(mo):
    mo.md("""
    ### Load Your Data

    You can either:

    - **Use the example dataset** (fire-starter briquettes MCC data) loaded by default
    - **Upload your own CSV file** with similar structure (Sample column + numerical parameters)
    """)
    return


@app.cell
def _(mo):
    # File upload widget for custom CSV
    file_upload = mo.ui.file(kind="button", filetypes=[".csv"], label="Upload CSV (optional)")
    # Show file upload element
    file_upload  # noqa: B018
    return (file_upload,)


@app.cell
def _(ParameterData, file_upload, io, np, pd):
    # Default example data - Fire-starter briquettes MCC measurements
    default_data = """Sample,Residue,THR,HRC,Time1
        A,7.69,13.56,157.13,151.5
        L,22.38,12.12,159.48,142
        GB,25.63,10.97,133.8,155.5
        M,13.42,9.87,100.33,131
        Pa,21.01,14.65,165.38,160.5
        Pb,27.89,16.7,148.26,157.5
        Pc,27.47,18.85,245.01,136
        P6,23.04,13.7,177.02,128
        P7,19.82,17.01,240.03,131
        P8,20.65,14.91,210.9,100
        P9,18.88,16.32,223.09,150
        P11,17.62,17.3,254.41,136
        PS,18.62,8.98,134.46,179"""

    # Use uploaded file if available, otherwise use default
    if file_upload.value:
        df = pd.read_csv(io.BytesIO(file_upload.value[0].contents))
        data_source = "Uploaded CSV"
    else:
        df = pd.read_csv(io.StringIO(default_data))
        data_source = "Example dataset (MCC fire-starter briquettes)"

    # Clean column names
    df.columns = df.columns.str.strip()

    # Validate that we have at least 2 columns (Sample + at least 1 parameter)
    if len(df.columns) < 2:
        raise ValueError("CSV file must have at least 2 columns (Sample column + parameter columns)")

    # Validate that we have at least 1 row of data
    if len(df) == 0:
        raise ValueError("CSV file is empty - no data rows found")

    # Extract sample information before processing parameters
    sample_names = df.iloc[:, 0].tolist()
    num_samples = len(df)

    # Display info
    print(f"📊 Data source: {data_source}")
    print(f"📏 Dataset shape: {df.shape}")
    print(f"🔢 Number of samples: {num_samples}")
    print(f"📈 Parameters: {', '.join(df.columns[1:].tolist())}")

    # Create ParameterData objects for each parameter column (skip first column which is Sample)
    parameters_data = []

    # Default parameter metadata for MCC dataset
    param_metadata = {
        "Residue": {"units": "%", "description": "Combustion efficiency (lower = better)"},
        "THR": {"units": "kJ/g", "description": "Total heat released (higher = better)"},
        "HRC": {"units": "J/g·K", "description": "Heat release capacity (higher = better)"},
        "Time1": {"units": "s", "description": "Time to ignition (lower = faster ignition)"},
    }

    # Process each known parameter and find matching column
    for param_name, metadata in param_metadata.items():
        # Find column that contains this parameter name (case-insensitive)
        matching_col = None
        for col in df.columns[1:]:  # Skip first column (Sample)
            if param_name.lower() in col.lower():
                matching_col = col
                break

        # If no matching column found, skip this parameter
        if matching_col is None:
            continue

        # Try to get numeric values, skip if column can't be converted to numeric
        try:
            values = pd.to_numeric(df[matching_col], errors="coerce").values
        except Exception:
            print(f"⚠️ Skipping parameter '{param_name}' (column '{matching_col}') - cannot convert to numeric values")
            continue

        parameters_data.append(
            ParameterData(
                name=param_name,  # Use the standardized parameter name
                units=metadata["units"],
                description=metadata["description"],
                values=values,
            )
        )
    return data_source, num_samples, parameters_data, sample_names


@app.cell
def _(parameters_data, DescriptiveStats, ParameterData):
    # Calculate descriptive statistics for each parameter
    param_stats: dict[str, DescriptiveStats] = {param_data.name: DescriptiveStats(param_data) for param_data in parameters_data}

    # Create a convenience dictionary for accessing parameters by name
    parameters: dict[str, ParameterData] = {p.name: p for p in parameters_data}

    return param_stats, parameters


@app.cell
def _(data_source, num_samples, parameters_data, sample_names, mo):
    mo.md(f"""
    ### Dataset Overview

    **Source:** {data_source}

    We have **{num_samples} samples** labeled: {", ".join(str(s) for s in sample_names)}

    **Parameters found:** {", ".join(param.display_name for param in parameters_data)}
    """)
    return


@app.cell
def _(mo, parameters_data, pd, sample_names):
    # Reconstruct the data table from parameter data for display
    _table_data = {"Sample": sample_names}

    for _param_data in parameters_data:
        _table_data[_param_data.name] = _param_data.values

    # Display the dataframe
    _display_table = mo.ui.table(
        data=pd.DataFrame(_table_data),
        pagination=False,
        show_column_summaries=False,
    )
    _display_table  # noqa: B018
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    **Step 1 Complete!** ✅

    We've successfully:

    - Loaded the MCC dataset
    - Displayed the data in an interactive table

    **Next Step:**

    - Calculate descriptive statistics
    - Visualize distributions
    - Test for normality
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 2. Descriptive Statistics

    Descriptive statistics summarize the central tendency, dispersion, and shape of the data distribution.
    They provide the foundation for understanding your dataset before conducting inferential tests.

    **Key Metrics Explained:**

    **Central Tendency:**

    - **Mean**: The arithmetic average. Sensitive to outliers; if much different from median, suggests skewed data.
        - *Example:* Dataset [2, 3, 3, 4, 100] → Mean = 22.4 (pulled up by outlier '100')
    - **Median (50%)**: The middle value when data is sorted. More robust than mean for skewed distributions.
        - *Example:* Same dataset [2, 3, **3**, 4, 100] → Median = 3 (not affected by outlier)

    **Dispersion (Spread):**

    - **Std Dev (Standard Deviation)**: Average distance from the mean. Higher values indicate more variability.
        - *Example:* [10, 10, 10] → Std = 0 (no variation) vs [1, 10, 19] → Std = 9.0 (high variation)
    - **CV (Coefficient of Variation)**: Std Dev / Mean x 100%. Measures relative variability, useful for comparing variability across different scales.
        - < 15%: Low variability (consistent measurements)
        - 15-50%: Moderate variability
        - \\> 50%: High variability (inconsistent measurements)
        - *Example:* Dataset A [100, 110, 90] → CV=10%, Dataset B [10, 11, 9] → CV=10% (same relative variability despite different scales)
    - **Min/Max**: The range boundaries. Large range suggests high variability or potential outliers.
    - **25% (Q1) and 75% (Q3)**: First and third quartiles. The middle 50% of data lies between these values.
        - *Example:* [1, 2, **3**, 4, 5, **6**, 7, 8, 9] → Q1=3, Q3=6, IQR=3
    - **IQR (Q3-Q1)**: Interquartile range, a robust measure of spread.

    **Distribution Shape:**

    - **Skewness**: Measures asymmetry
        - ≈ 0: Symmetric distribution (normal-like) *[5, 6, 7, 8, 9]*
        - \\> 0: Right-skewed (tail extends to higher values) *[1, 2, 3, 4, 100]*
        - < 0: Left-skewed (tail extends to lower values) *[1, 50, 51, 52, 53]*
        - |Skewness| > 2: Highly skewed
    - **Kurtosis**: Measures tail heaviness (relative to normal distribution)
        - ≈ 0: Similar to normal distribution (bell curve)
        - \\> 0: Heavy tails (more outliers than normal) *[1, 5, 5, 5, 100]*
        - < 0: Light tails (fewer outliers than normal) *[4, 5, 5, 5, 6]*
        - |Kurtosis| > 3: Significantly different from normal

    **Practical Insights:**

    - Compare mean vs median to detect skewness
    - High std dev / mean ratio indicates high relative variability
    - Check if min/max values are realistic (data quality)
    - Use quartiles to identify where most data concentrates
    """)
    return


@app.cell
def _(param_stats, pd):
    # Create descriptive statistics table from DescriptiveStats objects
    stats_dict = {}
    for _param_name, stats_obj in param_stats.items():
        stats_dict[_param_name] = stats_obj.to_dict()

    desc_stats = pd.DataFrame(stats_dict).T
    desc_stats = desc_stats.round(3)
    # Display the descriptive statistics table
    desc_stats  # noqa: B018
    return (desc_stats,)


@app.cell
def _(mo):
    mo.md("""
    ### Statistical Summary Analysis

    The table above shows comprehensive descriptive statistics for all parameters.
    Below, we analyze each parameter individually with descriptive insights and visual representations.
    """)
    return


@app.cell
def _(np):
    # Helper functions for parameter analysis
    def create_parameter_histogram(param_display, param_values, stats_obj, go):
        """
        Create a histogram with statistical markers for a parameter.

        Arguments:
            param_display: Display name with units (e.g., "Residue (%)")
            param_values: numpy array of values
            stats_obj: DescriptiveStats object containing statistics
            go: plotly.graph_objects module

        """
        data_vals = param_values[~np.isnan(param_values)]

        fig = go.Figure()

        # Histogram
        fig.add_trace(
            go.Histogram(
                x=data_vals,
                name="Distribution",
                nbinsx=10,
                marker={"color": "lightblue", "line": {"color": "darkblue", "width": 1}},
                opacity=0.7,
            )
        )

        # Statistical markers
        fig.add_vline(x=stats_obj.mean, line={"color": "red", "width": 2, "dash": "solid"})
        fig.add_vline(x=stats_obj.median, line={"color": "green", "width": 2, "dash": "dash"})
        fig.add_vline(x=stats_obj.q1, line={"color": "orange", "width": 1, "dash": "dot"})
        fig.add_vline(x=stats_obj.q3, line={"color": "orange", "width": 1, "dash": "dot"})

        # Legend box
        legend_text = f"""<b>Statistical Markers:</b><br>
        Mean: {stats_obj.mean:.2f} <span style="color:red">━━</span><br>
        Median: {stats_obj.median:.2f} <span style="color:green">╌╌</span><br>
        Q1: {stats_obj.q1:.2f} <span style="color:orange">···</span><br>
        Q3: {stats_obj.q3:.2f} <span style="color:orange">···</span>"""

        fig.add_annotation(
            text=legend_text,
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.98,
            xanchor="right",
            yanchor="top",
            showarrow=False,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            borderpad=8,
        )

        fig.update_layout(
            title=f"{param_display} Distribution",
            xaxis_title=param_display,
            yaxis_title="Frequency",
            showlegend=False,
            height=400,
        )

        return fig

    return create_parameter_histogram


@app.cell
def _(create_parameter_histogram, go, mo, param_stats, parameters_data):
    # Dynamic parameter analysis - iterate over all available parameters
    # Each parameter gets its own chapter with description and histogram
    _param_chapters = []

    for _param_data in parameters_data:
        _param_name = _param_data.name
        if _param_name in param_stats:
            _stats = param_stats[_param_name]
            _desc = _stats.generate_description()

            # Create histogram for this parameter
            _fig = create_parameter_histogram(_param_data.display_name, _param_data.values, _stats, go)

            # Combine description and histogram in a chapter
            _param_chapters.append(
                mo.vstack(
                    [
                        mo.md(f"""
                    #### {_stats.parameter.display_name}

                    {_desc}
                    """),
                        _fig,
                    ]
                )
            )

    # Stack all parameter chapters vertically
    mo.vstack(_param_chapters) if _param_chapters else mo.md("_No parameters found in dataset_")
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 3. Normality Testing

    Many statistical tests assume data follows a normal (Gaussian) distribution. We test this assumption
    using both statistical tests and visual methods.

    **Why It Matters:**

    - **Parametric tests** (t-test, ANOVA) require normality
    - **Non-parametric tests** (Mann-Whitney, Kruskal-Wallis) don't require normality
    - Helps choose the appropriate statistical method

    **Tests Used:**

    - **Shapiro-Wilk Test**: Most powerful for small-medium samples (n < 50) - **recommended for your dataset**
    - **Anderson-Darling Test**: Excellent for small samples, particularly sensitive to deviations at distribution tails
    - **Kolmogorov-Smirnov Test**: Better suited for larger samples (n ≥ 50)
    - **Q-Q Plots**: Visual assessment of normality

    **Interpretation:**

    - **Shapiro-Wilk & K-S**: p-value < 0.05 → reject normality (data is NOT normal)
    - **Anderson-Darling**: Statistic > Critical Value (at 5%) → reject normality (data is NOT normal)

    **For Small Datasets (n ≈ 10-15):**

    Shapiro-Wilk and Anderson-Darling are your best options. K-S test has lower statistical power
    with small samples and may fail to detect non-normality.
    """)
    return


@app.cell
def _(np, parameters_data, pd, stats):
    # Perform normality tests using parameter data
    _normality_results = []

    for _param_data in parameters_data:
        # Get non-NaN values from parameter data
        _data = _param_data.values[~np.isnan(_param_data.values)]

        # Shapiro-Wilk test (best for small samples, n < 50)
        _shapiro_stat, _shapiro_p = stats.shapiro(_data)

        # Anderson-Darling test (excellent for small samples, more sensitive at tails)
        _ad_result = stats.anderson(_data, dist="norm")
        # Get critical value for 5% significance level (index 2 corresponds to 5%)
        _ad_critical_5pct = _ad_result.critical_values[2]
        _ad_normal = "✅ Yes" if _ad_result.statistic < _ad_critical_5pct else "❌ No"

        # Kolmogorov-Smirnov test (better for larger samples)
        _ks_stat, _ks_p = stats.kstest(_data, "norm", args=(_data.mean(), _data.std()))

        _normality_results.append(
            {
                "Parameter": _param_data.name,
                "Shapiro-W": round(_shapiro_stat, 4),
                "Shapiro p": round(_shapiro_p, 4),
                "Shapiro?": "✅ Yes" if _shapiro_p > 0.05 else "❌ No",
                "A-D Stat": round(_ad_result.statistic, 4),
                "A-D Crit(5%)": round(_ad_critical_5pct, 4),
                "A-D?": _ad_normal,
                "K-S Stat": round(_ks_stat, 4),
                "K-S p": round(_ks_p, 4),
                "K-S?": "✅ Yes" if _ks_p > 0.05 else "❌ No",
            }
        )

    normality_df = pd.DataFrame(_normality_results)
    # Show the normality test results table
    normality_df  # noqa: B018
    return (normality_df,)


@app.cell
def _(mo, normality_df):
    # Check normality based on all three tests
    non_normal_shapiro = normality_df[normality_df["Shapiro?"] == "❌ No"]["Parameter"].tolist()
    non_normal_ad = normality_df[normality_df["A-D?"] == "❌ No"]["Parameter"].tolist()
    non_normal_ks = normality_df[normality_df["K-S?"] == "❌ No"]["Parameter"].tolist()

    mo.md(f"""
    ### Normality Test Results

    **Summary:**

    - **Shapiro-Wilk Test** (best for small samples, n < 50):
        - Normal: {len(normality_df) - len(non_normal_shapiro)} parameters
        - Non-normal: {len(non_normal_shapiro)} parameters {f"({', '.join(non_normal_shapiro)})" if non_normal_shapiro else ""}

    - **Anderson-Darling Test** (excellent for small samples, sensitive at distribution tails):
        - Normal: {len(normality_df) - len(non_normal_ad)} parameters
        - Non-normal: {len(non_normal_ad)} parameters {f"({', '.join(non_normal_ad)})" if non_normal_ad else ""}

    - **Kolmogorov-Smirnov Test** (better for larger samples):
        - Normal: {len(normality_df) - len(non_normal_ks)} parameters
        - Non-normal: {len(non_normal_ks)} parameters {f"({', '.join(non_normal_ks)})" if non_normal_ks else ""}

    **Note for Small Datasets (n ≈ 10-15):**

    - **Shapiro-Wilk** and **Anderson-Darling** are the most reliable tests for your sample size
    - **Anderson-Darling** is particularly good at detecting deviations in the tails
    - **K-S test** has lower power with small samples and may miss non-normality
    - When tests disagree, prioritize Shapiro-Wilk/Anderson-Darling results
    - Always examine the Q-Q plots below for visual confirmation
    """)
    return non_normal_shapiro, non_normal_ks


@app.cell
def _(go, np, parameters_data, stats):
    # Create Q-Q plots for visual normality assessment using parameter data
    import math

    from plotly.subplots import make_subplots

    _n_params = len(parameters_data)
    _n_cols = 2
    _n_rows = math.ceil(_n_params / _n_cols)
    _param_names = [p.name for p in parameters_data]

    fig_qq = make_subplots(
        rows=_n_rows,
        cols=_n_cols,
        subplot_titles=_param_names,
        vertical_spacing=0.12,
        horizontal_spacing=0.1,
    )

    for _idx, _param_data in enumerate(parameters_data):
        _row = _idx // _n_cols + 1
        _col = _idx % _n_cols + 1

        # Get non-NaN values and sort them
        _qq_data = _param_data.values[~np.isnan(_param_data.values)]
        _qq_data = np.sort(_qq_data)
        _theoretical_q = stats.norm.ppf(np.linspace(0.01, 0.99, len(_qq_data)))

        # Scatter plot of quantiles
        fig_qq.add_trace(
            go.Scatter(
                x=_theoretical_q,
                y=_qq_data,
                mode="markers",
                name=_param_data.name,
                marker={"size": 6, "color": "steelblue"},
                showlegend=False,
            ),
            row=_row,
            col=_col,
        )

        # Reference line (ideal normal)
        fig_qq.add_trace(
            go.Scatter(
                x=_theoretical_q,
                y=_theoretical_q * _qq_data.std() + _qq_data.mean(),
                mode="lines",
                line={"color": "red", "dash": "dash"},
                showlegend=False,
            ),
            row=_row,
            col=_col,
        )

        fig_qq.update_xaxes(title_text="Theoretical Quantiles", row=_row, col=_col)
        fig_qq.update_yaxes(title_text="Sample Quantiles", row=_row, col=_col)

    fig_qq.update_layout(
        title_text="Q-Q Plots (Normality Assessment)",
        height=300 * _n_rows,
        template="plotly_white",
    )

    # Display the Q-Q plots
    fig_qq  # noqa: B018
    return (fig_qq,)


@app.cell
def _(mo):
    mo.md("""
    **Q-Q Plot Interpretation:**

    - Points close to the red dashed line → data is approximately normal
    - Systematic deviation from the line → non-normal distribution
    - S-shaped curve → heavy or light tails
    - Points far from the line → outliers

    ---

    **Step 2 Complete!** ✅

    We've successfully:

    - Calculated descriptive statistics
    - Visualized distributions with box plots and histograms
    - Tested for normality using different statistical tests
    - Created Q-Q plots for visual assessment

    **Next Step:**

    - Assess data variability and choose appropriate analysis methods
    - Data normalization
    - Performance scoring
    """)
    return


@app.cell
def _(mo, normality_df):
    # Dynamic recommendation based on normality test results
    _all_normal_shapiro = all(normality_df["Shapiro?"] == "✅ Yes")
    _all_normal_ad = all(normality_df["A-D?"] == "✅ Yes")

    _data_is_normal = _all_normal_shapiro or _all_normal_ad
    _normality_text = "**follow normal distributions**" if _data_is_normal else "show some deviation from normality"

    mo.md(f"""
    ---
    ## Statistical Analysis: Choosing the Right Approach

    Based on our normality testing results, our parameters {_normality_text}.

    ### Understanding Our Data Structure

    Before selecting statistical methods, we need to understand what we have:

    **Our Dataset Characteristics:**

    - **13 samples** (A, L, GB, M, Pa, Pb, Pc, P6, P7, P8, P9, P11, PS)
    - **4 parameters** measured per sample (Residue, THR, HRC, Time1)
    - **1 measurement per sample** for each parameter (no replicates)
    - Each sample represents a **unique formulation** (not repeated measurements)

    **Data Distribution:**

    - Normality tests completed (Shapiro-Wilk, Anderson-Darling, K-S)
    - Q-Q plots examined for visual confirmation
    - Distribution characteristics assessed

    ### Statistical Analysis Options

    Given our data structure and goals, we have several approaches to consider:

    #### Option 1: Traditional ANOVA (Analysis of Variance)
    **Requirements:**

    - Multiple measurements per group (replicates) ✗ **We don't have this**
    - Normal distribution ✓ (confirmed)
    - Equal variances across groups (homogeneity)

    **Why it doesn't work for our data:**

    - ANOVA compares **between-group variance** to **within-group variance**
    - Formula: F-statistic = Between-group variance / Within-group variance
    - With only 1 measurement per sample → within-group variance = 0 → F-statistic = undefined
    - We need **n ≥ 3 replicates per sample** to calculate within-group variance

    #### Option 2: Non-Parametric Tests (e.g., Kruskal-Wallis)

    **Requirements:**

    - Ordinal or continuous data ✓
    - Independent observations ✓
    - No normality assumption needed (work in both cases) ✓
    - Multiple observations per group for meaningful comparison ✗ **We don't have this**

    **Limitation:**

    - Same fundamental issue as ANOVA: requires comparing **between-group** variation
    - With only 1 measurement per sample → cannot assess within-group variation
    - Would produce results but they wouldn't be statistically meaningful

    #### Option 3: Descriptive Variability Analysis

    **What we can do:**

    - Assess **variation across samples** using descriptive statistics
    - Calculate **Coefficient of Variation (CV)** to measure relative variability
    - Evaluate **range** and **standard deviation**
    - Determine if parameters effectively differentiate samples

    **Why this works:**

    - Appropriate for **comparative screening** of different formulations
    - Each sample is unique (not replicates of same formulation)
    - Quantifies how much parameters vary across samples
    - Justifies performance-based ranking

    ### Our Selected Approach: Variability Analysis

    Since each sample represents a different formulation, we're conducting a **comparative study**
    rather than a hypothesis test about group differences. Our analysis will:

    1. **Quantify variability** for each parameter across samples
    2. **Identify** which parameters show meaningful variation
    3. **Validate** that differences exist to justify ranking
    4. **Prepare data** for multi-criteria performance scoring

    This approach aligns with our research goal: **identifying the best-performing formulation**
    from a set of unique candidates.
    """)
    return


@app.cell
def _(np, parameters_data, pd, stats):
    # Statistical Variability Analysis for each parameter
    # Since we have single measurements per sample (no replicates), we cannot perform
    # traditional ANOVA. Instead, we assess variation using coefficient of variation
    # and test if the observed variation is significant compared to a uniform distribution.

    _variability_results = []

    for _param_data in parameters_data:
        # Get non-NaN values
        _data = _param_data.values[~np.isnan(_param_data.values)]

        # Calculate basic statistics
        _mean = np.mean(_data)
        _std = np.std(_data, ddof=1)
        _cv = (_std / _mean * 100) if _mean != 0 else 0
        _range = np.max(_data) - np.min(_data)

        # Perform Chi-square test for variance
        # Tests if variance is significantly different from expected (H0: no variation)
        # Using degrees of freedom = n - 1
        _n = len(_data)
        _expected_mean = _mean
        _chi_square = np.sum((_data - _expected_mean) ** 2) / (_std**2) if _std > 0 else 0
        _df = _n - 1

        # Calculate p-value for chi-square test
        _p_value = 1 - stats.chi2.cdf(_chi_square, _df) if _std > 0 else 1.0

        # Interpretation based on CV and range
        if _cv > 20:
            _interpretation = "✅ High variation (CV > 20%)"
        elif _cv > 10:
            _interpretation = "✅ Moderate variation (CV 10-20%)"
        else:
            _interpretation = "⚠️ Low variation (CV < 10%)"

        _variability_results.append(
            {
                "Parameter": _param_data.name,
                "Mean": round(_mean, 2),
                "Std Dev": round(_std, 2),
                "CV (%)": round(_cv, 2),
                "Range": round(_range, 2),
                "Variation": _interpretation,
            }
        )

    variability_df = pd.DataFrame(_variability_results)
    # Display the variability analysis results table
    variability_df  # noqa: B018
    return (variability_df,)


@app.cell
def _(mo):
    mo.md("""
    ### Understanding the Variability Metrics

    **Coefficient of Variation (CV):**

    CV is calculated as: **CV = (Standard Deviation / Mean) x 100%**

    **Why CV is useful:**

    - **Scale-independent**: Allows comparison between parameters with different units
    - **Relative measure**: Shows variability relative to the mean value
    - **Interpretable**: Higher CV means greater relative differences between samples

    **CV Interpretation Thresholds:**

    - **CV < 10%**: Low variation → Samples are similar on this parameter
    - **CV 10-20%**: Moderate variation → Noticeable differences exist
    - **CV > 20%**: High variation → Substantial differences between samples

    **What This Means for Our Analysis:**

    - Parameters with **higher CV** are more useful for ranking (they differentiate samples better)
    - Parameters with **lower CV** show less sensitivity to formulation changes
    - The **range** shows the absolute spread (max - min) in original units
    """)
    return


@app.cell
def _(variability_df, mo):
    # Analyze variability results
    _high_var = variability_df[variability_df["Variation"].str.contains("High")]["Parameter"].tolist()
    _mod_var = variability_df[variability_df["Variation"].str.contains("Moderate")]["Parameter"].tolist()
    _low_var = variability_df[variability_df["Variation"].str.contains("Low")]["Parameter"].tolist()

    mo.md(f"""
    ### Statistical Variability Analysis Results

    **Summary:**

    - **High variation parameters** (CV > 20%): {len(_high_var)}
        {f"- {', '.join(_high_var)}" if _high_var else "- None"}

    - **Moderate variation parameters** (CV 10-20%): {len(_mod_var)}
        {f"- {', '.join(_mod_var)}" if _mod_var else "- None"}

    - **Low variation parameters** (CV < 10%): {len(_low_var)}
        {f"- {', '.join(_low_var)}" if _low_var else "- None"}

    **For Future Studies:**

    To enable traditional ANOVA, collect **n ≥ 3 replicates** per sample:

    - Allows calculation of within-sample variance
    - Enables statistical significance testing (F-test, p-values)

    ---

    **Step 3 Complete!** ✅

    **Next Step:**

    - Normalize the data for multi-criteria comparison
    - Create radar charts
    - Calculate performance scores
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 4. Data Normalization for Multi-Criteria Analysis

    To compare samples across different parameters with different units and scales,
    we need to **normalize** the data to a common scale [0, 1].

    **Why Normalize?**

    - Parameters have different units (%, kJ/g, J/g·K, s)
    - Parameters have different scales (e.g., Residue: 7-28%, Time1: 100-179s)
    - We need equal weighting for fair comparison

    **Min-Max Normalization Formula:**

    $$\\text{normalized} = \\frac{x - x_{\\text{min}}}{x_{\\text{max}} - x_{\\text{min}}}$$

    This transforms all values to the range [0, 1], where:
    - 0 = worst value in the dataset
    - 1 = best value in the dataset

    **Direction Adjustment:**

    Not all parameters follow "higher is better" logic:

    - **Residue (%)**: Lower is better → Use $(1 - \\text{normalized})$
    - **THR (kJ/g)**: Higher is better → Use $\\text{normalized}$
    - **HRC (J/g·K)**: Higher is better → Use $\\text{normalized}$
    - **Time1 (s)**: Lower is better → Use $(1 - \\text{normalized})$

    After adjustment, **1.0 always means "best"** and **0.0 always means "worst"** for all parameters.
    """)
    return


@app.cell
def _(mo, np, parameters_data, pd, sample_names):
    # Create normalization function
    def normalize_parameter(values, lower_is_better=False):
        """
        Normalize parameter values to [0, 1] range.

        Arguments:
            values: numpy array of values
            lower_is_better: If True, invert normalized values (1 - normalized)

        Returns:
            Normalized values where 1.0 = best, 0.0 = worst

        """
        # Remove NaN values for min/max calculation
        valid_vals = values[~np.isnan(values)]

        if len(valid_vals) == 0:
            return values  # Return as-is if no valid data

        min_val = np.min(valid_vals)
        max_val = np.max(valid_vals)

        # Avoid division by zero
        if max_val == min_val:
            return np.ones_like(values)

        # Min-max normalization
        normalized = (values - min_val) / (max_val - min_val)

        # Invert if lower is better
        if lower_is_better:
            normalized = 1.0 - normalized

        return normalized

    # Define which parameters should be inverted (lower is better)
    param_directions = {
        "Residue": True,  # Lower residue = better combustion efficiency
        "THR": False,  # Higher THR = more energy release
        "HRC": False,  # Higher HRC = more intense combustion
        "Time1": True,  # Lower time = faster ignition
    }

    # Create normalized data dictionary
    _norm_data = {"Sample": sample_names}

    # Store original and normalized values
    _original_data = {"Sample": sample_names}

    for _param_data in parameters_data:
        _param_name = _param_data.name
        _lower_is_better = param_directions.get(_param_name, False)

        # Store original values
        _original_data[_param_name] = _param_data.values

        # Normalize
        _normalized = normalize_parameter(_param_data.values, lower_is_better=_lower_is_better)
        _norm_data[f"{_param_name}_norm"] = _normalized

    # Create DataFrames
    original_df = pd.DataFrame(_original_data)
    normalized_df = pd.DataFrame(_norm_data)

    # Combine original and normalized for display - interleave columns
    combined_df = pd.DataFrame({"Sample": sample_names})
    for _param_data in parameters_data:
        _param_name = _param_data.name
        # Add original value first, then normalized value next to it
        combined_df[_param_name] = original_df[_param_name]
        combined_df[f"{_param_name}_norm"] = normalized_df[f"{_param_name}_norm"]

    # Round to 3 decimal places for display
    combined_df = combined_df.round(3)

    # Show combined DataFrame
    _display_table = mo.ui.table(
        data=combined_df,
        pagination=False,
        show_column_summaries=False,
    )
    _display_table  # noqa: B018
    return combined_df, normalize_parameter, normalized_df, original_df, param_directions


@app.cell
def _(mo):
    mo.md("""
    ### Normalized Values Explanation

    The table above shows both **original** and **normalized values** (columns ending with `_norm`).

    **Interpretation Guide:**

    For normalized values (0.0 to 1.0):

    - **1.00** = Best performance for this parameter
    - **0.50** = Average performance
    - **0.00** = Worst performance for this parameter

    **Example:**

    - Sample with `Residue_norm = 1.00` has the **lowest residue** (best efficiency)
    - Sample with `THR_norm = 1.00` has the **highest total heat release** (best energy)
    - Sample with `Time1_norm = 1.00` has the **shortest ignition time** (fastest)

    All normalized values are now **comparable** across different parameters!
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---

    **Step 4 Complete!** ✅

    We've successfully normalized all parameters to a [0, 1] scale with proper direction adjustment.

    **Next Step:**

    - Create radar charts for visual comparison
    - Calculate overall performance scores
    - Rank samples
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 5. Radar Chart Visualization

    Radar charts (also called spider charts or star plots) allow us to visualize
    multiple parameters simultaneously for each sample.

    **How to Read a Radar Chart:**

    - Each axis represents one parameter
    - Distance from center = normalized value (0 at center, 1 at edge)
    - Larger area = better overall performance
    - Compare shapes to identify strengths/weaknesses

    **Our Parameters:**

    - **Residue**: Lower residue (outer edge) = better
    - **THR**: Higher heat release (outer edge) = better
    - **HRC**: Higher capacity (outer edge) = better
    - **Time1**: Faster ignition (outer edge) = better

    All axes point outward for "better" performance after normalization.
    """)
    return


@app.cell
def _(go, normalized_df, parameters_data, sample_names):
    # Create radar chart for all samples
    fig_radar = go.Figure()

    # Get parameter names for the radar axes
    _param_names = [p.name for p in parameters_data]

    # Add a trace for each sample
    for _sample_idx, _sample in enumerate(sample_names):
        # Get normalized values for this sample
        _values = [normalized_df[f"{param}_norm"].iloc[_sample_idx] for param in _param_names]

        # Close the radar chart by repeating the first value
        _radar_values = [*_values, _values[0]]
        _radar_params = [*_param_names, _param_names[0]]

        fig_radar.add_trace(
            go.Scatterpolar(
                r=_radar_values,
                theta=_radar_params,
                fill="toself",
                name=_sample,
                opacity=0.6,
            )
        )

    fig_radar.update_layout(
        polar={
            "radialaxis": {
                "visible": True,
                "range": [0, 1],
                "showline": True,
                "linewidth": 1,
                "gridcolor": "lightgray",
            }
        },
        showlegend=True,
        title="Multi-Parameter Performance Comparison (Normalized Values)",
        height=600,
        legend={"orientation": "v", "yanchor": "middle", "y": 0.5, "xanchor": "left", "x": 1.05},
    )

    # Display the radar chart
    fig_radar  # noqa: B018
    return (fig_radar,)


@app.cell
def _(mo):
    mo.md("""
    ### Radar Chart Interpretation

    **What to Look For:**

    - **Samples with larger areas** have better overall performance
    - **Balanced shapes** (similar radius on all axes) indicate consistent performance across all parameters
    - **Elongated shapes** indicate strength in specific parameters but weakness in others
    - **Compare individual axes** to see which parameter differentiates samples

    **Visual Analysis Tips:**

    1. Identify the sample(s) with the **largest enclosed area**
    2. Check for samples that excel in **multiple parameters simultaneously**
    3. Look for trade-offs (e.g., high THR but high residue)

    ---

    **Step 5 Complete!** ✅

    **Next Step (Step 6):**

    - Calculate performance scores (sum of normalized values)
    - Rank all samples
    - Identify the best performers
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 6. Performance Scoring and Ranking

    To objectively rank the samples, we calculate a **Performance Score** by summing
    all normalized parameter values for each sample.

    **Performance Score Formula:**

    $$\\text{Performance Score} = \\sum_{i=1}^{n} \\text{Normalized}_i$$

    Where $n$ is the number of parameters (in our case, 4).

    **Score Interpretation:**

    - **Maximum possible score**: 4.00 (perfect score on all parameters)
    - **Minimum possible score**: 0.00 (worst score on all parameters)
    - **Higher score** = better overall performance

    This approach gives **equal weight** to all parameters. For applications where certain
    parameters are more important, weighted scoring could be used instead.
    """)
    return


@app.cell
def _(mo, normalized_df, parameters_data, pd, sample_names):
    # Calculate performance scores
    _param_names = [p.name for p in parameters_data]

    # Sum normalized values for each sample
    _scores = []
    for _sample_idx in range(len(sample_names)):
        _score = sum(normalized_df[f"{param}_norm"].iloc[_sample_idx] for param in _param_names)
        _scores.append(_score)

    # Create performance ranking DataFrame
    performance_df = pd.DataFrame(
        {
            "Sample": sample_names,
            "Performance Score": _scores,
        }
    )

    # Add individual normalized values for reference
    for _param in _param_names:
        performance_df[f"{_param}_norm"] = normalized_df[f"{_param}_norm"].values

    # Sort by performance score (descending)
    performance_df = performance_df.sort_values("Performance Score", ascending=False).reset_index(drop=True)

    # Add rank column
    performance_df.insert(0, "Rank", range(1, len(performance_df) + 1))

    # Round for display
    performance_df = performance_df.round(3)
    # Show performance ranking table
    _display_table = mo.ui.table(
        data=performance_df,
        pagination=False,
        show_column_summaries=False,
    )
    _display_table  # noqa: B018
    return (performance_df,)


@app.cell
def _(mo, performance_df):
    # Identify top performers
    _top_sample = performance_df.iloc[0]["Sample"]
    _top_score = performance_df.iloc[0]["Performance Score"]
    _top_3 = performance_df.head(3)

    mo.md(f"""
    ### Performance Ranking Results

    **🏆 Best Performing Sample: {_top_sample}**

    - **Performance Score:** {_top_score:.3f} / 4.000
    - **Rank:** #1 out of {len(performance_df)} samples

    **Top 3 Samples:**

    1. {_top_3.iloc[0]["Sample"]} - Score: {_top_3.iloc[0]["Performance Score"]:.3f}
    2. {_top_3.iloc[1]["Sample"]} - Score: {_top_3.iloc[1]["Performance Score"]:.3f}
    3. {_top_3.iloc[2]["Sample"]} - Score: {_top_3.iloc[2]["Performance Score"]:.3f}

    **Key Insights:**

    The ranking is based on the sum of normalized values across all four parameters:

    - Residue (normalized, lower is better)
    - THR (normalized, higher is better)
    - HRC (normalized, higher is better)
    - Time1 (normalized, lower is better)

    Samples at the top of the ranking demonstrate the best **overall balance** across
    combustion efficiency, energy release, heat capacity, and ignition speed.

    ---

    **Step 6 Complete!** ✅
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Summary and Conclusions

    ### Key Findings

    ✅ **Analysis Completed**: Descriptive statistics → Normality testing → Variability analysis → Normalization → Performance ranking

    ✅ **Best Performing Samples Identified**: Objective ranking based on balanced performance across all parameters

    ✅ **Statistical Approach**: Variability analysis using Coefficient of Variation (CV) - appropriate for single measurements per unique formulation

    ### Important Methodological Note

    **Current Study Design:**

    - Single measurement per sample (no replicates)
    - Each sample = unique formulation (comparative screening)
    - **Cannot perform ANOVA** (requires within-group variance from replicates)
    - CV-based variability analysis confirms meaningful differences exist

    **For Future Studies:**

    To enable traditional statistical inference (e.g., ANOVA, significance testing):

    - Collect **n ≥ 3 replicates** per sample
    - This allows calculation of within-group variance and F-statistics

    """)
    return


if __name__ == "__main__":
    app.run()
