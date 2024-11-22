import numpy as np
from GEMM.arch import Arch
from GEMM.leaf import Leaf
from GEMM.arch import top_level_gemm
from adjustText import adjust_text
import math

# m,k,n = 8192*64,8192*64,8192*64
m,k,n = 1024,1024,1024
DEBUG = True

class Sys_arch:
    def __init__(self, leaf_pe_arr_dim,\
                 leaf_sram_size,\
                blade_mesh_dim,\
                blade_dram_bw,\
                node_mesh_dim,\
                blade_dram_size,\
                label=None):
        self.leaf_pe_arr_dim = leaf_pe_arr_dim #var3
        self.leaf_sram_size = leaf_sram_size #according to var3
        self.blade_mesh_dim = blade_mesh_dim #var1
        self.blade_dram_bw = blade_dram_bw
        self.node_mesh_dim = node_mesh_dim
        self.blade_dram_size = blade_dram_size #var2
        self.label = label
    def cannon_gemm(self, m, k, n, debug=False):
        imec_leaf = Leaf(pe_arr_dim=self.leaf_pe_arr_dim, 
                        # buffer_size=f"{self.leaf_pe_arr_dim*self.leaf_pe_arr_dim/200.0/200*20}MB", 
                        buffer_size=f"{self.leaf_sram_size}MB", 
                        # buffer_bw = f'{self.leaf_pe_arr_dim*self.leaf_pe_arr_dim/200.0/200*73.34}TBps',
                        buffer_bw = f'{73.34}TBps',
                        pe_freq=30.0, 
                        E_per_mac='14fJ', 
                        interconnect_E_per_bit='0.00001pJ', 
                        buffer_E_per_bit="0.021fJ", 
                        bytes_per_element=2,
                        buffer_bit_area=3.125,
                        mac_area=3600,
                        is3d=True)
        imec_blade = Arch(mesh_dim=self.blade_mesh_dim, 
                    # mesh_bw=f'{self.leaf_pe_arr_dim*self.leaf_pe_arr_dim/200.0/200*73.34}TBps', 
                    mesh_bw=f'{73.34}TBps', 
                    buffer_size=f"{self.blade_dram_size}GB", 
                    buffer_bw=f'{self.blade_dram_bw}TBps', 
                    mesh_E_per_bit='5e-4pJ', 
                    buffer_E_per_bit=f'{22*0.029}pJ',
                    buffer_static_W_per_bit=f'{22*1.33}pW',
                    sc_to_cryo_E_per_bit="0.4pJ",
                    cryo_to_sc_E_per_bit="4.24pJ", 
                    child_arch=imec_leaf)
        imec_node = Arch(mesh_dim=self.node_mesh_dim, 
                    mesh_bw='1PBps', 
                    buffer_size="8TB", 
                    buffer_bw='3.0PBps', 
                    mesh_E_per_bit='5e-3pJ', 
                    buffer_E_per_bit=f'{0}pJ', 
                    buffer_static_W_per_bit=f'{0}pW',
                    sc_to_cryo_E_per_bit="0pJ",
                    cryo_to_sc_E_per_bit="0pJ",
                    child_arch=imec_blade)
        T_top, E_total, T_memory, T_communication, T_compute, log = top_level_gemm(m,k,n, imec_node, debug=debug, general_tiling=True)
        return T_top, E_total

sys_arch_list = []
counter = 1
total_dram_bw = 1920
for sram_area_ratio in [5/6.0, 4/6.0, 2/6.0]:
    for total_dram_capacity in [32768, 16384, 65536]:
        for blade_mesh_dim in [8,4,2]:
                leaf_pe_arr_dim = math.sqrt(6*(1-sram_area_ratio)*200*200)
                node_mesh_dim = math.sqrt(8*8/blade_mesh_dim/blade_mesh_dim*8*8)
                blade_dram_bw = total_dram_bw/node_mesh_dim/node_mesh_dim
                blade_dram_size = total_dram_capacity/node_mesh_dim/node_mesh_dim
                leaf_sram_size = 6*sram_area_ratio*4
                label = f"c{counter}"
                counter += 1
        
                sys_arch_list.append(Sys_arch(leaf_pe_arr_dim=leaf_pe_arr_dim, leaf_sram_size=leaf_sram_size, blade_mesh_dim=blade_mesh_dim, blade_dram_bw=blade_dram_bw, node_mesh_dim=node_mesh_dim, blade_dram_size=blade_dram_size, label=label))
