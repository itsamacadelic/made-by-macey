# engine.py: weighting + allocation logic for Macey Media Planner Pro


import pandas as pd


def allocate_budget(
    channels,
    weights,
    total_budget,
    cost_benchmarks=None,
    kpi_focus=None,
    affinity=None,
    affinity_weights=None
):
    """
    Allocate budget mindful of channel weights, cost efficiency (CPC/CPM), and audience affinity (demo, behavioral, contextual).
    affinity: dict of {affinity_type: {channel: score}}
    affinity_weights: dict of {affinity_type: weight} (e.g., {"demo": 0.4, "behavioral": 0.4, "contextual": 0.2})
    """
    allocation = {}
    # Combine base weights with affinity adjustments
    combined_weights = weights.copy()
    if affinity and affinity_weights:
        for channel in channels:
            aff_score = 0
            for aff_type, aff_map in affinity.items():
                aff_score += affinity_weights.get(aff_type, 0) * aff_map.get(channel, 1.0)
            combined_weights[channel] = weights.get(channel, 1.0) * aff_score
    total_weight = sum(combined_weights.values())
    for channel in channels:
        allocation[channel] = (combined_weights.get(channel, 0) / total_weight) * total_budget

    # If cost benchmarks and KPI focus are provided, adjust allocation
    if cost_benchmarks is not None and kpi_focus is not None:
        cost_metric = "CPM" if kpi_focus.lower() in ["reach", "impressions"] else "CPC"
        costs = {row["channel"]: row[cost_metric] for _, row in cost_benchmarks.iterrows()}
        efficiency = {ch: 1.0 / costs.get(ch, 1.0) for ch in channels}
        eff_weight_sum = sum(combined_weights[ch] * efficiency.get(ch, 1.0) for ch in channels)
        for channel in channels:
            eff_weight = combined_weights[channel] * efficiency.get(channel, 1.0)
            allocation[channel] = (eff_weight / eff_weight_sum) * total_budget

    return allocation
