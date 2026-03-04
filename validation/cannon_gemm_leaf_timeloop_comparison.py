import numpy as np
import arch_lib
from GEMM.arch import top_level_gemm


# gemm_values = [
#     (1000,3000,400), (400,200,400), (400,400,200), (1000,400,3000), (1000,3000,1600),
#     (1000,1600,3000),(400,3000,1600),(400,3000,2400),(400,2400,3000),(600,3000,1600),
#     (600,3000,2400),(600,2400,3000),(1000,3000,1800),(1000,1800,3000),(2000,3000,800),
#     (2000,1600,2000),(2000,2000,1600),(2000,1600,1600),(1200,3000,1600),(400,1600,3000),
#     (400,3000,2000),(400,5800,1000),(600,1600,3000),(600,3000,2000),(600,5800,1000),
#     (3800,1600,800),(1200,1600,3000),(400,3000,800),(400,800,3000),(600,3000,800),
#     (600,800,3000),(1000,3000,800),(1000,800,3000),(2000,800,3000),(3800,800,1600)]
# gemm_values = [
#     (1000,3000,400), (400,200,400)]


gemm_values = [
    (1000, 1000, 1000),  
    (900, 1000, 1100),   
    (800, 1200, 1000),   
    (1100, 1100, 900),   
    (1000, 1100, 1100),  
    (1200, 1200, 1000),  
    (1300, 1100, 900),   
    (1000, 1300, 1100), 
    (800, 900, 1200),    
    (850, 950, 1050),    
    (1000, 1200, 850),   
    (1100, 900, 850),    
    (1000, 850, 1100),   
    (950, 1000, 1100),    
    (1500, 1500, 1500),
    (1600, 1500, 1400),   
    (1400, 1600, 1500), 
    (2000, 1200, 1300),   
    (1300, 2000, 1200), 
    (1800, 1500, 1100),   
    (1500, 1800, 1100), 
    (1700, 1400, 1300),   
    (1400, 1700, 1300), 
    (1600, 1600, 1300),   
    (1600, 1300, 1600), 
    (1800, 1800, 1800),   
    (2000, 2000, 1500),   
    (2100, 1500, 1400),   
    (1600, 1700, 1500),   
    (1700, 1700, 1500)    
]

# gemm_values = [
#     (400, 2000, 3400),
#     (400, 2400, 3200),
#     (400, 3000, 2600),
#     (400, 3600, 1800),
#     (450, 2000, 3400),
#     (450, 3200, 2000),
#     (500, 1600, 3600),
#     (500, 1800, 3200),
#     (500, 2400, 2400),
#     (500, 3200, 1800),
#     (500, 3600, 1600),
#     (600, 1500, 3200),
#     (600, 1600, 3000),
#     (600, 2000, 2400),
#     (600, 2400, 2000),
#     (600, 3000, 1600),
#     (600, 3200, 1500),
#     (750, 1200, 3200),
#     (750, 1600, 2400),
#     (750, 2400, 1600),
#     (750, 3200, 1200),
#     (800, 1000, 3600),
#     (800, 1200, 3000),
#     (800, 1500, 2400),
#     (800, 1800, 2000),
#     (800, 2000, 1800),
#     (800, 2400, 1500),
#     (800, 3000, 1200),
#     (800, 3600, 1000),
#     (900, 1000, 3200)
# ]

# m,k,n = (400,400,400)
# # m,k,n = (37800.0, 37800.0, 37800.0)
# m,k,n = 90*200*64,90*200*64,90*200*64

import re
import json
import io
import sys

# Redirect stdout to capture print statements from top_level_gemm
class CaptureOutput:
    def __enter__(self):
        self.new_out = io.StringIO()
        self.old_out = sys.stdout
        sys.stdout = self.new_out
        return self

    def __exit__(self, *args):
        self.output = self.new_out.getvalue()
        sys.stdout = self.old_out

# Initialize a dictionary to store the data
results = {}

# Capture the output of top_level_gemm and still print to the terminal
full_output = ""
for m, k, n in gemm_values:
    with CaptureOutput() as capture:
        top_level_gemm(m,k,n, arch_lib.leaf_imec, debug=True, general_tiling=True) # Assume this function uses m, k, n internally
    captured_output = capture.output
    full_output += captured_output

    # print("FINDING MATCHES ...............")
    # Find matches for "top level GEMM" line in the current output
    gemm_match = re.search(r"top level GEMM: (\d+),(\d+),(\d+)", captured_output)
    if gemm_match:
        val1, val2, val3 = gemm_match.groups()
        key = f"{val1}_{val3}_{val2}"

        # Extract the latency value
        latency_match = re.search(r"latency: ([\d.]+)", captured_output)
        latency = float(latency_match.group(1)) if latency_match else None
        # print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~ Latency: {latency} ~~~~~~~~~~~~~~~~~")

        # Extract the energy value and strip the unit
        energy_match = re.search(r"energy: ([\d.]+)uJ", captured_output)
        energy = float(energy_match.group(1)) if energy_match else None
        # print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~ Energy: {energy} ~~~~~~~~~~~~~~~~~")

        # Store in results if both values are found
        if latency is not None and energy is not None:
            results[key] = {
                "energy": energy,
                "latency": latency
            }

# Print the full output to the terminal for sanity
print(full_output)

# Write the results to a JSON file
output_file = "systolic_cache.json"
with open(output_file, "w") as json_file:
    json.dump(results, json_file, indent=4)

print(f"Data has been written to {output_file}")