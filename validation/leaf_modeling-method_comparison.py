import json
import matplotlib.pyplot as plt
import numpy as np

# Load the timeloop_cache.json file
timeloop_cache_file = "timeloop_cache_detailed.json"
with open(timeloop_cache_file, "r") as file:
    timeloop_data = json.load(file)

# Initialize a new dictionary to store the filtered and processed data
processed_data = {}
keys_found = 0
# Process each entry in the JSON data
for key, value in timeloop_data.items():
    # Split the key into its components
    key_parts = key.split("_")

    # Ensure the key has at least 6 parts (val1, val2, val3, val4, val5, val6)
    if len(key_parts) >= 6:
        val1, val2, val3, val4, val5, val6 = key_parts[:6]

        # Check if val5 equals "imec-gemm"
        if val4 == "imec-gemm":
            keys_found+=1
            # Create a new key with only val1, val2, val3
            new_key = f"{val1}_{val2}_{val3}"
            # print(new_key)
            # Add the entry to the processed data with the new key
            processed_data[new_key] = value

# Write the processed data to a new JSON file
output_file = "processed_timeloop_cache.json"
with open(output_file, "w") as file:
    json.dump(processed_data, file, indent=4)

print(f"Processed data has been written to {output_file} Key count: {keys_found}")

############# Maintain all data keys that are mutual in both caches ################
# Load the cannon_cache.json file
cannon_cache_file = "cannon_cache.json"
with open(cannon_cache_file, "r") as file:
    cannon_data = json.load(file)

# Load the processed_timeloop_cache.json file
processed_timeloop_file = "processed_timeloop_cache.json"
with open(processed_timeloop_file, "r") as file:
    timeloop_data = json.load(file)

# Get the keys from cannon_cache.json
cannon_keys = set(cannon_data.keys())

# Print total number of keys before preprocessing
print(f"Total keys in cannon_cache before preprocessing: {len(cannon_keys)}")

# Filter timeloop_data to include only keys present in cannon_data
filtered_timeloop_data = {key: value for key, value in timeloop_data.items() if key in cannon_keys}

# Filter cannon_data to include only keys present in both datasets
filtered_cannon_data = {key: value for key, value in cannon_data.items() if key in filtered_timeloop_data}

#Scale SIM
scale_sim_cycles = [34949,41939,31959,44939,44939,47939,52429,50939,31151,40439,39949,38939,37439,41939,121471,106287,111887,111859,100715,102491,105503,113273,102801,111887,108671,178037,191839,146145,134271,151055]
scale_sim_latency = [cycle / 30 for cycle in scale_sim_cycles]
all_keys = filtered_cannon_data.keys()
# Assuming you have a scale_sim_data dictionary where the keys correspond to the data points:
scale_sim_data = {key: value for key, value in zip(all_keys, scale_sim_latency)}
# Filter scale_sim_data to include only keys present in filtered_timeloop_data (or cannon_keys)
filtered_scale_sim_data = {key: value for key, value in scale_sim_data.items() if key in filtered_timeloop_data}
print("================= Systolic SIM ==================")
print(filtered_cannon_data)
print("================= SCALE SIM ==================")
print(filtered_scale_sim_data)
# Print total number of keys after preprocessing
print(f"Total keys in cannon_cache after preprocessing: {len(filtered_cannon_data)}")

# Create new filtered JSON files 
filtered_cannon_file = "filtered_cannon_cache.json"
filtered_timeloop_file = "filtered_timeloop_cache.json"

with open(filtered_cannon_file, "w") as file:
    json.dump(filtered_cannon_data, file, indent=4)

with open(filtered_timeloop_file, "w") as file:
    json.dump(filtered_timeloop_data, file, indent=4)

print(f"Filtered data written to {filtered_cannon_file} and {filtered_timeloop_file}")

################ DATA ANALYSIS ###########################

# Load the filtered JSON files
with open(filtered_cannon_file, 'r') as file:
    cannon_cache = json.load(file)

with open(filtered_timeloop_file, 'r') as file:
    processed_timeloop_cache = json.load(file)

