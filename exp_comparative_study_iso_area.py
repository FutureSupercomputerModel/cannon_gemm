import exp_normalize_mac_throughput
import exp_normalize_mac_count
import exp_normalize_area
import exp_normalize_power
import my_plot
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(2, 1, figsize=(4, 4)) 
fig.supxlabel("GEMM Dimension")
label0 = ax[0].set_ylabel('Normalized Runtime')
label1 = ax[1].set_ylabel('Normalized Energy')

arch_names = ["h100", "tpuv1", "tpuv4", "cryoE", "cryoP", "imec"]

gemm_dims = [1024, 8192, 8192*8, 8192*64]

time_table, energy_table = exp_normalize_area.exp_normalize_area()
my_plot.plot(time_table, gemm_dims, arch_names,  "latency", ax[0], logscale=True)
my_plot.plot(energy_table, gemm_dims, arch_names,  "energy", ax[1], logscale=True)
ax[0].axhline(y = 1.0, color = 'blue', linestyle = '-') 
ax[1].axhline(y = 1.0, color = 'blue', linestyle = '-')
# box = ax[0].get_position()
# ax[0].set_position([box.x0, box.y0, box.width * 0.8, box.height])
# box = ax[1].get_position()
# ax[1].set_position([box.x0, box.y0, box.width * 0.8, box.height])
handles, labels = ax[0].get_legend_handles_labels()
# ax[0].setylim(0,5)
# ax[1].setylim(0,5)
lgd = fig.legend(handles, labels, ncols=3, loc='upper center', bbox_to_anchor=(0.5, 0))
title = fig.suptitle('Normalized Latency and Energy \nfor Different Architectures, iso-area')
# fig.tight_layout()
plt.savefig("fig_comparative_study_iso_area.pdf", bbox_extra_artists=(lgd,label0, label1, title, ), bbox_inches='tight')


plt.close('all')