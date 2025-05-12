import pandas as pd

def present_analysis_tables(group_results: dict[str,pd.DataFrame]) -> dict:
    """
    Organizes analysis results into three tables (action, response, scenario)
    for each grouping level.

    Parameters
    ----------
    group_results : dict[str, pd.DataFrame]
        Dictionary of grouped analysis results, keyed by group column name.

    Returns
    -------
    dict[str, dict[str, pd.DataFrame]]
        Nested dictionary with outer keys as title-cased group names,
        and inner keys: 'action', 'response', 'scenario'.
    """
    final_dfs = {}

    for group, result_df in group_results.items():
        group_name = group.replace('_', ' ').title()
        final_dfs[group_name] = {}

        # Match columns dynamically by keywords
        def match_columns(keywords):
            return [col for col in result_df.columns if any(k in col.lower() for k in keywords)]

        df1_cols = [group_name] + match_columns(['usefulness', 'actionability', 'duplicate', 'relevant', 'action hallucination', 'n_action'])
        df2_cols = [group_name] + match_columns(['num responses', 'reasoning quality', 'reasoning hallucination', 'n_response'])
        df3_cols = [group_name] + match_columns(['success', 'tree depth', 'num branches', 'n_scenario'])

        # Assign sub-dataframes
        final_dfs[group_name]['action'] = result_df[df1_cols].copy()
        final_dfs[group_name]['response'] = result_df[df2_cols].copy()
        final_dfs[group_name]['scenario'] = result_df[df3_cols].copy()

        # Rename n columns
        final_dfs[group_name]['action'].rename(columns={'n_action': 'Actions Evaluated'}, inplace=True)
        final_dfs[group_name]['response'].rename(columns={'n_response': 'Responses Evaluated'}, inplace=True)
        final_dfs[group_name]['scenario'].rename(columns={'n_scenario': 'Scenarios Evaluated'}, inplace=True)

        # Rename hallucination columns
        final_dfs[group_name]['action'].rename(columns={'Action Hallucination': 'Hallucination'}, inplace=True)
        final_dfs[group_name]['response'].rename(columns={'Reasoning Hallucination': 'Hallucination'}, inplace=True)

        # Reorder columns
        for key, label in [('action', 'Actions Evaluated'), ('response', 'Responses Evaluated'), ('scenario', 'Scenarios Evaluated')]:
            df = final_dfs[group_name][key]
            if label in df.columns:
                reordered = [group_name, label] + [col for col in df.columns if col not in [group_name, label]]
                final_dfs[group_name][key] = df[reordered]

        # Special case: drop scenario count for sheet-level grouping
        if group == 'scenario':
            final_dfs[group_name]['scenario'].drop(columns='Scenarios Evaluated', inplace=True, errors='ignore')

        # Drop Num Responses column if present
        final_dfs[group_name]['response'].drop(columns='Num Responses', inplace=True, errors='ignore')

    return final_dfs