# Step 1: Data manipulation
# Process the processed_timeloop_cache.json data
processed_data = {}
for key, values in processed_timeloop_cache.items():
    # Convert energy from pJ to uJ
    energy_uJ = values['energy'] * 1e6  # Convert from pJ to uJ
    # Calculate latency by dividing cycles by 30
    latency = values['cycles'] / 30
    # latency = values['latency'] * 1e9
    processed_data[key] = {'energy': energy_uJ, 'latency': latency}

# Step 2: Calculate the differences between matching keys
energy_rel_diff = []
latency_rel_diff = []
scale_sim_latency_rel_diff = []

for key in cannon_cache:
    if key in processed_data:
        # Extract values from both datasets
        cannon_energy = cannon_cache[key]['energy']
        cannon_latency = cannon_cache[key]['latency']
        
        processed_energy = processed_data[key]['energy']
        processed_latency = processed_data[key]['latency']
        scale_sim_latency = filtered_scale_sim_data[key]
        
        # Compute the absolute differences
        energy_diff = abs(processed_energy - cannon_energy)
        latency_diff = abs(processed_latency - cannon_latency)

        scale_latency_diff = abs(scale_sim_latency - cannon_latency)

        # Compute the relative differences (normalized differences)
        energy_rel_diff.append(energy_diff / cannon_energy * 100)  # Relative difference in percentage
        latency_rel_diff.append(latency_diff / cannon_latency * 100)  # Relative difference in percentage

        scale_sim_latency_rel_diff.append(scale_latency_diff / cannon_latency * 100)  # Relative difference in percentage


# Step 3: Calculate avg diff and save the plots as files
avg_energy_rel_diff = np.mean(energy_rel_diff)
avg_latency_rel_diff = np.mean(latency_rel_diff)
avg_scale_sim_latency_rel_diff = np.mean(scale_sim_latency_rel_diff)

plt.rcParams.update({
    "font.size": 16,        # Increase font size globally
    "axes.linewidth": 1.3,
    "xtick.major.width": 2,  # Thicker major x-axis ticks
    "ytick.major.width": 2,  # Thicker major y-axis ticks
    "xtick.minor.width": 1.5,  # Thicker minor x-axis ticks
    "ytick.minor.width": 1.5,  # Thicker minor y-axis ticks
    "xtick.major.size": 6,   # Longer major x-axis ticks
    "ytick.major.size": 6,   # Longer major y-axis ticks
    "xtick.minor.size": 4,   # Longer minor x-axis ticks
    "ytick.minor.size": 4,    # Longer minor y-axis ticks
    "axes.titlesize": 18,   # Bigger title
    "axes.labelsize": 16,   # Bigger axis labels
    "xtick.labelsize": 14,  # Bigger x-tick labels
    "ytick.labelsize": 14,  # Bigger y-tick labels
    "legend.fontsize": 14,  # Bigger legend text
    "lines.linewidth": 2.5, # Thicker lines
    "lines.markersize": 8   # Bigger markers
})

# # Difference Plot (Step 2)
plt.figure(figsize=(5.7, 8), dpi=300)
plt.subplot(1, 2, 1)
plt.scatter(range(len(energy_rel_diff)), energy_rel_diff, c='b', label='Energy Difference (uJ)')
plt.axhline(0, color='r', linestyle='--', linewidth=3, label='Zero Line')
plt.title('Energy Difference')
plt.xlabel('Simulation Run')
plt.ylabel('Energy Relative Difference (%)')
plt.legend(title=f'Avg Energy Relative Diff: {avg_energy_rel_diff:.2f}%')

plt.subplot(1, 2, 2)
plt.scatter(range(len(latency_rel_diff )), latency_rel_diff, c='g', label='Latency Difference')
plt.axhline(0, color='r', linestyle='--', linewidth=3, label='Zero Line')
plt.title('Latency Difference')
plt.xlabel('Simulation Run')
plt.ylabel('Latency Relative Difference (%)')
plt.legend(title=f'Avg Latency Relative Diff: {avg_latency_rel_diff:.2f}%')

plt.tight_layout()
# Save the difference plot as a file
plt.savefig('difference_plot_timeloop.png')
plt.close()  # Close the plot to avoid overlap with the next one

