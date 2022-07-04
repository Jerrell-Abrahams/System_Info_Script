import platform
import psutil
import cpuinfo
import os


hdd_type = os.system('cmd /k "wmic diskdrive get model"')

print(hdd_type)

def bytes_to_gb(bytes):
    return (bytes * 9.31 * 10**-10)



cpu = cpuinfo.get_cpu_info()["brand_raw"]
ram = psutil.virtual_memory()

processor_type = cpuinfo.get_cpu_info()["bits"]

os = platform.uname().system + " " + platform.uname().release
hdd = psutil.disk_usage('/').total

print(psutil.disk_partitions())