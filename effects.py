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
        start_time = time.time()
        while time.time() - start_time < 5:
            for x in range(self.wall.width):
                for y in range(self.wall.height):
                    hsv = (hue, 1, 1)
                    self.wall.set_pixel(x, y, hsv)
                    self.wall.draw()
                    time.sleep(.02)
                    self.wall.clear()
                    hue = (hue + .05) % 1

class Rainbow(Effect):
    def run(self):
        hue = random.random()
        hue_spacing = 1.0/(self.wall.width * self.wall.height)
        delay = .1

        # Draw rainbow stripes from right to left.
        for i in range(self.wall.width - 1, -1, -1):
            for j in range(self.wall.height - 1, -1, -1):
                hsv = (hue, 1, 1)
                self.wall.set_pixel(i, j, hsv)
                hue += hue_spacing
                # on python 2.5, having a hue value of > 1 will return None
                # when you try to convert HSV to RGB using colorsys
                #
                # in later versions, colorsys will treat a hue value of
                # > 1 as *just the truncated fractional part*, e.g.
                # 1.29 becomes 0.29.
                #
                # neither of these particularly make sense, but let's
                # emulate the behaviour of python 2.6+ here for compatibility's
                # sake.
                if hue > 1:
                    hue -= int(hue)
            time.sleep(delay)
            self.wall.draw()

        time.sleep(1)

        # Shift the wall hues for a few seconds.
        start_time = time.time()
        while time.time() - start_time < 5:
            for i in range(self.wall.width):
                for j in range(self.wall.height):
                    hsv = self.wall.get_pixel(i, j)
                    new_hue = (hsv[0] + hue_spacing/4) % 1
                    new_hsv = (new_hue, hsv[1], hsv[2])
                    self.wall.set_pixel(i, j, new_hsv)
            self.wall.draw()

        time.sleep(1)


class Twinkle(Effect):
    def run(self):
        start_time = time.time()
        while time.time() - start_time < 5:
            x = random.randint(0, self.wall.width - 1)
            y = random.randint(0, self.wall.height - 1)
            # Stick to blueish colors.
            hue = .65 + random.uniform(-1, 1) * .1
            value = random.random()
            hsv = (hue, 1, value)
            self.wall.set_pixel(x, y, hsv)
            self.wall.draw()
            time.sleep(.01)

class Matrix(Effect):
    class Column(object):
        def __init__(self, wall):
            self.wall = wall
            self.cache = []
            # Tail must be at least 1 pixel long
            self.tail = max(1, random.randint(
                    self.wall.height / 2, self.wall.height * 2))
            # Get a position somewhere above the wall (so it can trickle down
            # onto the wall)
            self.pos = (random.randint(0, self.wall.width - 1),
                        random.randint(-(self.wall.height * 3), 0))
            self.green = .35

        def step(self):
            """
            Advance the location of the head of the column and all pixels in the
            tail.
            """
            self.cache.append(self.pos)
            self.cache = self.cache[-self.tail:]
            self.pos = [self.pos[0], self.pos[1] + 1]

        def inside_wall(self, x, y, wall):
            if x >= 0 and x < wall.width and y >= 0 and y < wall.height:
                return True
            return False

        def draw(self, wall):
            """
            Set the pixel colors in this column for this step.

            Returns the number of pixels making up this column that were
            actually within the scope of the wall.
            """
            draw_cnt = 0
            # Prepare the tail colors. The further from the head, the dimmer the
            # pixel.
            for index, pos in enumerate(self.cache):
                x = pos[0]
                y = pos[1]
                if self.inside_wall(x, y, wall):
                    hsv = (self.green, 1, float(index)/self.tail)
                    wall.set_pixel(x, y, hsv)
                    draw_cnt += 1

            # Prepare the head color
            x = self.pos[0]
            y = self.pos[1]
            if self.inside_wall(x, y, wall):
                hsv = (self.green, 1, 1)
                wall.set_pixel(x, y, hsv)
                draw_cnt += 1

            return draw_cnt

    def run(self):
        cols = []
        # Initialize 15 - 30 Matrix columns.
        for i in range(random.randint(15, 30)):
            col = self.Column(self.wall)
            cols.append(col)
        # Run the columns down the wall.
        self.draw(cols)

    def draw(self, cols):
        """
        Draw the advancing columns until no parts of any columns are left on the
        wall.
        """
        timeout = 4
        drawing = 0
        while drawing or timeout:
            self.wall.clear()
            for col in cols:
                col.step()
                drawing += col.draw(self.wall)
            self.wall.draw()
            time.sleep(.05)
            if not drawing:
                timeout -= 1
            drawing = 0

Effects = [HueTest, SaturationTest, ValueTest, Columns, Rainbow, Twinkle, Matrix]