# Scatter Plot (Step 3)
# Energy comparison scatter plot
plt.figure(figsize=(5.7, 8), dpi=300)
plt.subplot(2, 1, 1)
plt.scatter([cannon_cache[key]['energy'] for key in cannon_cache], [processed_data[key]['energy'] for key in cannon_cache if key in processed_data], color='b', s=50)
plt.plot([min(cannon_cache[key]['energy'] for key in cannon_cache), max(cannon_cache[key]['energy'] for key in cannon_cache)], 
         [min(cannon_cache[key]['energy'] for key in cannon_cache), max(cannon_cache[key]['energy'] for key in cannon_cache)], 
         color='r', linestyle='--')  # Line where values match
plt.title('Energy Comparison (Roofline vs TL)')
plt.xlabel('Energy (Roofline Model) [uJ]')
plt.ylabel('Energy (Timeloop) [uJ]')
plt.legend(title=f'Avg Energy Relative Diff: {avg_energy_rel_diff:.2f}%')

# Latency comparison scatter plot
plt.subplot(2, 1, 2)
plt.scatter([cannon_cache[key]['latency'] for key in cannon_cache], [processed_data[key]['latency'] for key in cannon_cache if key in processed_data], color='g', s=50)
plt.plot([min(cannon_cache[key]['latency'] for key in cannon_cache), max(cannon_cache[key]['latency'] for key in cannon_cache)], 
         [min(cannon_cache[key]['latency'] for key in cannon_cache), max(cannon_cache[key]['latency'] for key in cannon_cache)], 
         color='r', linestyle='--')  # Line where values match
plt.title('Latency Comparison (Roofline vs TL)')
plt.xlabel('Latency (Roofline Model) [ns]')
plt.ylabel('Latency (Systolic) [ns]')
plt.legend(title=f'Avg Latency Rel Diff: {avg_latency_rel_diff:.2f}%')

plt.tight_layout()
# Save the scatter plot as a file
plt.savefig('scatter_plot_roofline-vs-cannon.png')
plt.close()  # Close the plot
###### SCALE SIM

# Difference Plot (Step 2)
# plt.figure(figsize=(10, 6), dpi=300)
# plt.subplot(1, 2, 1)
# plt.scatter(range(len(energy_rel_diff)), energy_rel_diff, c='b', label='Energy Difference (uJ)')
# plt.axhline(0, color='r', linestyle='--', linewidth=3, label='Zero Line')
# # plt.title('Energy Difference (Systolic vs Timeloop)')
# plt.xlabel('Simulation Run')
# plt.ylabel('Energy Relative Difference (%)')
# plt.legend(title=f'Avg Energy Relative Diff: {avg_energy_rel_diff:.2f}%')

# plt.subplot(1, 2, 2)
# plt.scatter(range(len(scale_sim_latency_rel_diff )), scale_sim_latency_rel_diff, c='g', label='Latency Difference')
# plt.axhline(0, color='r', linestyle='--', linewidth=3, label='Zero Line')
# # plt.title('Latency Difference (Systolic vs S-S)')
# plt.xlabel('Simulation Run')
# plt.ylabel('Latency Relative Difference (%)')
# plt.legend(title=f'Avg Latency Relative Diff: {avg_scale_sim_latency_rel_diff:.2f}%')

# plt.tight_layout()
# # Save the difference plot as a file
# plt.savefig('difference_plot_scale-sim.png')
# plt.close()  # Close the plot to avoid overlap with the next one

# ### SCALE-SIM
# # Energy comparison scatter plot
# plt.figure(figsize=(5.7, 8), dpi=300)
# plt.subplot(2, 1, 1)
# plt.scatter([cannon_cache[key]['energy'] for key in cannon_cache], [processed_data[key]['energy'] for key in cannon_cache if key in processed_data], color='b', s=50)
# plt.plot([min(cannon_cache[key]['energy'] for key in cannon_cache), max(cannon_cache[key]['energy'] for key in cannon_cache)], 
#          [min(cannon_cache[key]['energy'] for key in cannon_cache), max(cannon_cache[key]['energy'] for key in cannon_cache)], 
#          color='r', linestyle='--')  # Line where values match
# plt.title('Energy Comparison (Systolic vs TL)')
# plt.xlabel('Energy (Systolic Model) [uJ]')
# plt.ylabel('Energy (Timeloop) [uJ]')
# plt.legend(title=f'Avg Energy Relative Diff: {avg_energy_rel_diff:.2f}%')

