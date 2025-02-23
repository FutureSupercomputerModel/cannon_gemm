from cannon_gemm.GEMM.arch_base import Arch_base, Log
from cannon_gemm.Leaf_Modeling.src.leaf_interface import run_leaf_modeling
import math
from cannon_gemm.helper.myMath import *
class Leaf(Arch_base):
    # pe_arr_dim = 200.0
    # buffer_size = 20.0*1024*1024 #20MB
    # buffer_width = 64.0 #element per ns
    
    # pe_freq = 4.0 #GHz
    # nJ_per_mac = 0.38
    # buffer_freq = 4.0
    # interconnect_nJ_per_bit = 0.1
    # buffer_nJ_per_bit = 500
    # bytes_per_element = 2

    # min_gemm_size = pe_arr_dim
    # buffer_bw = buffer_width*buffer_freq/8.0 #bytes per ns

    def __init__(self, pe_arr_dim:float, buffer_size:str, buffer_bw:str, pe_freq:float, E_per_mac:float, interconnect_E_per_bit:float, buffer_E_per_bit:float, bytes_per_element:int, buffer_bit_area:float, mac_area:float, is_systolic=True, is3d=False) -> None:
        self.pe_arr_dim = pe_arr_dim
        self.buffer_size_bytes = str2bytes(buffer_size)
        self.buffer_size_elems = self.buffer_size_bytes/bytes_per_element
        self.buffer_bw_GBps = str2GBps(buffer_bw)
        self.buffer_bw = self.buffer_bw_GBps/bytes_per_element #elements per ns
        self.pe_freq = pe_freq
        self.nJ_per_mac = str2energy(E_per_mac)
        self.interconnect_nJ_per_bit = str2energy(interconnect_E_per_bit)
        self.buffer_nJ_per_bit = str2energy(buffer_E_per_bit)
        self.bytes_per_element = bytes_per_element
        self.total_static_W = 0
        self.is_systolic = is_systolic


        self.min_gemm_size = self.pe_arr_dim
        self.child_arch = None
        self.level = 0
        self.log = Log()

        self.buffer_area = self.buffer_size_bytes*8*buffer_bit_area
        self.mac_area = self.pe_arr_dim*self.pe_arr_dim*mac_area
        sram_layers = 5.0
        compute_layers = 1.0
        if is3d:
            self.total_chip_area = max(self.mac_area/compute_layers, self.buffer_area/sram_layers)
        else:
            self.total_chip_area = (self.mac_area + self.buffer_area)/0.54
        
    
    def to_dict(self):
        return {
            "pe_arr_dim": self.pe_arr_dim,
            "buffer_size": self.buffer_size_bytes,
            "buffer_bw": self.buffer_bw_GBps,
            "pe_freq": self.pe_freq,
            "E_per_mac": self.nJ_per_mac,
            "interconnect_E_per_bit": self.interconnect_nJ_per_bit,
            "buffer_E_per_bit": self.buffer_nJ_per_bit,
            "bytes_per_element": self.bytes_per_element,
            "min_gemm_size": self.min_gemm_size,
            "buffer_area": self.buffer_area,
            "mac_area": self.mac_area,
            "total_chip_area": self.total_chip_area
        }
    
    def update_data_transfer_log_recursively(self, num_iter):
        self.log.update_data_transfer(num_iter)

    def update_latency_log_recursively(self, num_iter):
        self.log.update_latency(num_iter)

    def print(self):
        self.debugprint(f"total_chip_area: {self.total_chip_area/1e8}cm^2 (mac area: {self.mac_area/1e8}, buffer area: {self.buffer_area/1e8}), pe_arr_dim: {self.pe_arr_dim}, buffer_size: {bytes2str(self.buffer_size_bytes)}, buffer_bw: {GBps2str(self.buffer_bw_GBps)}, "
                f"pe_freq: {self.pe_freq}GHz,  E_per_mac: {energy2str(self.nJ_per_mac)}, "
                f"interconnect_E_per_bit: {energy2str(self.interconnect_nJ_per_bit)}, buffer_E_per_bit: {energy2str(self.buffer_nJ_per_bit)}, min_gemm_size: {self.min_gemm_size}, precision: {self.bytes_per_element*8},"
                f"max_gemm_size: {self.get_max_gemm_size()}")
    
    def print_log(self):
        self.debugprint(self.log.toString())

    def OutputStationary(self, m,n,K,cycle_time, bw, debug):
        t_compute = (2*m + n + K - 2)*cycle_time
        if debug:
            print(f"t_compute: {t_compute} = (2*{m} + {n} + {K} - 2)*{cycle_time}")
        t_load = (m*K+K*n)/bw
        t_store = m*n/bw
        t_total = max(t_compute, t_load + t_store)
        load_elems = m*K+K*n
        store_elems = m*n
        load_store_elems = load_elems + store_elems
        return t_total, t_compute, t_load, t_store, load_store_elems
    def scale_sim_systolic(self, M,K,N, debug):
        

        bw = self.buffer_bw
        d = self.pe_arr_dim
        cycle_time = 1/self.pe_freq
        if M > d and N > d:
            m = M%d
            n = N%d

            t_DD, t_DD_compute, t_DD_load, t_DD_store, DD_elems = self.OutputStationary(d,d,K,cycle_time, bw, debug)
            t_Dn, t_Dn_compute, t_Dn_load, t_Dn_store, Dn_elems = self.OutputStationary(d,n,K,cycle_time, bw, debug)
            t_mD, t_mD_compute, t_mD_load, t_mD_store, mD_elems = self.OutputStationary(m,d,K,cycle_time, bw, debug)
            t_mn, t_mn_compute, t_mn_load, t_mn_store, mn_elems = self.OutputStationary(m,n,K,cycle_time, bw, debug)
           
            
            T_total = math.floor(M/d)*math.floor(N/d)*t_DD + math.floor(M/d)*t_Dn + math.floor(N/d)*t_mD + t_mn 
            if debug:
                print(f"{math.floor(M/d)*math.floor(N/d)} x t_DD: {t_DD} + {math.floor(M/d)} x t_Dn: {t_Dn} + {math.floor(N/d)} * t_mD: {t_mD} + t_mn: {t_mn} = {T_total}")
            T_compute = math.floor(M/d)*math.floor(N/d)*t_DD_compute + math.floor(M/d)*t_Dn_compute + math.floor(N/d)*t_mD_compute + t_mn_compute
            T_load = math.floor(M/d)*math.floor(N/d)*t_DD_load + math.floor(M/d)*t_Dn_load + math.floor(N/d)*t_mD_load + t_mn_load
            T_store = math.floor(M/d)*math.floor(N/d)*t_DD_store + math.floor(M/d)*t_Dn_store + math.floor(N/d)*t_mD_store + t_mn_store

            elems_accessed = math.floor(M/d)*math.floor(N/d)*DD_elems + math.floor(M/d)*Dn_elems + math.floor(N/d)*mD_elems + mn_elems

        elif M > d:
            m = M%d
            t_DN, t_DN_compute, t_DN_load, t_DN_store, DN_elems = self.OutputStationary(d,N,K,cycle_time, bw, debug)
            t_mN, t_mN_compute, t_mN_load, t_mN_store, mN_elems = self.OutputStationary(m,N,K,cycle_time, bw, debug)
            T_total = math.floor(M/d)*t_DN + t_mN
            T_compute = math.floor(M/d)*t_DN_compute + t_mN_compute
            T_load = math.floor(M/d)*t_DN_load + t_mN_load
            T_store = math.floor(M/d)*t_DN_store + t_mN_store
            elems_accessed = math.floor(M/d)*DN_elems + mN_elems
        
        elif N > d:
            n = N%d
            t_MD, t_MD_compute, t_MD_load, t_MD_store, MD_elems = self.OutputStationary(M,d,K,cycle_time, bw, debug)
            t_Mn, t_Mn_compute, t_Mn_load, t_Mn_store, Mn_elems = self.OutputStationary(M,n,K,cycle_time, bw, debug)
            T_total = math.floor(N/d)*t_MD + t_Mn
            T_compute = math.floor(N/d)*t_MD_compute + t_Mn_compute
            T_load = math.floor(N/d)*t_MD_load + t_Mn_load
            T_store = math.floor(N/d)*t_MD_store + t_Mn_store
            elems_accessed = math.floor(N/d)*MD_elems + Mn_elems
           
        else:
            t_MN, t_MN_compute, t_MN_load, t_MN_store, MN_elems = self.OutputStationary(M,N,K,cycle_time, bw, debug)
            T_total = t_MN
            T_compute = t_MN_compute
            T_load = t_MN_load
            T_store = t_MN_store
            elems_accessed = MN_elems

        compute_energy = M*K*N*self.nJ_per_mac
        buffer_access_bits = elems_accessed*self.bytes_per_element*8
        buffer_energy = buffer_access_bits*(self.interconnect_nJ_per_bit + self.buffer_nJ_per_bit)
        energy = compute_energy + buffer_energy

        #update logs
        self.log.mac += M*K*N
        self.log.buffer_access += buffer_access_bits
        self.log.interconnect_bits += buffer_access_bits
        self.log.buffer_E_nJ += buffer_access_bits * self.buffer_nJ_per_bit
        self.log.interconnect_E_nJ += buffer_access_bits * self.interconnect_nJ_per_bit
        self.log.mac_E_nJ += M*K*N * self.nJ_per_mac
        self.log.T_prep += T_load
        self.log.T_compute += T_compute
        self.log.T_send += 0
        self.log.T_store += T_store

        if debug:
            self.debugprint("------------------GEMM------------------")
            self.debugprint(f"GEMM: {M},{K},{N}")
            self.debugprint(f"latency: {T_total}, T_compute: {T_compute}, T_buffer: {T_load+T_store}")
            self.debugprint(f"energy: {energy2str(energy)}, E_compute: {energy2str(compute_energy)}, E_buffer: {energy2str(buffer_energy)}")
            self.debugprint(f"buffer load store bits: {buffer_access_bits}")
            self.debugprint(f"interconnect transfer bits: {buffer_access_bits}")
        
        return energy, T_total
    #energy in nJ, time in ns
    def run_leaf_modeling_fallback(self, M, K, N, debug=False):
        if self.is_systolic:
            energy, time = self.scale_sim_systolic(M,K,N, debug)
            return energy, time
        else:
            compute_time = M*K*N/self.pe_arr_dim/self.pe_arr_dim/self.pe_freq
            buffer_time = (M*K+K*N+M*N)/self.buffer_bw
            time = max(compute_time, buffer_time)
                
            # energy = (M*K*N*self.nJ_per_mac + (M*K+K*N+M*N)*(self.interconnect_nJ_per_bit + self.buffer_nJ_per_bit))
            compute_energy = M*K*N*self.nJ_per_mac
            buffer_access_bits = (M*K+K*N+M*N)*self.bytes_per_element*8
            buffer_energy = buffer_access_bits*(self.interconnect_nJ_per_bit + self.buffer_nJ_per_bit)
            energy = compute_energy + buffer_energy

            #update logs
            self.log.mac += M*K*N
            self.log.buffer_access += buffer_access_bits
            self.log.interconnect_bits += buffer_access_bits
            self.log.buffer_E_nJ += self.log.buffer_access * self.buffer_nJ_per_bit
            self.log.interconnect_E_nJ += self.log.interconnect_bits * self.interconnect_nJ_per_bit
            self.log.mac_E_nJ += self.log.mac * self.nJ_per_mac
            self.log.T_prep += (M*K+K*N)/self.buffer_bw
            self.log.T_compute += compute_time
            self.log.T_send += 0
            self.log.T_store += M*N/self.buffer_bw
            if debug:
                self.debugprint("------------------GEMM------------------")
                self.debugprint(f"GEMM: {M},{K},{N}")
                self.debugprint(f"latency: {time}, T_compute: {compute_time}, T_buffer: {buffer_time}")
                self.debugprint(f"energy: {energy2str(energy)}, E_compute: {energy2str(compute_energy)}, E_buffer: {energy2str(buffer_energy)}")
                self.debugprint(f"buffer load store bits: {buffer_access_bits}")
                self.debugprint(f"interconnect transfer bits: {buffer_access_bits}")
            
            return energy, time
    
    def get_gemm_latency_energy(self, M:int, K:int, N:int, debug:bool, general_tiling:bool):
        # M = math.ceil(M/(self.min_gemm_size)) * self.min_gemm_size
        # K = math.ceil(K/(self.min_gemm_size)) * self.min_gemm_size
        # N = math.ceil(N/(self.min_gemm_size)) * self.min_gemm_size
        if debug:
            #report buffer usage
            self.debugprint("------------------Tiling------------------")
            self.debugprint(f"buffer usage: {bytes2str((M*K+K*N+M*N)*self.bytes_per_element)}/{bytes2str(self.buffer_size_bytes)}")
        # leaf_tech = 'cmos-gemm-7nm'
        # energy, cycles = run_leaf_modeling(leaf_tech, M, K, N)
        # time = cycles/self.pe_freq
        energy, time = self.run_leaf_modeling_fallback(M, K, N, debug)
        # if debug:
        #     self.debugprint(f"Leaf energy (nJ): {energy}, Leaf time (ns): {time}")
        assert M*K+K*N+M*N<=self.buffer_size_elems
        # return max(M*K*N/self.pe_arr_dim/self.pe_arr_dim/self.pe_freq, M*K+K*N+M*N/self.buffer_bw), M*K*N*self.nJ_per_mac
        return time, energy
    
    def get_max_gemm_size(self):
        min_problem_size_per_leaf = self.min_gemm_size*self.min_gemm_size*3
        scale_up_factor = math.floor(math.sqrt(self.buffer_size_elems / min_problem_size_per_leaf))
        return (self.min_gemm_size*scale_up_factor, self.min_gemm_size*scale_up_factor, self.min_gemm_size*scale_up_factor)
    
    def reset_log(self):
        self.log = Log()
