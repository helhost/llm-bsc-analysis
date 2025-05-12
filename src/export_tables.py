import os

def export_latex_tables(final_dfs, out_path):
    """
    Export a nested dictionary of DataFrames to LaTeX files, with one subdirectory per group.

    Parameters
    ----------
    final_dfs : dict
        Nested dictionary with structure final_dfs[group_name][level] = DataFrame.

    out_path : str
        Path to the base output directory where all LaTeX files will be saved.
    """

    def escape_percent(s):
        if isinstance(s, str):
            return s.replace('%', r'\%')
        return s
    
    def escape_percent_in_df(df):
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].map(escape_percent)
        return df

    os.makedirs(out_path, exist_ok=True)

    for group_name, dfs in final_dfs.items():
        group_dir = os.path.join(out_path, group_name)
        os.makedirs(group_dir, exist_ok=True)

        for level, df in dfs.items():
            file_path = os.path.join(group_dir, f"{level}.tex")

            df = escape_percent_in_df(df)
            df.to_latex(
                file_path,
                index=False,
                escape=False,
                column_format='l' + 'r' * (len(df.columns) - 1)
            )
