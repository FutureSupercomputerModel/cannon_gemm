import matplotlib.pyplot as plt
import numpy as np

def plot(table, gemm_dims, latency_or_energy, ax):
    normed_table = []
    for i in range(len(table)):
        normed_list = []
        for j in range(len(table[i])):
            normed_list.append(table[i][j]/table[i][0])
        normed_table.append(normed_list)
    normed_table = list(map(list, zip(*normed_table)))
    # print (time_normed_table)
    arch_names = ["h100", "tpuv1", "tpuv4", "cryoE", "cryoP", "imec"]

    width = 0.12  # the width of the bars
    multiplier = 0
    
    for arch_name, normed_list in zip(arch_names, normed_table):
        ax.bar(np.arange(len(normed_list)) + multiplier*width, normed_list, width, label=arch_name)
        for i, normed in enumerate(normed_list):
            if normed > 1:
                ax.text(i + multiplier*width, 1,  f'{normed:.1f}', rotation=90, ha='center', va='top', size='small')
            # elif normed >0.8:
            #     ax.text(i + multiplier*width, normed,  f'{normed:.2f}', rotation=90, ha='center', va='top', size='small')
            elif arch_name == "imec":
                ax.text(i + multiplier*width, normed,  f'{normed:.2f}', rotation=90, ha='center', va='bottom', size='small')
        multiplier += 1
    # ax.set_ylabel(f'{latency_or_energy}_normed')
    # ax.set_title(f'Normalized {latency_or_energy} for Different Architectures')
    ax.set_xticks(np.arange(len(normed_list)) + width*(len(arch_names)-1)/2.0, gemm_dims)
    # ax.legend(loc=(0.01,0.8), ncol = 3)
    ax.set_ylim(0,1)





def plot_energy(energy_table, gemm_dims, file_name):
    energy_normed_table = []
    for i in range(len(energy_table)):
        energy_normed_list = []
        for j in range(len(energy_table[i])):
            energy_normed_list.append(energy_table[i][j]/energy_table[i][0])
        energy_normed_table.append(energy_normed_list)
    energy_normed_table = list(map(list, zip(*energy_normed_table)))
    # print (energy_table)
    arch_names = ["h100", "tpuv1", "tpuv4", "cryoE", "cryoP", "imec"]

    width = 0.12  # the width of the bars
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')
    for arch_name, energy_normed_list in zip(arch_names, energy_normed_table):
        ax.bar(np.arange(len(energy_normed_list)) + multiplier*width, energy_normed_list, width, label=arch_name)
        for i, energy_normed in enumerate(energy_normed_list):
            if energy_normed > 1:
                ax.text(i + multiplier*width, 1,  f'{energy_normed:.1f}', rotation=90, ha='center', va='top', size='small')
        multiplier += 1
    ax.set_ylabel('Normalized Energy')
    ax.set_title('Normalized Energy for Different Architectures')
    ax.set_xticks(np.arange(len(energy_normed_list)) + width*(len(arch_names)-1)/2.0, gemm_dims)
    ax.set_ylim(0,1)
    ax.legend(loc=(0.01,0.8), ncol = 3)

    plt.savefig(file_name)


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