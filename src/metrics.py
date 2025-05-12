import pandas as pd
import numpy as np
from scipy import stats
from .filter import filter_data_for_analysis

def analyze_grouped_metric(
    df: pd.DataFrame,
    group_col: str,
    metric_col: str,
    analysis_level: str,
    binary_condition=None,
    confidence: float=0.95,
    special_formatting=False
):
    """
    Analyze and summarize a metric by group, with optional confidence intervals.

    This function groups a DataFrame by a specified column and calculates the mean
    of a target metric. It optionally converts values to binary using a condition,
    calculates confidence intervals, and formats the results for presentation.

    Parameters
    ----------
    df : pandas.DataFrame
        The input DataFrame containing raw data.

    group_col : str
        Column name to group the data by (e.g., 'context-level', 'category').

    metric_col : str
        Name of the numeric column to be analyzed.

    analysis_level : str
        analysis_level of analysis: one of 'action', 'response', or 'scenario'.
        Used for determining deduplication and labeling in the output.

    binary_condition : callable, optional
        A function that returns True for "positive" binary values (e.g., `lambda x: x == 'Yes'`).
        If provided, metric values are converted to 0 or 1.

    confidence : float, default=0.95
        Confidence level for computing confidence intervals (only used when n > 1).

    special_formatting : str or bool, default=False
        Optional output formatting style. Supported:
        - 'percentage': Format mean as a percentage
        - 'zero-to-five': Show mean and CI in 0–5 scale with interval in parentheses

    Returns
    -------
    pandas.DataFrame
        A summarized DataFrame with the group, formatted metric value,
        and sample size (`n_{analysis_level}`).
    """

    # Step 1: Filter data to appropriate level
    filtered_df = filter_data_for_analysis(
        df,
        level=analysis_level,
        metric_col=metric_col,
        group_col=group_col
    )

    # Step 2: Handle binary metric transformation
    working_df = filtered_df.copy()
    if binary_condition is not None:
        working_df[metric_col] = working_df[metric_col].apply(
            lambda x: 1 if binary_condition(x) else 0
        )

    result_rows = []

    # Step 3: Compute stats by group
    for group_val, group_df in working_df.groupby(group_col):
        values = group_df[metric_col]
        n = len(values)
        mean = values.mean()
        ci_lower = ci_upper = None

        if n > 1:
            std = values.std(ddof=1)
            stderr = std / np.sqrt(n)
            t_val = stats.t.ppf((1 + confidence) / 2, df=n - 1)
            margin = t_val * stderr
            ci_lower = mean - margin
            ci_upper = mean + margin

        result_rows.append({
            'group': group_val,
            'mean': mean,
            'n': n,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper
        })

    # Step 4: Format values for presentation
    all_n_one_or_less = all(row['n'] <= 1 for row in result_rows)
    all_n_more_than_one = all(row['n'] > 1 for row in result_rows)

    formatted = []
    for row in result_rows:
        mean, ci_low, ci_high = row['mean'], row['ci_lower'], row['ci_upper']
        margin = (ci_high - ci_low) / 2 if ci_high is not None and ci_low is not None else None

        if all_n_one_or_less:
            display = f"{mean:.0f}"
        elif special_formatting == 'percentage':
            display = f"{mean * 100:.2f}%"
        elif special_formatting == 'zero-to-five' and all_n_more_than_one and group_col != 'scenario':
            display = f"\\( {mean:.2f} \\pm {margin:.2f} \\)"
        else:
            display = f"{mean:.2f}"

        formatted.append({
            group_col: row['group'],
            metric_col: display,
            f'n_{analysis_level}': row['n']
        })

    # Step 5: Create output DataFrame and format column names
    output_df = pd.DataFrame(formatted).sort_values(by=group_col).reset_index(drop=True)

    metric_label = f"Avg {metric_col.replace('_', ' ').title()}" if special_formatting != 'percentage' and not all_n_one_or_less else metric_col.replace('_', ' ').title()
    output_df.columns = [
        group_col,
        metric_label,
        f'n_{analysis_level}'
    ]

    return output_df
