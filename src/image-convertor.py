#!/usr/bin/python3

# This code converts all png files in the same directory into Python bytearray
# The code is improved based on: http://www.penguintutor.com/programming/picodisplayanimations
# automaticdai
# YF Robotics Lab

import png
import os


# convert colors to RGB565
def color_to_bytes (color):
    r, g, b = color
    arr = bytearray(2)
    arr[0] = r & 0xF8
    arr[0] += (g & 0xE0) >> 5
    arr[1] = (g & 0x1C) << 3
    arr[1] += (b & 0xF8) >> 3

    return arr


if __name__ == "__main__":
    pngfiles = []
    folder = "artwork/"

    for file in os.listdir(folder):
        if file.endswith(".png"):
            print(file)
            pngfiles.append(file)

    for filename in pngfiles:
        infile = folder + filename
        outfile = folder + filename.split(".")[0] + ".raw"

        png_reader = png.Reader(infile)
        image_data = png_reader.asRGBA8()

        with open(outfile, "wb") as file:
            print ("PNG file \nwidth {}\nheight {}\n".format(image_data[0], image_data[1]))
            #count = 0

            for row in image_data[2]:
                for r, g, b, a in zip(row[::4], row[1::4], row[2::4], row[3::4]):
                    #print ("This pixel {:02x}{:02x}{:02x} {:02x}".format(r, g, b, a))

                    # convert to (RGB565)
                    img_bytes = color_to_bytes((r,g,b))
                    file.write(img_bytes)
