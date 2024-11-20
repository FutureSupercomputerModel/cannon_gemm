import numpy as np
from GEMM.arch import Arch
from GEMM.leaf import Leaf
from GEMM.arch import top_level_gemm

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
imec_blade = Arch(mesh_dim=8.0, 
                mesh_bw=f'{73.34}TBps', 
                buffer_size="256GB", 
                buffer_bw='30.0TBps', 
                mesh_E_per_bit='5e-4pJ', 
                buffer_E_per_bit=f'{22*0.029}pJ', 
                buffer_static_W_per_bit=f'{22*1.33}pW',
                sc_to_cryo_E_per_bit="0.4pJ",
                cryo_to_sc_E_per_bit="4.24pJ",
                child_arch=imec_leaf)
imec_node = Arch(mesh_dim=8.0, 
                mesh_bw='1PBps', 
                buffer_size="8TB", 
                buffer_bw='3.0PBps', 
                mesh_E_per_bit='5e-3pJ', 
                buffer_E_per_bit=f'{0}pJ', 
                buffer_static_W_per_bit=f'{0}pW',
                sc_to_cryo_E_per_bit="0pJ",
                cryo_to_sc_E_per_bit="0pJ",
                child_arch=imec_blade)

# m,k,n = (90,90,90)
# m,k,n = (2**19, 2**19, 2**19)
# m,k,n = (1024, 1024, 1024)
m,k,n = (8192, 8192, 8192)
# m,k,n = 90*200*64,90*200*64,90*200*64
T, E, T_mem, T_communicate, T_compute, log = top_level_gemm(m,k,n, imec_node, debug=True, general_tiling=True)
print(f"top_level gemm returns: {T}, {E}, {T_mem}, {T_communicate}, {T_compute}")
print(log)

