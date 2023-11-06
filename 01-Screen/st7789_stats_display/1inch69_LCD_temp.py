#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import psutil
import sys
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch69
from PIL import Image, ImageDraw, ImageFont
from gpiozero import CPUTemperature
import subprocess

cpu = CPUTemperature()

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0
logging.basicConfig(level = logging.DEBUG)

# Create blank image for drawing.

isDrawPrepared = True
isTempPrepared = True
isWlanPrepared = True

LCD = LCD_1inch69.LCD_1inch69()
# Initialize library.
LCD.Init()
# Clear display.
#LCD.clear()
# Font
Font1 = ImageFont.truetype("/home/pi/Desktop/LCD_Module_code/RaspberryPi/python/Font/Font01.ttf", 25)
Font2 = ImageFont.truetype("/home/pi/Desktop/LCD_Module_code/RaspberryPi/python/Font/Font01.ttf", 35)
Font3 = ImageFont.truetype("/home/pi/Desktop/LCD_Module_code/RaspberryPi/python/Font/Font02.ttf", 32)

image1 = Image.new("RGB", (LCD.width,LCD.height ), "BLACK")
draw = ImageDraw.Draw(image1)


time.sleep(2)
wifi_cmd = subprocess.check_output(['iwconfig'])
wifi_data = wifi_cmd.decode('utf-8')
wifi_ssid = wifi_data.split("ESSID:\"",1)[1].split("\"",1)[0]

def drawTemp(draw):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory()
        disk_usage = psutil.disk_usage('/')
        cpu_temp = cpu.temperature
        TEMP_COLOR = "GREEN"
        if(cpu_temp < 40 ):
                TEMP_COLOR = "GREEN"
        elif(cpu_temp > 55):
                TEMP_COLOR = "RED"
        else:
                TEMP_COLOR = "YELLOW"

        MEM_COLOR = "GREEN"
        if(memory_usage.percent < 50):
                MEM_COLOR = "GREEN"
        elif(memory_usage.percent > 75):
                MEM_COLOR = "RED"
        else:
                MEM_COLOR = "YELLOW"

        DISK_COLOR = "GREEN"
        if(disk_usage.percent < 50):
                DISK_COLOR = "GREEN"
        elif(disk_usage.percent > 75):
                DISK_COLOR = "RED"
        else:
                DISK_COLOR = "YELLOW"

        CPU_COLOR = "GREEN"
        if(cpu_usage < 50):
                CPU_COLOR = "GREEN"
        elif(cpu_usage > 75):
                CPU_COLOR = "RED"
        else:
                CPU_COLOR = "YELLOW"

        draw.text((20, 15),u"cpu", fill = "WHITE", font=Font3)
        draw.text((20, 55), f"{cpu_usage}%", fill = CPU_COLOR, font=Font3)
        draw.text((130, 15),u"temp", fill = "WHITE", font=Font3)
        draw.text((130, 55), str(cpu.temperature)[:4]+str('°C'), fill = TEMP_COLOR, font=Font3)
        draw.text((20, 100),u"mem", fill = "WHITE", font=Font3)
        draw.text((20, 140), f"{memory_usage.percent}%", fill = MEM_COLOR, font=Font3)
        draw.text((130, 100),u"disk", fill = "WHITE", font=Font3)
        draw.text((130, 140), f"{disk_usage.percent}%", fill = DISK_COLOR, font=Font3)


def drawSSID(draw):
    #wifi_cmd = subprocess.check_output(['iwconfig'])
    #wifi_data = wifi_cmd.decode('utf-8')
    #wifi_ssid = wifi_data.split("ESSID:\"",1)[1].split("\"",1)[0]
    draw.text((20, 190),u"ssid", fill = "WHITE", font=Font3)
    draw.text((20, 230), wifi_ssid, fill = "PURPLE", font=Font3)


while(isTempPrepared):

    time.sleep(2)

    image1 = Image.new("RGB", (LCD.width,LCD.height ), "BLACK")
    draw = ImageDraw.Draw(image1)

    drawTemp(draw)
    drawSSID(draw)

    image1=image1.rotate(0)
    LCD.ShowImage(image1)
