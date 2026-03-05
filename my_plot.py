import matplotlib.pyplot as plt
import numpy as np
def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


import numpy as np

def plot(table, gemm_dims, arch_names, latency_or_energy, ax, logscale=False, ylim=1, show_wkld_names=True, rotate_xticks=False):
    normed_table = []
    for i in range(len(table)):
        normed_list = []
        for j in range(len(table[i])):
            normed_list.append(table[i][j] / table[i][0])
        normed_table.append(normed_list)
    normed_table = list(map(list, zip(*normed_table)))

    width = 1 / 1.3 / len(arch_names)  # the width of the bars
    multiplier = 0

    for arch_name, normed_list in zip(arch_names, normed_table):
        ax.bar(np.arange(len(normed_list)) + multiplier * width, normed_list, width, label=arch_name)
        for i, normed in enumerate(normed_list):
            if not logscale and normed > ylim:
                ax.text(i + multiplier * width, ylim, f'{normed:.1f}', rotation=90, ha='center', va='top', size='small')
            elif arch_name == "SCD":
                ax.text(i + multiplier * width, normed, f'{normed:.2f}', rotation=90, ha='center', va='bottom', size='small')
        multiplier += 1

    # Control x-axis labels visibility based on show_wkld_names parameter
    if show_wkld_names:
        ax.set_xticks(np.arange(len(normed_list)) + width * (len(arch_names) - 1) / 2.0)
        ax.set_xticklabels(gemm_dims)
        
        # Rotate x-ticks if rotate_xticks is True
        if rotate_xticks:
            ax.tick_params(axis='x', rotation=45)
    else:
        ax.set_xticks([])  # Remove tick marks
        ax.set_xticklabels([])  # Remove tick labels

    if logscale:
        ax.set_yscale('log')
    else:
        ax.set_ylim(0, ylim)



def plot_2(table, table_compute, gemm_dims, arch_names, latency_or_energy, ax):
    normed_table = []
    for i in range(len(table)):
        normed_list = []
        for j in range(len(table[i])):
            normed_list.append(table[i][j]/table[i][0])
        normed_table.append(normed_list)
    normed_table = list(map(list, zip(*normed_table)))

    normed_table_compute = []
    for i in range(len(table_compute)):
        normed_list = []
        for j in range(len(table_compute[i])):
            normed_list.append(table_compute[i][j]/table[i][0])
        normed_table_compute.append(normed_list)
    normed_table_compute = list(map(list, zip(*normed_table_compute)))
    # print (time_normed_table)

    
    arch_names = arch_names[1:]
    normed_table = normed_table[1:]
    normed_table_compute = normed_table_compute[1:]
    width = 1/1.3/len(arch_names)  # the width of the bars
    multiplier = 0
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for arch_name, normed_list, normed_list_compute in zip(arch_names, normed_table, normed_table_compute):
        ax.bar(np.arange(len(normed_list)) + multiplier*width, normed_list, width, label=f"{arch_name}_stall", color=colors[multiplier])
        ax.bar(np.arange(len(normed_list_compute)) + multiplier*width, normed_list_compute, width, label=f"{arch_name}_compute", color=lighten_color(colors[multiplier], 1.6))
        # for i, normed in enumerate(normed_list):
        #     if normed > 1:
        #         ax.text(i + multiplier*width, normed,  f'{normed:.1f}', rotation=90, ha='center', va='top', size='small')
        #     # elif normed >0.8:
        #     #     ax.text(i + multiplier*width, normed,  f'{normed:.2f}', rotation=90, ha='center', va='top', size='small')
        #     elif arch_name == "imec":
        #         ax.text(i + multiplier*width, normed,  f'{normed:.2f}', rotation=90, ha='center', va='bottom', size='small')
        multiplier += 1
    # ax.set_ylabel(f'{latency_or_energy}_normed')
    # ax.set_title(f'Normalized {latency_or_energy} for Different Architectures')
    ax.set_xticks(np.arange(len(normed_list)) + width*(len(arch_names)-1)/2.0, gemm_dims)
    # ax.legend(loc=(0.01,0.8), ncol = 3)
    # ax.set_ylim(0,1)





    # energy_saving_table = []
# for i in range(len(energy_table)):
#     energy_saving_list = []
#     for j in range(len(energy_table[i])):
#         energy_saving_list.append(energy_table[i][0]/energy_table[i][j])
#     energy_saving_table.append(energy_saving_list)
# energy_saving_table = list(map(list, zip(*energy_saving_table)))
# # print (energy_table)
# arch_names = ["h100", "tpuv1", "tpuv4", "cmos3d", "cryoE", "cryoP", "imec"]
# width = 0.12  # the width of the bars
# multiplier = 0
# fig, ax = plt.subplots(layout='constrained')
# for arch_name, energy_saving_list in zip(arch_names, energy_saving_table):
#     ax.bar(np.arange(len(energy_saving_list)) + multiplier*width, energy_saving_list, width, label=arch_name)
#     multiplier += 1
# ax.set_ylabel('Energy Saving')
# ax.set_title('Energy Savings for Different Architectures')
# ax.set_xticks(np.arange(len(energy_saving_list)) + width*3, gemm_dims)
# ax.legend(loc='upper left', ncols=3)

# plt.savefig("energy_saving_normalize_mac_count.pdf")

# # print (time_table)
# speedup_table = []
# for i in range(len(time_table)):
#     speedup_list = []
#     for j in range(len(time_table[i])):
#         speedup_list.append(time_table[i][0]/time_table[i][j])
#     speedup_table.append(speedup_list)
# # print (speedup_table)
# #transpose speedup_table
# speedup_table = list(map(list, zip(*speedup_table)))
# # print (speedup_table)
# arch_names = ["h100", "tpuv1", "tpuv4", "cmos3d", "cryoE", "cryoP", "imec"]

# width = 0.1  # the width of the bars
# multiplier = 0
# fig, ax = plt.subplots(layout='constrained')
# for arch_name, speedup_list in zip(arch_names, speedup_table):
#     ax.bar(np.arange(len(speedup_list)) + multiplier*width, speedup_list, width, label=arch_name)
#     multiplier += 1
# ax.set_ylabel('Speedup')
# ax.set_title('Speedups for different architectures')
# ax.set_xticks(np.arange(len(speedup_list)) + width*3, gemm_dims)
# ax.legend(loc='upper left', ncols=3)

# plt.savefig("speedup_normalize_mac_count.pdf")