# # Latency comparison scatter plot
# plt.subplot(2, 1, 2)
# plt.scatter([cannon_cache[key]['latency'] for key in cannon_cache], [filtered_scale_sim_data[key] for key in cannon_cache if key in filtered_scale_sim_data], color='g', s=50)
# plt.plot([min(cannon_cache[key]['latency'] for key in cannon_cache), max(cannon_cache[key]['latency'] for key in cannon_cache)], 
#          [min(cannon_cache[key]['latency'] for key in cannon_cache), max(cannon_cache[key]['latency'] for key in cannon_cache)], 
#          color='r', linestyle='--')  # Line where values match
# plt.title('Latency Comparison (Systolic vs S-S)')
# plt.xlabel('Latency (Systolic Model) [ns]')
# plt.ylabel('Latency (SCALE-SIM) [ns]')
# plt.legend(title=f'Avg Latency Rel Diff: {avg_scale_sim_latency_rel_diff:.2f}%')


# plt.tight_layout()
# # Save the scatter plot as a file
# plt.savefig('scatter_plot_scale-sim.png')
# plt.close()  # Close the plot

################ CANNON VS TIMELOOP COMPARISON ###########################

# Create a comprehensive cannon vs timeloop comparison plot
plt.figure(figsize=(12, 10), dpi=300)

# Energy comparison scatter plot
plt.subplot(2, 2, 1)
cannon_energies = [cannon_cache[key]['energy'] for key in cannon_cache]
timeloop_energies = [processed_data[key]['energy'] for key in cannon_cache if key in processed_data]
plt.scatter(cannon_energies, timeloop_energies, color='b', s=50, alpha=0.7)
min_energy = min(min(cannon_energies), min(timeloop_energies))
max_energy = max(max(cannon_energies), max(timeloop_energies))
plt.plot([min_energy, max_energy], [min_energy, max_energy], color='r', linestyle='--', linewidth=2)
plt.title('Energy Comparison (Cannon vs Timeloop)')
plt.xlabel('Energy (Cannon) [uJ]')
plt.ylabel('Energy (Timeloop) [uJ]')
plt.grid(True, alpha=0.3)

# Latency comparison scatter plot
plt.subplot(2, 2, 2)
cannon_latencies = [cannon_cache[key]['latency'] for key in cannon_cache]
timeloop_latencies = [processed_data[key]['latency'] for key in cannon_cache if key in processed_data]
plt.scatter(cannon_latencies, timeloop_latencies, color='g', s=50, alpha=0.7)
min_latency = min(min(cannon_latencies), min(timeloop_latencies))
max_latency = max(max(cannon_latencies), max(timeloop_latencies))
plt.plot([min_latency, max_latency], [min_latency, max_latency], color='r', linestyle='--', linewidth=2)
plt.title('Latency Comparison (Cannon vs Timeloop)')
plt.xlabel('Latency (Cannon) [ns]')
plt.ylabel('Latency (Timeloop) [ns]')
plt.grid(True, alpha=0.3)

# Energy relative difference histogram
plt.subplot(2, 2, 3)
plt.hist(energy_rel_diff, bins=20, color='b', alpha=0.7, edgecolor='black')
plt.axvline(avg_energy_rel_diff, color='r', linestyle='--', linewidth=2, label=f'Mean: {avg_energy_rel_diff:.2f}%')
plt.title('Energy Relative Difference Distribution')
plt.xlabel('Relative Difference (%)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

# Latency relative difference histogram
plt.subplot(2, 2, 4)
plt.hist(latency_rel_diff, bins=20, color='g', alpha=0.7, edgecolor='black')
plt.axvline(avg_latency_rel_diff, color='r', linestyle='--', linewidth=2, label=f'Mean: {avg_latency_rel_diff:.2f}%')
plt.title('Latency Relative Difference Distribution')
plt.xlabel('Relative Difference (%)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('cannon_vs_timeloop_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Cannon vs Timeloop comparison plot saved as 'cannon_vs_timeloop_comparison.png'")
print(f"Average Energy Relative Difference: {avg_energy_rel_diff:.2f}%")
print(f"Average Latency Relative Difference: {avg_latency_rel_diff:.2f}%")