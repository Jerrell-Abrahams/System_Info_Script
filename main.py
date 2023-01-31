from bs4 import BeautifulSoup
import os
import re
import subprocess
from PIL import Image, ImageDraw, ImageFont
import time

print("Starting program...")
current_path = os.getcwd()

SPECSFONT = 0
HEADINGFONT = 0
PERIPHERALSFONT = 0


def readSettings():
    global SPECSFONT, HEADINGFONT, PERIPHERALSFONT
    try:
        with open("settings.txt", "r") as settings:
            print("--> Retrieving font sizes")
            lines = settings.readlines()
            SPECSFONT = re.findall(r'\d+', lines[0])[0]
            HEADINGFONT = re.findall(r'\d+', lines[1])[0]
            PERIPHERALSFONT = re.findall(r'\d+', lines[2])[0]
    except:
        print("--> Using default font sizes, could not find settings.txt")
        SPECSFONT = 50 
        HEADINGFONT = 65
        PERIPHERALSFONT = 35        


def add_info():
    try:
        with Image.open("put_wallpaper_here/wallpaper.jpg", "r") as img:
            print("--> Drawing all specs on image")
            width, height = img.size

            processed_img = ImageDraw.Draw(img)

            
            font = ImageFont.truetype(font="verdana.ttf", size=int(SPECSFONT))
            font_system = ImageFont.truetype(font="verdana.ttf", size=int(HEADINGFONT))
            font_peripherals = ImageFont.truetype(font="verdana.ttf", size=int(PERIPHERALSFONT))

            processed_img.text((width / 2, height / 6), text=f"{system_brand}", font=font_system, anchor="ms")
            processed_img.text((width / 2, height / 6 + 100), text=f"{system_model}", font=font_system, anchor="ms")
            processed_img.text((width / 9, height / 3 + 50), text=f"Processor: {cpu}", font=font)
            processed_img.text((width / 9, height / 3 + 150), text=f"Installed memory: {ram} GB " + ram_type + " " + ram_speed, font=font)
            processed_img.text((width / 9, height / 3 + 250), text=f"System type: {operating_sys_arch}-bit Operating System, x{processor_type}-based processor", font=font)
            processed_img.text((width / 9, height / 3 + 350), text=f"OS: {operating_sys}", font=font)
            processed_img.text((width / 9, height / 3 + 450), text=f"HDD size: {hdd} GB {hdd_type}", font=font)
            processed_img.text((width / 9, height / 3 + 550), text=f"Battery health: {battery_health} %", font=font)
            processed_img.text((width / 9, height / 3 + 650), text=f"Video controller: {video_controller}", font=font)
            processed_img.text((width / 1.6, height / 3 + 50), text=f"Number of cores: {num_of_cores} Core(s)", font=font)
            processed_img.text((width / 1.6, height / 3 + 150), text=f"Peripherals:", font=font)

            padding = 250
            for port in peripherals:
                processed_img.text((width / 1.37, height / 3 + padding), text=f"{port}", font=font_peripherals)
                padding += 90
            print("--> Saving processed image to project file")
            img.save(fr"{current_path}\specs_image.png", format="PNG")
    except:
        print("--! Failed to get Background image")



def update_screen():
    # Change background image
    print("--> Updating background image")
    current_path = os.getcwd()
    image_loci = f'"{current_path}\specs_image.jpg"'
    print("--> location: ", image_loci)
    time.sleep(1)
    subprocess.run(f'reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /d {image_loci} /f', capture_output=True)
    subprocess.run("RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters")
    print("Done!")



# A function that converts bytes to gigabytes
def bytes_to_gb(byte):
    return byte * 9.31 * 10**-10

# Creates the battery report and saves it to the current directory
print("--> Creating the battery report")
battery_report = subprocess.run(rf'powercfg /batteryreport /output "{current_path}\battery-report.html"', capture_output=True)


# Accesses the battery report and extracts the needed values
with open(rf"{current_path}\battery-report.html", encoding="UTF-8") as file:
    print("--> Parsing the battery report")
    soup = BeautifulSoup(file, 'html.parser')
    battery_design = soup.html.body.find_all("table")[1].find_all("tr")[5].find_all("td")[1].text
    battery_charge = soup.html.body.find_all("table")[1].find_all("tr")[7].find_all("td")[1].text
    battery_charge_capacity = "".join(re.findall(r'\d+', battery_charge))
    battery_design_capacity = "".join(re.findall(r'\d+', battery_design))
    file.close()


print("--> Retrieving specs of machine")
total_ram = 0
ram_slots = re.findall(r"\d+", str(subprocess.run("wmic memorychip get capacity", capture_output=True).stdout))

for ram in ram_slots:
    total_ram += int(ram)
battery_health = round(int(battery_charge_capacity) / int(battery_design_capacity) * 100)  # Battery health in percentage
cpu = re.findall("Name\s*(.*\S)\s*", (str(subprocess.run("wmic cpu get name", capture_output=True, text=True).stdout)))[0]
ram = round(bytes_to_gb(total_ram))   # Amount of Ram installed
processor_type = re.findall("\d+", str(subprocess.run("wmic cpu get datawidth", capture_output=True).stdout))[0]  # Type of processor 32-bit or 64-bit
video_controller = " ".join(re.split("\W+", subprocess.run("wmic path win32_VideoController get name", capture_output=True, text=True).stdout)[1:])
operating_sys_arch = re.findall("\d+", str(subprocess.run("wmic os get osarchitecture", capture_output=True).stdout))[0]
operating_sys = " ".join(re.split("\W+", str(subprocess.run("wmic os get caption", capture_output=True, text=True).stdout))[1:-1])
hdd = round(bytes_to_gb(int(re.findall("\d+", str(subprocess.run("wmic diskdrive where 'index=0' get size", capture_output=True).stdout))[-1])))  # Size of C:\
hdd_type = re.findall(r"[A-Z][A-Z][A-Z]", str(subprocess.run("powershell get-physicaldisk | format-table mediatype", capture_output=True).stdout))[0]
num_of_cores = re.findall('\d', subprocess.run('wmic cpu get numberofcores', capture_output=True, text=True).stdout)[0]
peripherals = re.split("\W+\s", str(subprocess.run("wmic portconnector get externalreferencedesignator", capture_output=True, text=True).stdout))[1:-1]
system_model = ' '.join(re.split("\W+",subprocess.run("wmic csproduct get name", text=True, capture_output=True).stdout)[1:-1])
system_brand = ' '.join(re.split("\W+",subprocess.run("wmic csproduct get vendor", text=True, capture_output=True).stdout)[1:-1])
ram_type = ' '.join(re.split("\D+",subprocess.run("wmic memorychip get memorytype", text=True, capture_output=True).stdout))[1:3]
ram_speed = ' '.join(re.split("\D+",subprocess.run("wmic memorychip get speed", text=True, capture_output=True).stdout))[1:5] + " MHz"

match ram_type:
    case "24":
        ram_type = "DDR3"
    case "26":
        ram_type = "DDR4"
    case "21":
        ram_type = "DDR2"
    case "20":
        ram_type = "DDR"
    case "9":
        ram_type = "RAM"
    case "7":
        ram_type = "VRAM"
    case _:
        ram_type = "Unknown"

    




# Deletes the battery report after use
print("--> Removing battery report")
os.remove("battery-report.html")


readSettings()
add_info()
update_screen()



