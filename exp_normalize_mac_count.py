from GEMM.arch import Arch
from GEMM.leaf import Leaf
from GEMM.arch import top_level_gemm
import math
import json
import my_plot
def exp_normalize_mac_count():
    h100_leaf = Leaf(pe_arr_dim=519.93, 
                        buffer_size=f'{50}MB', 
                        buffer_bw = f'{512*2*16/8*1.8}GBps', 
                        pe_freq=1.8, 
                        E_per_mac="0.38pJ", 
                        interconnect_E_per_bit="0.1pJ", 
                        buffer_E_per_bit='0.5fJ', 
                        bytes_per_element=2,
                        buffer_bit_area=0.058,
                        mac_area=550/3,
                        is3d=False)
    h100_blade = Arch(mesh_dim=1.0, 
                    mesh_bw=f'{450}GBps', #NVLink
                    buffer_size="80GB", 
                    buffer_bw='3352GBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=h100_leaf)
    h100_node = Arch(mesh_dim=4.0, 
                    mesh_bw=f'{450}GBps', 
                    buffer_size="8TB", 
                    buffer_bw=f'{math.inf}TBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=h100_blade)
    h100_node.peak_power = 700*h100_node.mesh_dim*h100_node.mesh_dim



    tpuv1_leaf = Leaf(pe_arr_dim=256.0, 
                        buffer_size=f'{24+4}MB', 
                        buffer_bw = f'{256*2*8/8*0.7}GBps', 
                        pe_freq=0.7/4, 
                        E_per_mac="0.38pJ", 
                        interconnect_E_per_bit="0.1pJ", 
                        buffer_E_per_bit='0.5fJ', 
                        bytes_per_element=2,
                        buffer_bit_area=0.058,
                        mac_area=550/3,
                        is3d=False)
    tpuv1_blade = Arch(mesh_dim=1.0, 
                    mesh_bw=f'{300}GBps', #1000GBps
                    buffer_size="80GB", 
                    buffer_bw='30GBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=tpuv1_leaf)
    tpuv1_node = Arch(mesh_dim=7.0, 
                    mesh_bw=f'{300}GBps', 
                    buffer_size="8TB", 
                    buffer_bw=f'{math.inf}GBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=tpuv1_blade)
    tpuv1_node.peak_power = 75*tpuv1_node.mesh_dim*tpuv1_node.mesh_dim


    tpuv4_leaf = Leaf(pe_arr_dim=361.0, 
                        buffer_size=f'{128}MB', 
                        buffer_bw = f'{362*2*8/8*1.05}GBps', 
                        pe_freq=1.05, 
                        E_per_mac="0.38pJ", 
                        interconnect_E_per_bit="0.1pJ", 
                        buffer_E_per_bit='0.5fJ', 
                        bytes_per_element=2,
                        buffer_bit_area=0.058,
                        mac_area=550,
                        is3d=False)
    tpuv4_blade = Arch(mesh_dim=1.0, 
                    mesh_bw=f'{300}GBps', #1000GBps
                    buffer_size="32GB", 
                    buffer_bw='1200GBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=tpuv4_leaf)
    tpuv4_node = Arch(mesh_dim=5.0, 
                    mesh_bw=f'{300}GBps', 
                    buffer_size="8TB", 
                    buffer_bw=f'{math.inf}GBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=tpuv4_blade)
    tpuv4_node.peak_power = 192*tpuv4_node.mesh_dim*tpuv4_node.mesh_dim




    cmos3d_leaf = Leaf(pe_arr_dim=128.0*4, 
                        buffer_size=f'{16.0*16}MB', 
                        buffer_bw = f'{9680}GBps', 
                        pe_freq=4.0, 
                        E_per_mac="0.38pJ", 
                        interconnect_E_per_bit="0.1pJ", 
                        buffer_E_per_bit='0.5fJ', 
                        bytes_per_element=2,
                        buffer_bit_area=0.058,
                        mac_area=550,
                        is3d=True)
    cmos3d_blade = Arch(mesh_dim=4.0, 
                    mesh_bw=f'{9680}GBps', #1000GBps
                    buffer_size="80GB", 
                    buffer_bw='30.0TBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=cmos3d_leaf)
    cmos3d_node = Arch(mesh_dim=1.0, 
                    mesh_bw='1PBps', 
                    buffer_size="8TB", 
                    buffer_bw='3.0PBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit='0.29pJ', 
                    child_arch=cmos3d_blade)




    cryoE_leaf = Leaf(pe_arr_dim=128.0*4, 
                        buffer_size=f'{256}MB', 
                        buffer_bw = f'{9680}GBps', 
                        pe_freq=4.0, 
                        E_per_mac="2.27pJ", 
                        interconnect_E_per_bit="0.1pJ", 
                        buffer_E_per_bit='2.75fJ', 
                        bytes_per_element=2,
                        buffer_bit_area=0.058,
                        mac_area=550,
                        is3d=True)
    cryoE_blade = Arch(mesh_dim=4.0, 
                    mesh_bw=f'{9680}GBps', 
                    buffer_size="80GB", 
                    buffer_bw='30.0TBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit=f'{22*0.029}pJ', 
                    child_arch=cryoE_leaf)
    cryoE_node = Arch(mesh_dim=1.0, 
                    mesh_bw='1PBps', 
                    buffer_size="8TB", 
                    buffer_bw='3.0PBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit=f'{22*0.029}pJ', 
                    child_arch=cryoE_blade)



    cryoP_leaf = Leaf(pe_arr_dim=128.0*4, 
                        buffer_size=f'{16.0*16}MB', 
                        buffer_bw = f'{13552}GBps', 
                        pe_freq=5.6, 
                        E_per_mac="8.4pJ", 
                        interconnect_E_per_bit="0.1pJ", 
                        buffer_E_per_bit='11fJ', 
                        bytes_per_element=2,
                        buffer_bit_area=0.058,
                        mac_area=550)
    cryoP_blade = Arch(mesh_dim=4.0, 
                    mesh_bw=f'{13552}GBps', 
                    buffer_size="80GB", 
                    buffer_bw='30.0TBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit=f'{22*0.29}pJ', 
                    child_arch=cryoP_leaf)
    cryoP_node = Arch(mesh_dim=1.0, 
                    mesh_bw='1PBps', 
                    buffer_size="8TB", 
                    buffer_bw='3.0PBps', 
                    mesh_E_per_bit='0.1pJ', 
                    buffer_E_per_bit=f'{22*0.29}pJ', 
                    child_arch=cryoP_blade)




    imec_leaf = Leaf(pe_arr_dim=200.0, 
                        buffer_size='20MB', 
                        buffer_bw = f'{73.34}TBps',
                        pe_freq=30.0, 
                        E_per_mac='14fJ', 
                        interconnect_E_per_bit='0.00001pJ', 
                        buffer_E_per_bit="0.021fJ", 
                        bytes_per_element=2,
                        buffer_bit_area=3.125,
                        mac_area=3600,
                        is3d=True)
    imce_blade = Arch(mesh_dim=9.0, 
                    mesh_bw=f'{73.34}TBps', 
                    buffer_size="80GB", 
                    buffer_bw='30.0TBps', 
                    mesh_E_per_bit='5e-4pJ', 
                    buffer_E_per_bit=f'{22*0.029}pJ', 
                    child_arch=imec_leaf)
    imec_node = Arch(mesh_dim=1.0, 
                    mesh_bw='1PBps', 
                    buffer_size="8TB", 
                    buffer_bw='3.0PBps', 
                    mesh_E_per_bit='5e-3pJ', 
                    buffer_E_per_bit=f'{22*0.029}pJ', 
                    child_arch=imce_blade)
    gemm_dims = [819, 8192, 81920, 819200]
    gemm_sizes = [
        (m, m, m) for m in gemm_dims
    ]
    time_table = []
    energy_table = []
    for m,k,n in gemm_sizes:
        time_list = []
        energy_list = []
        for arch in [h100_node, tpuv1_node, tpuv4_node]:
            time,_,log = top_level_gemm(m,k,n, arch, debug=False, general_tiling=True)
            log = json.loads(log)
            print (f"Time: {time}, Energy: {time * arch.peak_power}, Time_compute: {log['Level 0 logs']['T_compute']*1E-9}")
            time_list.append(time)
            energy_list.append(time * arch.peak_power)
        for arch in [cryoE_node, cryoP_node, imec_node]:
            time,energy,log = top_level_gemm(m,k,n, arch, debug=False, general_tiling=True)
            log = json.loads(log)
            leaf_arch = arch
            while leaf_arch.child_arch is not None:
                leaf_arch = leaf_arch.child_arch
            print (f"Time: {time}, Energy: {energy}, Time_compute: {log['Level 0 logs']['T_compute']*1E-9}, energy_compute: {log['Level 0 logs']['mac']*leaf_arch.nJ_per_mac*1e-9}")
            time_list.append(time)
            energy_list.append(energy)

        time_table.append(time_list)
        energy_table.append(energy_list)
    return time_table, energy_table

# my_plot.plot_energy(energy_table, gemm_dims, "fig_energy_normalize_mac_count.pdf")
# my_plot.plot_latency(time_table, gemm_dims, "fig_latency_normalize_mac_count.pdf")