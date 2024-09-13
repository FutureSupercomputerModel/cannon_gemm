from cannon_gemm.GEMM.arch_base import Arch_base
from cannon_gemm.Leaf_Modeling.src.leaf_interface import run_leaf_modeling

# from GEMM.arch_base import Arch_base
# from Leaf_Modeling.src.leaf_interface import run_leaf_modeling

# from arch_base import Arch_base
# from cannon_gemm.Leaf_Modeling.src.leaf_interface import run_leaf_modeling

import math
class Leaf(Arch_base):
    pe_arr_dim = 200.0
    buffer_size = 20.0*1024*1024 #20MB
    buffer_width = 64.0 #element per ns
    
    pe_freq = 4.0 #GHz
    pJ_per_mac = 0.38
    buffer_freq = 4.0
    interconnect_pJ_per_bit = 0.1
    buffer_pJ_per_bit = 500

    bytes_per_element = 2

    min_gemm_size = pe_arr_dim

    def __init__(self, pe_arr_dim:float, buffer_size:float, buffer_width:float, pe_freq:float, pJ_per_mac:float, buffer_freq:float, interconnect_pJ_per_bit:float, buffer_pJ_per_bit:float) -> None:
        self.pe_arr_dim = pe_arr_dim
        self.buffer_size = buffer_size
        self.buffer_width = buffer_width
        self.pe_freq = pe_freq
        self.pJ_per_mac = pJ_per_mac
        self.buffer_freq = buffer_freq
        self.interconnect_pJ_per_bit = interconnect_pJ_per_bit
        self.buffer_pJ_per_bit = buffer_pJ_per_bit

        self.child_arch = None

    def print(self):
        print(f"pe_arr_dim: {self.pe_arr_dim}, buffer_size: {self.buffer_size}, buffer_width: {self.buffer_width},\
                pe_freq: {self.pe_freq},  pJ_per_mac: {self.pJ_per_mac}, buffer_freq: {self.buffer_freq}, \
                interconnect_pJ_per_bit: {self.interconnect_pJ_per_bit}, buffer_pJ_per_bit min_gemm_size: {self.min_gemm_size}, bytes_per_element: {2},\
                max_gemm_size: {self.get_max_gemm_size()}")
    
    def run_leaf_modeling_fallback(self, M , K, N):
        return M*K*N*self.nJ_per_mac, max(M*K*N/self.pe_arr_dim/self.pe_arr_dim/self.pe_freq, M*K+K*N+M*N/self.buffer_bw)

    def get_gemm_latency_energy(self, M:int, K:int, N:int):
        M = math.ceil(M/(self.min_gemm_size)) * self.min_gemm_size
        K = math.ceil(K/(self.min_gemm_size)) * self.min_gemm_size
        N = math.ceil(N/(self.min_gemm_size)) * self.min_gemm_size

        # leaf_tech = 'cmos-gemm-7nm'
        # energy, cycles = run_leaf_modeling(leaf_tech, M, K, N)
<<<<<<< HEAD
        energy, time = run_leaf_modeling_fallback(self, M, K, N)
        print(f"Leaf energy (nJ): {energy}, Leaf time (ns): {time}")
=======
        print(f"Leaf Problem : {int(M)} {int(K)} {int(N)}")
        energy, cycles = self.run_leaf_modeling_fallback( int(M), int(K), int(N))
        leaf_time = cycles / self.pe_freq #ns
        energy = energy * 1e9 #nJ
        # print(f"Leaf energy: {energy}, Leaf time (ns): {leaf_time}")
>>>>>>> e1c58019c984d1b6ae4e6eae57f0a4296aef4a41
        #report buffer usage
        print(f"buffer usage: {(M*K+K*N+M*N)*self.bytes_per_element}/{self.buffer_size}")
        assert M*K+K*N+M*N<=self.buffer_size
        # return max(M*K*N/self.pe_arr_dim/self.pe_arr_dim/self.pe_freq, M*K+K*N+M*N/self.buffer_bw), M*K*N*self.nJ_per_mac
        return time, energy
    
    def get_max_gemm_size(self):
        min_problem_size_per_leaf = self.min_gemm_size*self.min_gemm_size*3*self.bytes_per_element
        scale_up_factor = math.floor(math.sqrt(self.buffer_size / min_problem_size_per_leaf))
        return (self.min_gemm_size*scale_up_factor, self.min_gemm_size*scale_up_factor, self.min_gemm_size*scale_up_factor)
