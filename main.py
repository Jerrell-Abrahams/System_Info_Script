from bs4 import BeautifulSoup
import psutil
import cpuinfo
import re
import os
import subprocess



# A function that converts bytes to gigabytes
def bytes_to_gb(byte):
    return byte * 9.31 * 10**-10

# Creates the battery report and saves it to the current directory
battery_report = os.system(rf"powercfg /batteryreport")


# Accesses the battery report and extracts the needed values
with open("battery-report.html", encoding="UTF-8") as file:
    soup = BeautifulSoup(file, 'html.parser')
    battery_design = soup.html.body.find_all("table")[1].find_all("tr")[5].find_all("td")[1].text
    battery_charge = soup.html.body.find_all("table")[1].find_all("tr")[7].find_all("td")[1].text
    battery_charge_capacity = "".join(re.findall(r'\d+', battery_charge))
    battery_design_capacity = "".join(re.findall(r'\d+', battery_design))
    file.close()



battery_health = round(int(battery_charge_capacity) / int(battery_design_capacity) * 100)  # Battery health in percentage
cpu = cpuinfo.get_cpu_info()["brand_raw"]  # Cpu details / generation
ram = round(bytes_to_gb(psutil.virtual_memory()[0]))  # Amount of Ram installed
processor_type = cpuinfo.get_cpu_info()["bits"]  # Type of processor 32-bit or 64-bit
video_controller = " ".join(re.split("\W+", subprocess.run("wmic path win32_VideoController get name", capture_output=True, text=True).stdout)[1:])
operating_sys = " ".join(re.split("\W+", str(subprocess.run("wmic os get caption", capture_output=True, text=True).stdout))[1:-1])
hdd = round(bytes_to_gb(psutil.disk_usage('/').total))  # Size of C:\
num_of_cores = re.findall('\d', subprocess.run('wmic cpu get numberofcores', capture_output=True, text=True).stdout)[0]
peripherals = re.split("\W+\s", str(subprocess.run("wmic portconnector get externalreferencedesignator", capture_output=True, text=True).stdout))[1:-1]
system_model = ' '.join(re.split("\W+",subprocess.run("wmic csproduct get name", shell=True, text=True, capture_output=True).stdout)[1:-1])
system_brand = ' '.join(re.split("\W+",subprocess.run("wmic csproduct get vendor", shell=True, text=True, capture_output=True).stdout)[1:-1])
current_path = os.getcwd()


# Deletes the battery report after use
os.remove("battery-report.html")





