#!/usr/bin/env python

from Tkinter import ALL, Canvas, Frame, SUNKEN, Tk
import colorsys

"""
A Color Wall of configurable size. Each pixel on the color wall expects a
3-element tuple representing the HSV (hue, saturation, value) for that
pixel. Each element is a float between 0 and 1.

For bright colors, vary the hue and set the saturation and value to 1.

For more information on HSV, see:
http://en.wikipedia.org/wiki/HSL_and_HSV

Interface:

set_pixel(): Set the HSV values for the pixel at x-offset x and y-offset y. 0,0
is the upper-left corner.

get_pixel(): Get the HSV values for the pixel at x-offset x and y-offset y.

draw(): Re-draw every pixel on the wall based on the pixel's HSV tuple.

clear(): Set every pixel on the wall to black (HSV (0, 0, 0)). This does not
re-draw the pixels.
"""

class Wall(object):
    MIN_RED = MIN_GREEN = MIN_BLUE = 0x0
    MAX_RED = MAX_GREEN = MAX_BLUE = 0xFF

    PIXEL_WIDTH = 50

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._tk_init()
        self.pixels = [(0, 0, 0) for i in range(self.width * self.height)]

    def _tk_init(self):
        self.root = Tk()
        self.root.title("ColorWall %d x %d" % (self.width, self.height))
        self.root.resizable(0, 0)
        self.frame = Frame(self.root, bd=5, relief=SUNKEN)
        self.frame.pack()

        self.canvas = Canvas(self.frame,
                             width=self.PIXEL_WIDTH * self.width,
                             height=self.PIXEL_WIDTH * self.height,
                             bd=0, highlightthickness=0)
        self.canvas.pack()
        self.root.update()

    def set_pixel(self, x, y, hsv):
        self.pixels[self.width * y + x] = hsv

    def get_pixel(self, x, y):
        return self.pixels[self.width * y + x]

    def draw(self):
        self.canvas.delete(ALL)
        for x in range(len(self.pixels)):
            x_0 = (x % self.width) * self.PIXEL_WIDTH
            y_0 = (x / self.width) * self.PIXEL_WIDTH
            x_1 = x_0 + self.PIXEL_WIDTH
            y_1 = y_0 + self.PIXEL_WIDTH
            hue = "#%02x%02x%02x" % self._get_rgb(self.pixels[x])
            self.canvas.create_rectangle(x_0, y_0, x_1, y_1, fill=hue)
        self.canvas.update()

    def clear(self):
        for i in range(self.width * self.height):
            self.pixels[i] = (0, 0, 0)

    def _hsv_to_rgb(self, hsv):
        rgb = colorsys.hsv_to_rgb(*hsv)
        red = self.MAX_RED * rgb[0]
        green = self.MAX_GREEN * rgb[1]
        blue = self.MAX_BLUE * rgb[2]
        return (red, green, blue)

    def _get_rgb(self, hsv):
        red, green, blue = self._hsv_to_rgb(hsv)
        red = int(float(red) / (self.MAX_RED - self.MIN_RED) * 0xFF)
        green = int(float(green) / (self.MAX_GREEN - self.MIN_GREEN) * 0xFF)
        blue = int(float(blue) / (self.MAX_BLUE - self.MIN_BLUE) * 0xFF)
        return (red, green, blue)
