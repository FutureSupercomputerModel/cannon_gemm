import exp_normalize_mac_throughput
import exp_normalize_mac_count
import exp_normalize_area
import exp_normalize_power
import my_plot
import matplotlib.pyplot as plt
import numpy as np
arch_list = ['imec_Nb_interconnect', 'imec']
fig, ax = plt.subplots(2, len(arch_list), figsize=(5*len(arch_list), 8)) 
fig.supxlabel("GEMM Dimension")
ax[0][0].set_ylabel('Normalized Runtime')
ax[1][0].set_ylabel('Normalized Energy')

arch_names = ["h100", "imec"]


lim_set = False
for i, arch in enumerate(arch_list):
    time_table, energy_table, time_compute_table, energy_compute_table = exp_normalize_area.exp_ablation(arch)
    gemm_dims = [1024, 8192, 8192*8, 8192*64]
    my_plot.plot_2(time_table, time_compute_table, gemm_dims,arch_names,  "latency", ax[0][i])
    my_plot.plot_2(energy_table, energy_compute_table, gemm_dims, arch_names, "energy", ax[1][i])
    if not lim_set:
        ylim_latency = ax[0][0].get_ylim()[1]
        ylim_energy = ax[1][0].get_ylim()[1]
        lim_set = True
    ax[0][i].set_ylim(0, ylim_latency)
    ax[1][i].set_ylim(0, ylim_energy)
    ax[0][i].set_title(f'{arch}')



handles, labels = ax[0][0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower right", ncols=6)
fig.suptitle('IMEC Latency and Energy Normalized to H100, with Nb or NbTiN, iso-area')
fig.tight_layout()
plt.savefig("fig_ablation_interconnect.pdf")


plt.close('all')