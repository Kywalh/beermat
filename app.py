#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from flask import Flask, render_template, request
import board
import busio
import os
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import neopixel


def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

# Configuration of I2C
i2c = busio.I2C(board.SCL, board.SDA)
i2c = board.I2C()
# Configuration of SSD1306 OLED display
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 1
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Configuration of NeoPixels
pixel_pin = board.D18
num_pixels = 4
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.01, auto_write=True, pixel_order=ORDER)
    


text_size = 24


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data():
    username = request.form['fname']
    usercolor = request.form['favcolor']
    userbeertype = "IPA3" #request.form['fbeertype']
    print(username + " " + usercolor + " " + userbeertype)
    image = Image.new("1", (oled.width, oled.height))
     
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
         
    # Load default font.
    font1 = ImageFont.truetype('arial_narrow_7.ttf',text_size)
     
    # Draw Some Text
    text = username
    (font1_width, font1_height) = font1.getsize(text)
    draw.text(
        (oled.width // 2 - font1_width // 2, oled.height // 2 - font1_height // 2),
        text,
        font=font1,
        fill=255,
    )
    # Display image
    oled.image(image)
    oled.show()

    
    color = hex_to_rgb(usercolor)
    
    pixels.fill(color)
    pixels.show()
    print(color)
    
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')