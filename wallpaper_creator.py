from PIL import Image, ImageDraw, ImageFont
import main
import subprocess

specs = main

def add_info():
    with Image.open("1127004.jpg", "r") as img:
        width, height = img.size
        processed_img = ImageDraw.Draw(img)
        font = ImageFont.truetype(font="verdana.ttf", size=80)
        font_peripherals = ImageFont.truetype(font="verdana.ttf", size=60)

        processed_img.text((width / 2.05, height / 6), text=f"{specs.system_brand}", font=font)
        processed_img.text((width / 2.05, height / 6 + 100), text=f"{specs.system_model}", font=font)
        processed_img.text((width / 9, height / 3 + 50), text=f"Processor: {specs.cpu}", font=font)
        processed_img.text((width / 9, height / 3 + 150), text=f"Installed memory: {specs.ram} GB", font=font)
        processed_img.text((width / 9, height / 3 + 250), text=f"System type: {specs.processor_type}-bit Operating System", font=font)
        processed_img.text((width / 9, height / 3 + 350), text=f"OS: {specs.operating_sys}", font=font)
        processed_img.text((width / 9, height / 3 + 450), text=f"HDD size: {specs.hdd} GB", font=font)
        processed_img.text((width / 9, height / 3 + 550), text=f"Battery health: {specs.battery_health} %", font=font)
        processed_img.text((width / 9, height / 3 + 650), text=f"Video Controller: {specs.video_controller}", font=font)
        processed_img.text((width / 1.6, height / 3 + 50), text=f"Number of cores: {specs.num_of_cores} Core(s)", font=font)
        processed_img.text((width / 1.6, height / 3 + 150), text=f"Peripherals:", font=font)

        padding = 250
        for port in specs.peripherals:
            processed_img.text((width / 1.37, height / 3 + padding), text=f"{port}", font=font_peripherals)
            padding += 90

        img.save(fr"{specs.current_path}\specs_image.jpg", format="JPEG")

        image_loci = f'"{specs.current_path}\specs_image.jpg"'

        # Change background image
        subprocess.run(f'reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /d {image_loci} /f')
        subprocess.run("RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters")
        subprocess.run("RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters")

add_info()