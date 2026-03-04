import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def create_scatter_comparison(systolic_file="systolic_cache.json",
                              cannon_file="cannon_cache.json",
                              tick_width=1.2, spine_width=1.2,
                              label_fontsize=12, label_fontweight='normal'):
    # Load data
    with open(systolic_file, 'r') as f:
        systolic_data = json.load(f)
    with open(cannon_file, 'r') as f:
        cannon_data = json.load(f)

    # Use intersection of keys
    common_keys = sorted(set(systolic_data.keys()) & set(cannon_data.keys()))
    if not common_keys:
        raise RuntimeError("No common keys between the two JSON files.")

    # Extract latencies for common keys
    systolic_latencies = []
    cannon_latencies = []
    for key in common_keys:
        s_entry = systolic_data[key]
        c_entry = cannon_data[key]
        s = s_entry.get('latency') if isinstance(s_entry, dict) else None
        c = c_entry.get('latency') if isinstance(c_entry, dict) else None
        if s is None or c is None:
            continue
        systolic_latencies.append(float(s))
        cannon_latencies.append(float(c))

    systolic_latencies = np.array(systolic_latencies)
    cannon_latencies = np.array(cannon_latencies)

    if systolic_latencies.size == 0:
        raise RuntimeError("No valid latency pairs found to compare.")

    # Absolute statistics
    correlation = stats.pearsonr(systolic_latencies, cannon_latencies)
    mean_diff = np.mean(cannon_latencies - systolic_latencies)
    std_diff = np.std(cannon_latencies - systolic_latencies)
    rmse = np.sqrt(np.mean((cannon_latencies - systolic_latencies) ** 2))

    # Relative differences: (cannon - systolic) / systolic
    nonzero_mask = systolic_latencies != 0
    if not np.all(nonzero_mask):
        n_zero = np.sum(~nonzero_mask)
        print(f"Warning: {n_zero} entries have systolic latency == 0 and are excluded from relative stats.")

    rel_diffs = (cannon_latencies[nonzero_mask] - systolic_latencies[nonzero_mask]) / systolic_latencies[nonzero_mask]
    if rel_diffs.size == 0:
        raise RuntimeError("No relative differences could be computed (all systolic latencies are zero).")

    mean_rel = np.mean(rel_diffs)          # fraction
    mean_rel_pct = mean_rel * 100.0        # percent
    std_rel = np.std(rel_diffs)
    rmse_rel = np.sqrt(np.mean(rel_diffs ** 2))

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(systolic_latencies, cannon_latencies,
                         color='#1976D2', alpha=0.6, s=50, label='Data points')

    # Diagonal line
    min_val = min(systolic_latencies.min(), cannon_latencies.min())
    max_val = max(systolic_latencies.max(), cannon_latencies.max())
    ax.plot([min_val, max_val], [min_val, max_val],
            '--', color='gray', alpha=0.5, label='y = x')

    # Legend entry with average relative difference
    legend_label = f'Mean relative diff: {mean_rel_pct:.2f}%'
    # Add a proxy artist for the legend entry (so it appears alongside other entries)
    ax.scatter([], [], color='none', label=legend_label)  # invisible marker for legend text

    # Style the plot
    ax.set_xlabel('Systolic Latency', fontsize=label_fontsize, fontweight=label_fontweight)
    ax.set_ylabel('Cannon Latency', fontsize=label_fontsize, fontweight=label_fontweight)
    ax.tick_params(axis='both', which='major', width=tick_width, length=7)
    ax.tick_params(axis='both', which='minor', width=tick_width, length=4)
    for spine in ax.spines.values():
        spine.set_linewidth(spine_width)

    # # Place legend (frame with white background)
    # ax.legend(loc='upper left', frameon=True, framealpha=0.9)

    # Stats textbox (kept compact)
    stats_text = (
        f'Corr: {correlation[0]:.3f}\n'
        f'Mean diff: {mean_diff:.3f}\n'
        f'RMSE: {rmse:.3f}\n'
        f'Mean rel: {mean_rel_pct:.2f}%'
    )
    ax.text(0.05, 0.95, stats_text,
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.85),
            fontsize=9)

    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()

    # Save figure
    plt.savefig('latency_comparison_cannon-sys.pdf', bbox_inches='tight')
    plt.savefig('latency_comparison_cannon-sys.png', bbox_inches='tight')
    plt.close()

    # Print statistics
    print("\nLatency Comparison Statistics:")
    print("-" * 30)
    print(f"Correlation coefficient: {correlation[0]:.3f}")
    print(f"Correlation p-value: {correlation[1]:.3e}")
    print(f"Mean difference: {mean_diff:.3f}")
    print(f"Standard deviation of difference: {std_diff:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print()
    print("Relative statistics (relative = (cannon - systolic) / systolic):")
    print(f"Mean relative difference: {mean_rel:.6f} ({mean_rel_pct:.3f}%)")
    print(f"Std of relative differences: {std_rel:.6f}")
    print(f"Relative RMSE: {rmse_rel:.6f}")

if __name__ == "__main__":
    create_scatter_comparison()
