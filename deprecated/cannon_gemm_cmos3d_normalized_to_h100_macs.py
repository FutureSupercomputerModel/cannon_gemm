from GEMM.arch import Arch
from GEMM.leaf import Leaf
from GEMM.arch import top_level_gemm

leaf_cmos = Leaf(pe_arr_dim=128.0*4, 
                      buffer_size=f'{16.0*16}MB', 
                      buffer_bw = f'{9680}GBps', 
                      pe_freq=4.0, 
                      E_per_mac="0.38pJ", 
                      interconnect_E_per_bit="0.1pJ", 
                      buffer_E_per_bit='0.5fJ', 
                      bytes_per_element=2,
                      buffer_bit_area=0.058,
                      mac_area=550)
blade_cmos = Arch(mesh_dim=1.0, 
                  mesh_bw=f'{9680}GBps', #1000GBps
                  buffer_size="80GB", 
                  buffer_bw='30.0TBps', 
                  mesh_E_per_bit='0.1pJ', 
                  buffer_E_per_bit='0.29pJ', 
                  child_arch=leaf_cmos)
node_cmos = Arch(mesh_dim=1.0, 
                 mesh_bw='1PBps', 
                 buffer_size="8TB", 
                 buffer_bw='3.0PBps', 
                 mesh_E_per_bit='0.1pJ', 
                 buffer_E_per_bit='0.29pJ', 
                 child_arch=blade_cmos)
gemm_sizes = [
    (819, 819, 819),
    # (409600, 409600, 409600),
    # (204800, 204800, 204800),
    # (102400, 102400, 102400),
    # (51200, 51200, 51200),
    # (25600, 25600, 25600),
    # (12800, 12800, 12800),
    # (6400, 6400, 6400),
    # (3200, 3200, 3200),
    # (1600, 1600, 1600),
    # (800, 800, 800),
    # (400, 400, 400),
    # (200, 200, 200)
]
for m,k,n in gemm_sizes:
    _,_,log = top_level_gemm(m,k,n, node_cmos, debug=True, general_tiling=True)
    # print(log)