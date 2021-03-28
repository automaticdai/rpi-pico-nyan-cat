## This example borrows a CircuitPython hsv_to_rgb function to cycle through some rainbows on Pico Display's screen and RGB LED . If you're into rainbows, HSV (Hue, Saturation, Value) is very useful!

import utime
import picodisplay as display

# Set up and initialise Pico Display
width = display.get_width()
height = display.get_height()
pixel_size = 4

buf = bytearray(width * height * 2)
display.init(buf)
display.set_backlight(0.8)

# From CPython Lib/colorsys.py
def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q

h = 0

while True:
    h += 1
    r, g, b = [int(255 * c) for c in hsv_to_rgb(h / 360.0, 1.0, 1.0)]  # rainbow magic
    display.set_led(r, g, b)  # Set LED to a converted HSV value
    pen = display.create_pen(r, g, b)
    display.set_pen(pen)  # Set pen to a converted HSV value
    display.clear()           # Fill the screen with the colour
    display.set_pen(255, 0, 0)  # Set pen to black
    display.rectangle(int(width/2), int(height/2), pixel_size, pixel_size)
    #display.text("Amazing PICO!", 10, 10, 240, 6)  # Add some text
    
    display.update()          # Update the display
    utime.sleep(1.0 / 60)          
