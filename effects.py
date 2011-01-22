import random
import time

class Effect(object):
    def __init__(self, wall):
        self.wall = wall
        self.wall.clear()

    def run(self):
        pass

class HueTest(Effect):
    def run(self):
        hue = random.random()
        start_time = time.time()
        while time.time() - start_time < 5:
            hsv = (hue, 1, 1)
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            hue = (hue + .01) % 1
            time.sleep(.05)

class SaturationTest(Effect):
    def run(self):
        hue = random.random()
        saturation = 0
        start_time = time.time()
        while time.time() - start_time < 5:
            hsv = (hue, saturation, 1)
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            saturation = (saturation + .05) % 1
            time.sleep(.05)

class ValueTest(Effect):
    def run(self):
        hue = random.random()
        value = 0
        start_time = time.time()
        while time.time() - start_time < 5:
            hsv = (hue, 1, value)
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            value = (value + .05) % 1
            time.sleep(.05)

class Columns(Effect):
    def run(self):
        hue = random.random()
        for x in range(self.wall.width):
            for y in range(self.wall.height):
                hsv = (hue, 1, 1)
                self.wall.set_pixel(x, y, hsv)
                self.wall.draw()
                time.sleep(.02)
                self.wall.clear()
                hue = hue + .05

class Twinkle(Effect):
    def run(self):
        start_time = time.time()
        while time.time() - start_time < 10:
            x = random.randint(0, self.wall.width - 1)
            y = random.randint(0, self.wall.height - 1)
            # Stick to blueish colors.
            hue = .65 + random.uniform(-1, 1) * .1
            saturation = random.random()
            value = random.random()
            hsv = (hue, saturation, value)
            self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            time.sleep(.01)

Effects = [HueTest, SaturationTest, ValueTest, Columns, Twinkle]
