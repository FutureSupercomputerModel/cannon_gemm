def ceildiv(a, b):
    return -(a // -b)

import math

# def bytes2str(size_bytes):
#    if size_bytes == 0:
#        return "0B"
#    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
#    i = int(math.floor(math.log(size_bytes, 1024)))
#    p = math.pow(1024, i)
#    s = round(size_bytes / p, 2)
#    return "%s %s" % (s, size_name[i])

def str2bytes(size_string):
    if size_string[-1] == 'B':
        size_string = size_string[:-1]
    size = float(size_string[:-1])
    if 'K' in size_string:
        size *= 1024
    elif 'M' in size_string:
        size *= 1024*1024
    elif 'G' in size_string:
        size *= 1024*1024*1024
    elif 'T' in size_string:
        size *= 1024*1024*1024*1024
    elif 'P' in size_string:
        size *= 1024*1024*1024*1024*1024
    return size

def bytes2str(size_bytes):
    if size_bytes< 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024*1024:
        return f"{size_bytes/1024}KB"
    elif size_bytes < 1024*1024*1024:
        return f"{size_bytes/1024/1024}MB"
    elif size_bytes < 1024*1024*1024*1024:
        return f"{size_bytes/1024/1024/1024}GB"
    elif size_bytes < 1024*1024*1024*1024*1024:
        return f"{size_bytes/1024/1024/1024/1024}TB"
    elif size_bytes < 1024*1024*1024*1024*1024*1024:
        return f"{size_bytes/1024/1024/1024/1024/1024}PB"
    else:
        return f"{size_bytes/1024/1024/1024/1024/1024/1024}EB"

def str2GBps(bw_string):
    if 'PBps' in bw_string:
        bw = float(bw_string[:-4]) * 1024 * 1024
    elif 'TBps' in bw_string:
        bw = float(bw_string[:-4]) * 1024
    elif 'GBps' in bw_string:
        bw = float(bw_string[:-4])
    elif 'TBps' in bw_string:
        bw = float(bw_string[:-4]) * 1024
    elif 'MBps' in bw_string:
        bw = float(bw_string[:-4]) / 1024
    elif 'KBps' in bw_string:
        bw = float(bw_string[:-4]) / (1024*1024)
    elif 'Bps' in bw_string:
        bw = float(bw_string[:-3]) / (1024*1024*1024)
    return bw
def GBps2str(bw):
    if bw < 0.000001:
        return f"{bw*1024*1024*1024}Bps"
    elif bw < 0.001:
        return f"{bw*1024*1024}KBps"
    elif bw < 1:
        return f"{bw*1024}MBps"
    elif bw < 1024:
        return f"{bw}GBps"
    elif bw < 1024*1024:
        return f"{bw/1024}TBps"
    elif bw < 1024*1024*1024:
        return f"{bw/1024/1024}PBps"
    else:
        return f"{bw/1024/1024/1024}PBps"

def str2energy(energy_string):
    if 'aJ' in energy_string:
        energy = float(energy_string[:-2]) / 1000000000
    elif 'fJ' in energy_string:
        energy = float(energy_string[:-2]) / 1000000
    elif 'pJ' in energy_string:
        energy = float(energy_string[:-2]) / 1000
    elif 'nJ' in energy_string:
        energy = float(energy_string[:-2])
    elif 'uJ' in energy_string:
        energy = float(energy_string[:-2]) * 1000
    elif 'mJ' in energy_string:
        energy = float(energy_string[:-2]) * 1000000
    elif 'J' in energy_string:
        energy = float(energy_string[:-1]) * 1000000000
    return energy

def energy2str(energy):
    if energy < 1e-3:
        return f"{energy*1000000}fJ"
    elif energy < 1:
        return f"{energy*1000}pJ"
    elif energy < 1000:
        return f"{energy}nJ"
    elif energy < 1000000:
        return f"{energy/1000}uJ"
    elif energy < 1000000000:
        return f"{energy/1000000}mJ"
    else:
        return f"{energy/1000000000}J"

#returns W from string representation of power
def str2power(power):
    if 'aW' in power:
        power = float(power[:-2]) / 1E18
    elif 'fW' in power:
        power = float(power[:-2]) / 1E15
    elif 'pW' in power:
        power = float(power[:-2]) / 1E12
    elif 'nW' in power:
        power = float(power[:-2]) / 1E9
    elif 'uW' in power:
        power = float(power[:-2]) / 1E6
    elif 'mW' in power:
        power = float(power[:-2]) / 1E3
    elif 'W' in power:
        power = float(power[:-1])
    return power

def power2str(power):
    if power < 1E-15:
        return f"{power*1E18}aW"
    elif power < 1E-12:
        return f"{power*1E15}fW"
    elif power < 1E-9:
        return f"{power*1E12}pW"
    elif power < 1E-6:
        return f"{power*1E9}nW"
    elif power < 1E-3:
        return f"{power*1E6}uW"
    elif power < 1:
        return f"{power*1E3}mW"
    else:
        return f"{power}W"

# Calculon helper 
def convert_to_bytes(size_str):
    # Dictionary of unit multipliers
    unit_multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
        'PB': 1024**5
    }
    # Extract number and unit from the string
    size = float(''.join([c for c in size_str if c.isdigit() or c == '.']))
    unit = ''.join([c for c in size_str if c.isalpha()]).upper()
    # Multiply the size by the corresponding unit multiplier
    if unit in unit_multipliers:
        return size * unit_multipliers[unit]
    else:
        raise ValueError(f"Unknown unit '{unit}' in size string '{size_str}'")