print(f"number of experiments: {len(sys_arch_list)}")
#print sys_arch_list to see the list of experiments
for sys_arch in sys_arch_list:
    print(f"PE array dim={sys_arch.pe_arr_dim}, SRAM size={sys_arch.sram_size}, blade mesh dim={sys_arch.blade_mesh_dim}, blade dram bw={sys_arch.blade_dram_bw}, blade dram size={sys_arch.blade_dram_size}, node mesh dim={sys_arch.node_mesh_dim} ")

import matplotlib
import matplotlib.pyplot as plt
import numpy as np



data = []
print(f"number of experiments: {len(sys_arch_list)}")
finished_exps = 0
import multiprocessing
from multiprocessing import Pool
from tqdm import tqdm
import json
import csv

def exp(sys_arch:Sys_arch):
    T_top, E_total = sys_arch.cannon_gemm(m,k,n, debug=DEBUG)
    return sys_arch, T_top, E_total

max_processes = int(multiprocessing.cpu_count())
print("Maximum number of processes:", max_processes)
pool = Pool(max_processes)
# res = tqdm(pool.imap_unordered(exp, sys_arch_list), total=len(sys_arch_list)) 
res = list(tqdm(pool.imap_unordered(exp, sys_arch_list), total=len(sys_arch_list)))
print(f"finished all {len(res)} experiments")

with open("data_design_space_explore.csv", "w") as fp:
    writer = csv.writer(fp)
    writer.writerow(["label", "leaf_pe_arr_dim", "leaf_sram_size","blade_mesh_dim","dram_bw_per_blade", "node_mesh_dim","T_top(s)", "E_total(J)"])
    for sys_arch, T_top, E_total in res:
        #for plot
        # list_T = np.append(list_T, T_top)
        # list_E = np.append(list_E, E_total)
        #for dump
        row=[sys_arch.label, sys_arch.leaf_pe_arr_dim, sys_arch.leaf_sram_size , sys_arch.blade_mesh_dim, sys_arch.node_mesh_dim, T_top, E_total]
        writer.writerow(row)
        data.append(row)
# with open("cannon_gemm_para_sweep_dumped_data", "w") as fp:
#     json.dump(data, fp)

LEAF_PE_ARR_DIM = 0
BLADE_MESH_DIM = 1
NODE_MESH_DIM = 2

list_param_name = ["LEAF_PE_ARR_DIM",
            "BLADE_MESH_DIM",
            "NODE_MESH_DIM"
            ]

def get_label(row):
    return ", ".join([f"{list_param_name[i]}: {row[i]}" for i in range(len(list_param_name))])

ALPHA = 0.3

def plot_energy_vs_latency(data):
    
    list_T = np.array([float(row[-2]) for row in data])
    list_E = np.array([float(row[-1]) for row in data])
    
    fig4 = plt.figure("Energy vs Latency", figsize=(4, 3))
    texts = []
    plt.scatter(list_T, list_E, s=50, alpha=ALPHA)
    for row in data:
        texts.append(plt.text(float(row[-2]), float(row[-1]), row[0], fontsize=10))
    
    adjust_text(texts, arrowprops=dict(arrowstyle="->", color='None', lw=1.0))
    plt.ticklabel_format(axis='both', style='sci', scilimits=(0,0))
    plt.xlabel('Latency (s)')
    plt.ylabel('Energy (J)')
    plt.title(f'GEMM m=k=n=2^{int(math.log2(m))}')
    plt.tight_layout()
    plt.savefig('fig_design_space_explore.pdf')
    matplotlib.pyplot.close()

plot_energy_vs_latency(data)
