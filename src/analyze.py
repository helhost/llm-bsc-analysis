from .metrics import analyze_grouped_metric
import pandas as pd

def analyze_data(df: pd.DataFrame) -> dict:
    """
    Run grouped metric analyses on the input DataFrame across multiple levels
    and return a dictionary of summary DataFrames grouped by the specified dimensions.

    Parameters
    ----------
    df : pd.DataFrame
        The original DataFrame with flattened action/response/scenario data.

    Returns
    -------
    dict[str, pd.DataFrame]
        A dictionary where each key is a group column (e.g., 'context-level'),
        and the value is a summary DataFrame of aggregated metrics.
    """
    group_cols = ['context-level', 'category', 'scenario']
    metrics = [
        ('usefulness',              'action',   None,               'zero-to-five'),
        ('actionability',           'action',   None,               'zero-to-five'), 
        ('duplicate',               'action',   lambda x: x == 'Y', 'percentage'),
        ('relevant',                'action',   lambda x: x == 'Y', 'percentage'),
        ('action_hallucination',    'action',   lambda x: x == 'Y', 'percentage'),
        ('reasoning_quality',       'response', None,               'zero-to-five'), 
        ('reasoning_hallucination', 'response', lambda x: x == 'Y', 'percentage'),
        ('success',                 'scenario', lambda x: x == 1,   'percentage'), 
        ('tree_depth',              'scenario', None,               None), 
        ('num_branches',            'scenario', None,               None), 
        ('num_responses',           'scenario', None,               None),
    ]

    results_by_group = {}

    for group_col in group_cols:
        combined_df = None

        for metric_col, level, condition, format_ in metrics:
            result_df = analyze_grouped_metric(
                df,
                group_col=group_col,
                metric_col=metric_col,
                analysis_level=level,
                binary_condition=condition,
                special_formatting=format_,
            )

            if combined_df is None:
                combined_df = result_df
            else:
                for col in result_df.columns:
                    if col in combined_df.columns and col != group_col:
                        result_df = result_df.drop(columns=col)
                combined_df = pd.merge(combined_df, result_df, on=group_col)

        # rename the columns to change _ for spcae and title case
        combined_df.columns = [col.replace('_', ' ').title() for col in combined_df.columns]

        results_by_group[group_col] = combined_df

    return results_by_group
