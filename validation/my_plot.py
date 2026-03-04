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

def plot(
    table, gemm_dims, arch_names, latency_or_energy, ax, 
    logscale=False, ylim=1, show_wkld_names=True, rotate_xticks=False, xtick_fontsize=None,
    tick_width=1.2, spine_width=1.2, label_fontsize=12, label_fontweight='normal', tick_label_fontweight='normal'
):
    normed_table = []
    for i in range(len(table)):
        normed_list = []
        for j in range(len(table[i])):
            normed_list.append(table[i][j]/table[i][0])
        normed_table.append(normed_list)
    normed_table = list(map(list, zip(*normed_table)))

    width = 1/1.3/len(arch_names)
    multiplier = 0

    color_map = {
        "h100gpu": "#1976D2",      # strong blue
        "tpuv4": "#FF9800",        # vivid orange
        "cryop": "#006D5B",        # strong teal
        "cryoe": "#A9CD51",        # strong green
        "cmos": "#7B1FA2",         # strong purple
        "imec": "#D32F2F",         # strong red
        "ersfq": "#616161"         # dark gray
    }
    label_archs = ["imec", "cmos", "cryoe", "cryop", "tpuv4"]  # List of architectures to label

    for arch_name, normed_list in zip(arch_names, normed_table):
        color = color_map.get(arch_name, None)
        bars = ax.bar(np.arange(len(normed_list)) + multiplier*width, normed_list, width, label=arch_name, color=color)
        for i, normed in enumerate(normed_list):
            # Add normalized value label for selected architectures
            if arch_name in label_archs:
                ax.text(i + multiplier*width, normed, f'{normed:.2f}x', 
                        rotation=90, ha='center', va='bottom', size='small', color='black')
            # Add normalized value label for SCD (imec)
            if arch_name == "imec":
                ax.text(i + multiplier*width, normed, f'{normed:.2f}x', 
                        rotation=90, ha='center', va='bottom', size='small', color='black')
            if not logscale and normed > ylim:
                ax.text(i + multiplier*width, ylim,  f'{normed:.1f}', rotation=90, ha='center', va='top', size='small')
            elif arch_name == "SCD":
                ax.text(i + multiplier*width, normed,  f'{normed:.2f}', rotation=90, ha='center', va='bottom', size='small')
        multiplier += 1

    # Capitalize and format model names for x-tick labels
    def format_model_name(name):
        if name.lower().startswith("gpt3"):
            return name.replace("gpt3", "GPT-3").replace("gpt", "GPT")
        elif name.lower().startswith("gopher"):
            return name.replace("gopher", "Gopher-")
        elif name.lower().startswith("palm"):
            return name.replace("palm", "PaLM-")
        elif name.lower().startswith("megatron"):
            return name.replace("megatron", "Megatron-")
        elif name.lower() == "gmean":
            return "GMean"
        else:
            return name.capitalize()

    formatted_gemm_dims = [format_model_name(x) for x in gemm_dims]

    # Handle x-ticks
    if show_wkld_names:
        ax.set_xticks(np.arange(len(normed_list)) + width*(len(arch_names)-1)/2.0, formatted_gemm_dims)
        if rotate_xticks:
            for label in ax.get_xticklabels():
                label.set_rotation(45)
        if xtick_fontsize is not None:
            for label in ax.get_xticklabels():
                label.set_fontsize(xtick_fontsize)
    else:
        ax.set_xticks(np.arange(len(normed_list)) + width*(len(arch_names)-1)/2.0, [])

    if logscale:
        ax.set_yscale('log')
    else:
        ax.set_ylim(0, ylim)

    # Axis labels bold/thick, tick labels small/normal
    ax.tick_params(axis='both', which='major', labelsize=label_fontsize, width=tick_width, length=7)
    ax.tick_params(axis='both', which='minor', labelsize=label_fontsize-2, width=tick_width, length=4)
    ax.xaxis.label.set_fontsize(label_fontsize)
    ax.xaxis.label.set_weight(label_fontweight)
    ax.yaxis.label.set_fontsize(label_fontsize)
    ax.yaxis.label.set_weight(label_fontweight)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight(tick_label_fontweight)
    for label in ax.get_xticklabels():
        label.set_fontsize(xtick_fontsize if xtick_fontsize else label_fontsize)
    for spine in ax.spines.values():
        spine.set_linewidth(spine_width)

# def plot(table, gemm_dims, arch_names, latency_or_energy, ax, logscale = False, ylim=1):
#     normed_table = []
#     for i in range(len(table)):
#         normed_list = []
#         for j in range(len(table[i])):
#             normed_list.append(table[i][j]/table[i][0])
#         normed_table.append(normed_list)
#     normed_table = list(map(list, zip(*normed_table)))
#     # print (time_normed_table)

#     width = 1/1.3/len(arch_names)  # the width of the bars
#     multiplier = 0
    
#     for arch_name, normed_list in zip(arch_names, normed_table):
#         ax.bar(np.arange(len(normed_list)) + multiplier*width, normed_list, width, label=arch_name)
#         for i, normed in enumerate(normed_list):
#             if not logscale and normed > ylim:
#                 ax.text(i + multiplier*width, ylim,  f'{normed:.1f}', rotation=90, ha='center', va='top', size='small')
#             # elif normed >0.8:
#             #     ax.text(i + multiplier*width, normed,  f'{normed:.2f}', rotation=90, ha='center', va='top', size='small')
#             elif arch_name == "SCD":
#                 ax.text(i + multiplier*width, normed,  f'{normed:.2f}', rotation=90, ha='center', va='bottom', size='small')
#         multiplier += 1
#     # ax.set_ylabel(f'{latency_or_energy}_normed')
#     # ax.set_title(f'Normalized {latency_or_energy} for Different Architectures')
#     ax.set_xticks(np.arange(len(normed_list)) + width*(len(arch_names)-1)/2.0, gemm_dims)
#     # ax.legend(loc=(0.01,0.8), ncol = 3)
    
#     if logscale:
#         ax.set_yscale('log')
#     else:
#         ax.set_ylim(0,ylim)

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