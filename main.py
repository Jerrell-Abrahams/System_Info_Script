from bs4 import BeautifulSoup
import os
import re
import subprocess
from PIL import Image, ImageDraw, ImageFont
import time

current_path = os.getcwd()





def add_info():
    with Image.open("put_wallpaper_here/wallpaper.jpg", "r") as img:
        width, height = img.size
        processed_img = ImageDraw.Draw(img)
        font = ImageFont.truetype(font="verdana.ttf", size=80)
        font_system = ImageFont.truetype(font="verdana.ttf", size=80)
        font_peripherals = ImageFont.truetype(font="verdana.ttf", size=60)

        processed_img.text((width / 2.05, height / 6), text=f"{system_brand}", font=font_system)
        processed_img.text((width / 2.05, height / 6 + 100), text=f"{system_model}", font=font_system)
        processed_img.text((width / 9, height / 3 + 50), text=f"Processor: {cpu}", font=font)
        processed_img.text((width / 9, height / 3 + 150), text=f"Installed memory: {ram} GB", font=font)
        processed_img.text((width / 9, height / 3 + 250), text=f"System type: {operating_sys_arch}-bit Operating System, x{processor_type}-based processor", font=font)
        processed_img.text((width / 9, height / 3 + 350), text=f"OS: {operating_sys}", font=font)
        processed_img.text((width / 9, height / 3 + 450), text=f"HDD size: {hdd} GB {hdd_type}", font=font)
        processed_img.text((width / 9, height / 3 + 550), text=f"Battery health: {battery_health} %", font=font)
        processed_img.text((width / 9, height / 3 + 650), text=f"Video Controller: {video_controller}", font=font)
        processed_img.text((width / 1.6, height / 3 + 50), text=f"Number of cores: {num_of_cores} Core(s)", font=font)
        processed_img.text((width / 1.6, height / 3 + 150), text=f"Peripherals:", font=font)

        padding = 250
        for port in peripherals:
            processed_img.text((width / 1.37, height / 3 + padding), text=f"{port}", font=font_peripherals)
            padding += 90

        img.save(fr"{current_path}\specs_image.jpg", format="JPEG")



def update_screen():
    # Change background image
    image_loci = f'"{current_path}\specs_image.jpg"'
    subprocess.run(f'reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /d {image_loci} /f')
    time.sleep(3)
    subprocess.run("RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters")


# A function that converts bytes to gigabytes
def bytes_to_gb(byte):
    return byte * 9.31 * 10**-10

# Creates the battery report and saves it to the current directory
battery_report = subprocess.run(rf'powercfg /batteryreport /output "{current_path}\battery-report.html"', shell=True)


# Accesses the battery report and extracts the needed values
with open(rf"{current_path}\battery-report.html", encoding="UTF-8") as file:
    soup = BeautifulSoup(file, 'html.parser')
    battery_design = soup.html.body.find_all("table")[1].find_all("tr")[5].find_all("td")[1].text
    battery_charge = soup.html.body.find_all("table")[1].find_all("tr")[7].find_all("td")[1].text
    battery_charge_capacity = "".join(re.findall(r'\d+', battery_charge))
    battery_design_capacity = "".join(re.findall(r'\d+', battery_design))
    file.close()

total_ram = 0
ram_slots = re.findall(r"\d+", str(subprocess.run("wmic memorychip get capacity", shell=True, capture_output=True).stdout))

for ram in ram_slots:
    total_ram += int(ram)
battery_health = round(int(battery_charge_capacity) / int(battery_design_capacity) * 100)  # Battery health in percentage
cpu = re.findall("Name\s*(.*\S)\s*", (str(subprocess.run("wmic cpu get name", shell=True, capture_output=True, text=True).stdout)))[0]
ram = round(bytes_to_gb(total_ram))   # Amount of Ram installed
processor_type = re.findall("\d+", str(subprocess.run("wmic cpu get datawidth", capture_output=True, shell=True).stdout))[0]  # Type of processor 32-bit or 64-bit
video_controller = " ".join(re.split("\W+", subprocess.run("wmic path win32_VideoController get name", capture_output=True, text=True).stdout)[1:])
operating_sys_arch = re.findall("\d+", str(subprocess.run("wmic os get osarchitecture", capture_output=True, shell=True).stdout))[0]
operating_sys = " ".join(re.split("\W+", str(subprocess.run("wmic os get caption", capture_output=True, text=True).stdout))[1:-1])
hdd = round(bytes_to_gb(int(re.findall("\d+", str(subprocess.run("wmic diskdrive get size", shell=True, capture_output=True).stdout))[0])))  # Size of C:\
hdd_type = re.findall(r"[A-Z][A-Z][A-Z]", str(subprocess.run("powershell get-physicaldisk | format-table mediatype", capture_output=True).stdout))[0]
num_of_cores = re.findall('\d', subprocess.run('wmic cpu get numberoflogicalprocessors', capture_output=True, text=True).stdout)[0]
peripherals = re.split("\W+\s", str(subprocess.run("wmic portconnector get externalreferencedesignator", capture_output=True, text=True).stdout))[1:-1]
system_model = ' '.join(re.split("\W+",subprocess.run("wmic csproduct get name", shell=True, text=True, capture_output=True).stdout)[1:-1])
system_brand = ' '.join(re.split("\W+",subprocess.run("wmic csproduct get vendor", shell=True, text=True, capture_output=True).stdout)[1:-1])


# Deletes the battery report after use
os.remove("battery-report.html")

add_info()
update_screen()



