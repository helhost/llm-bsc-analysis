from scipy.stats import pearsonr
import pandas as pd

def calculate_correlation_with_p(
    df: pd.DataFrame,
    column1: str,
    column2: str,
    level: str = 'action'
):
    """
    Calculate the Pearson correlation and p-value between two columns,
    with optional aggregation at the 'action', 'response', or 'scenario' level.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the data.

    column1 : str
        First column for correlation.

    column2 : str
        Second column for correlation.

    level : str, optional (default='action')
        Level of aggregation: 'action', 'response', or 'scenario'.

    Returns
    -------
    tuple
        (correlation coefficient, p-value)
    """
    if level == 'action':
        # Use all rows as-is
        data = df[[column1, column2]].dropna()

    elif level == 'response':
        # Deduplicate by response_id
        if 'response_id' not in df.columns:
            raise ValueError("Column 'response_id' is required for response-level analysis.")
        data = df[['response_id', column1, column2]].drop_duplicates(subset='response_id').dropna()

    elif level == 'scenario':
        # Deduplicate by scenario
        if 'scenario' not in df.columns:
            raise ValueError("Column 'scenario' is required for scenario-level analysis.")
        data = df[['scenario', column1, column2]].drop_duplicates(subset='scenario').dropna()

    else:
        raise ValueError(f"Invalid level: '{level}'. Choose from 'action', 'response', or 'scenario'.")

    # Run correlation
    r, p = pearsonr(data[column1], data[column2])
    return r, p
