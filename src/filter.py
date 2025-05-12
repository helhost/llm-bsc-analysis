import pandas as pd

def filter_data_for_analysis(
    df: pd.DataFrame,
    level: str,
    metric_col: str,
    group_col: str,
) -> pd.DataFrame:
    """
    Filters and prepares a DataFrame for analysis at a specified level of granularity.

    Depending on the analysis level ('action', 'response', or 'scenario'),
    the function selects only the relevant columns and deduplicates the data
    where appropriate.

    Parameters
    ----------
    df : pandas.DataFrame
        The original DataFrame containing all raw data.

    level : str
        The level of analysis. Must be one of:
        - 'action': analyze individual actions
        - 'response': analyze grouped responses
        - 'scenario': analyze high-level scenarios (worksheets)

    metric_col : str
        Name of the column containing the metric to analyze.

    group_col : str
        Column name to group data by (e.g., 'context-level', 'category').

    Returns
    -------
    pandas.DataFrame
        A filtered and optionally deduplicated DataFrame containing only the
        relevant columns for the specified analysis level.

    Raises
    ------
    ValueError
        If the provided `level` is not one of 'action', 'response', or 'scenario'.
    """
    if level == 'action':
        # Action-level: no deduplication needed; each action is distinct
        required_cols = ['response_id', 'action_name']
        if group_col not in required_cols:
            required_cols.append(group_col)
        if metric_col not in required_cols:
            required_cols.append(metric_col)
        return df[required_cols]

    elif level == 'response':
        # Response-level: deduplicate by response_id
        required_cols = ['response_id']
        if group_col not in required_cols:
            required_cols.append(group_col)
        if metric_col not in required_cols:
            required_cols.append(metric_col)
        return df[required_cols].drop_duplicates()

    elif level == 'scenario':
        required_cols = ['scenario']
        if group_col not in required_cols:
            required_cols.append(group_col)
        if metric_col not in required_cols:
            required_cols.append(metric_col)
        return df[required_cols].drop_duplicates()

    else:
        raise ValueError(f"Invalid analysis level: '{level}'. Must be 'action', 'response', or 'scenario'.")
