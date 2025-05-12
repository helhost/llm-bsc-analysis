import numpy as np
from scipy.stats import norm, t

def correlation_confidence_margin(r, n, confidence=0.95):
    """
    Calculate the margin of error for a Pearson correlation coefficient
    using Fisher's z transformation.

    Parameters:
    r (float): Pearson correlation coefficient.
    n (int): Sample size.
    confidence (float): Confidence level, e.g., 0.95 for 95% CI.

    Returns:
    float: Margin of error for the correlation coefficient.
    """
    if n <= 3:
        raise ValueError("Sample size must be greater than 3 for Fisher transformation.")

    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    z_crit = norm.ppf(1 - (1 - confidence) / 2)
    z_margin = z_crit * se
    r_margin = np.tanh(z + z_margin) - r

    return r_margin

def check_pvalue(p_value):
    """
    Check if the p-value indicates statistical significance.
    """
    return p_value < 0.05

def present_corr(p, r, r_margin):
    """
    Present the correlation results in a formatted string.
    """
    significance = "Statistically significant" if check_pvalue(p) else "Not statistically significant"
    return f"Correlation: {r:.3f} ± {r_margin:.3f}, p-value: {p:.2e} ({significance})"
