import exp_normalize_mac_throughput
import exp_normalize_mac_count
import exp_normalize_area
import exp_normalize_power
import my_plot
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(2, 6, figsize=(20, 8)) 
fig.supxlabel("GEMM Dimension")
ax[0][0].set_ylabel('Normalized Runtime')
ax[1][0].set_ylabel('Normalized Energy')
ax[0][0].set_title('1.8GHz')
ax[0][1].set_title('4GHz')
ax[0][2].set_title('16GHz')
ax[0][3].set_title('30GHz')
ax[0][4].set_title('50GHz')
ax[0][5].set_title('100GHz')

arch_names = ["h100", "imec"]



time_table, energy_table, time_compute_table, energy_compute_table = exp_normalize_area.exp_normalize_area_imec_freq(1.8)
gemm_dims = [1024, 8192, 8192*8, 8192*64]
my_plot.plot_2(time_table, time_compute_table, gemm_dims,arch_names,  "latency", ax[0][0])
my_plot.plot_2(energy_table, energy_compute_table, gemm_dims, arch_names, "energy", ax[1][0])
ylim_latency = ax[0][0].get_ylim()[1]
ylim_energy = ax[1][0].get_ylim()[1]

time_table, energy_table, time_compute_table, energy_compute_table = exp_normalize_area.exp_normalize_area_imec_freq(4.0)
my_plot.plot_2(time_table, time_compute_table, gemm_dims,arch_names,  "latency", ax[0][1])
my_plot.plot_2(energy_table, energy_compute_table, gemm_dims, arch_names, "energy", ax[1][1])
ax[0][1].set_ylim(0, ylim_latency)
ax[1][1].set_ylim(0, ylim_energy)

time_table, energy_table, time_compute_table, energy_compute_table = exp_normalize_area.exp_normalize_area_imec_freq(16.0)
my_plot.plot_2(time_table, time_compute_table, gemm_dims,arch_names,  "latency", ax[0][2])
my_plot.plot_2(energy_table, energy_compute_table, gemm_dims, arch_names, "energy", ax[1][2])
ax[0][2].set_ylim(0, ylim_latency)
ax[1][2].set_ylim(0, ylim_energy)

time_table, energy_table, time_compute_table, energy_compute_table = exp_normalize_area.exp_normalize_area_imec_freq(30.0)
my_plot.plot_2(time_table, time_compute_table, gemm_dims,arch_names,  "latency", ax[0][3])
my_plot.plot_2(energy_table, energy_compute_table, gemm_dims, arch_names, "energy", ax[1][3])
ax[0][3].set_ylim(0, ylim_latency)
ax[1][3].set_ylim(0, ylim_energy)

time_table, energy_table, time_compute_table, energy_compute_table = exp_normalize_area.exp_normalize_area_imec_freq(50.0)
my_plot.plot_2(time_table, time_compute_table, gemm_dims,arch_names,  "latency", ax[0][4])
my_plot.plot_2(energy_table, energy_compute_table, gemm_dims, arch_names, "energy", ax[1][4])
ax[0][4].set_ylim(0, ylim_latency)
ax[1][4].set_ylim(0, ylim_energy)

time_table, energy_table, time_compute_table, energy_compute_table = exp_normalize_area.exp_normalize_area_imec_freq(100.0)
my_plot.plot_2(time_table, time_compute_table, gemm_dims,arch_names,  "latency", ax[0][5])
my_plot.plot_2(energy_table, energy_compute_table, gemm_dims, arch_names, "energy", ax[1][5])
ax[0][5].set_ylim(0, ylim_latency)
ax[1][5].set_ylim(0, ylim_energy)



handles, labels = ax[0][0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower right", ncols=6)
fig.suptitle('IMEC Latency and Energy Normalized to H100, with different frequencies, iso-area')
fig.tight_layout()
plt.savefig("fig_comparative_study_sweep_freq.pdf")


plt.close('all')