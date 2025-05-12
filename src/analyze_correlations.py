from .corr_helper import (
    correlation_confidence_margin,
    present_corr,
)
from .correlations import calculate_correlation_with_p

def analyze_correlations(df):

    ret = ""

    # 1. reasoning quality vs usefulness (action level)
    c1, c2 = 'reasoning_quality', 'usefulness'
    r, p = calculate_correlation_with_p(
        df,
        column1=c1,
        column2=c2,
        level='action'
    )
    r_margin = correlation_confidence_margin(r, len(df), confidence=0.95)
    corr = present_corr(p, r, r_margin)
    ret += f"\n{c1} vs {c2}\n{corr}\n"

    # 2. Tree depth vs usefulness (action level)
    c1, c2 = 'tree_depth', 'usefulness'
    r, p = calculate_correlation_with_p(
        df,
        column1=c1,
        column2=c2,
        level='action'
    )
    r_margin = correlation_confidence_margin(r, len(df), confidence=0.95)
    corr = present_corr(p, r, r_margin)
    ret += f"\n{c1} vs {c2}\n{corr}\n"

    # 3. Content length vs usefulness (action level)
    c1, c2 = 'concatenated_text_from_root_length', 'usefulness'
    r, p = calculate_correlation_with_p(
        df,
        column1=c1,
        column2=c2,
        level='action'
    )
    r_margin = correlation_confidence_margin(r, len(df), confidence=0.95)
    corr = present_corr(p, r, r_margin)
    ret += f"\n{c1} vs {c2}\n{corr}\n"

    # 4. Reasoning Hallucination vs usefulness (action level)
    c1, c2 = 'reasoning_hallucination', 'usefulness'
    r, p = calculate_correlation_with_p(
        df[[c1, c2]].assign(reasoning_hallucination=df[c1].map({'Y': 1, 'N': 0})),
        column1=c1,
        column2=c2,
        level='action'
    )
    r_margin = correlation_confidence_margin(r, len(df), confidence=0.95)
    corr = present_corr(p, r, r_margin)
    ret += f"\n{c1} vs {c2}\n{corr}\n"
    

    return ret