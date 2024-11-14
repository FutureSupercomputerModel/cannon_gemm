import exp_normalize_mac_throughput
import exp_normalize_mac_count
import exp_normalize_area
import exp_normalize_power
import my_plot
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(2, 4, figsize=(20, 8)) 
fig.supxlabel("GEMM Dimension")
ax[0][0].set_ylabel('Normalized Runtime')
ax[1][0].set_ylabel('Normalized Energy')
ax[0][0].set_title('iso-compute throughput')
ax[0][1].set_title('iso-mac count')
ax[0][2].set_title('iso-area')
ax[0][3].set_title('iso-power')

arch_names = ["h100", "tpuv1", "tpuv4", "cryoE", "cryoP", "imec"]

time_table, energy_table = exp_normalize_mac_throughput.exp_normalize_mac_throughput()
gemm_dims = [1024, 8192, 8192*8, 8192*64]
my_plot.plot(time_table, gemm_dims, arch_names, "latency", ax[0][0])
my_plot.plot(energy_table, gemm_dims, arch_names,  "energy", ax[1][0])

time_table, energy_table = exp_normalize_mac_count.exp_normalize_mac_count()
my_plot.plot(time_table, gemm_dims, arch_names,  "latency", ax[0][1])
my_plot.plot(energy_table, gemm_dims, arch_names,  "energy", ax[1][1])

time_table, energy_table = exp_normalize_area.exp_normalize_area()
my_plot.plot(time_table, gemm_dims, arch_names,  "latency", ax[0][2])
my_plot.plot(energy_table, gemm_dims, arch_names,  "energy", ax[1][2])

time_table, energy_table = exp_normalize_power.exp_normalize_power()
my_plot.plot(time_table, gemm_dims, arch_names,  "latency", ax[0][3])
my_plot.plot(energy_table, gemm_dims, arch_names,  "energy", ax[1][3])

handles, labels = ax[0][0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower right", ncols=6)
fig.suptitle('Normalized Latency and Energy for Different Architectures')
fig.tight_layout()
plt.savefig("comparative_study.pdf")


plt.close('all')