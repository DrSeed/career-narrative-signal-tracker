# Self-contained demo: simulate a year of career posts and track pillar balance.
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PILLARS = ["past_achievement", "current_work", "industry_commentary"]


def simulate_posts(n_weeks=52, seed=42):
    rng = np.random.default_rng(seed)
    # Simulate a scientist who starts achievement-heavy and drifts toward commentary.
    rows = []
    for week in range(n_weeks):
        t = week / (n_weeks - 1)
        base = np.array([
            0.6 * (1 - t) + 0.15,
            0.3,
            0.1 + 0.5 * t,
        ])
        noise = rng.normal(0, 0.08, size=3)
        weights = np.clip(base + noise, 0.01, None)
        weights = weights / weights.sum()
        rows.append([week] + list(weights))
    df = pd.DataFrame(rows, columns=["week"] + PILLARS)
    return df


def main():
    os.makedirs("figures", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    df = simulate_posts()

    # Rolling mean to smooth weekly noise.
    smooth = df[PILLARS].rolling(window=4, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(9, 5))
    colours = ["#2c7fb2", "#41ab5d", "#d94801"]
    ax.stackplot(df["week"], smooth.T.values, labels=PILLARS, colors=colours, alpha=0.85)
    ax.set_xlabel("Week of year")
    ax.set_ylabel("Pillar share (4-week rolling mean)")
    ax.set_title("Career Narrative Balance Over Time (simulated)")
    ax.set_ylim(0, 1)
    ax.legend(loc="upper center", ncol=3)
    fig.tight_layout()
    fig.savefig("figures/demo.png", dpi=120)

    dominant = df[PILLARS].idxmax(axis=1)
    summary = pd.DataFrame({
        "pillar": PILLARS,
        "mean_share": [df[p].mean() for p in PILLARS],
        "weeks_dominant": [int((dominant == p).sum()) for p in PILLARS],
    })
    summary.to_csv("results/summary.csv", index=False)

    print("Wrote figures/demo.png and results/summary.csv")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
