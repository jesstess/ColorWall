import random
import time
from effects import colors

"""
advanced_effects use a class hierarchy to run on the wall.
"""

class Effect(object):
    def __init__(self, wall):
        self.wall = wall
        self.wall.clear()

    def run(self):
        pass

class KnightMoves(Effect):
    def __init__(self, wall):
        self.wall = wall
        self.wall.clear()
        for x in range(self.wall.width):
            for y in range(self.wall.height):
                if (x + y) % 2 == 0:
                    self.wall.set_pixel(x, y, colors["black"])
                else:
                    self.wall.set_pixel(x, y, colors["white"])
        # Pick a random starting location for the knight
        self.knight_x = random.randint(0, self.wall.width - 1)
        self.knight_y = random.randint(0, self.wall.height - 1)
        self.wall.set_pixel(self.knight_x, self.knight_y, colors["red"])

    def run(self):
        if self.wall.width < 2 or self.wall.height < 2:
            return

        self.wall.draw()
        start_time = time.time()
        while time.time() - start_time < 12:
            self.move()
            self.wall.draw()
            time.sleep(0.75)

    def move(self):
        """
        Move the knight.
        """
        if (self.knight_x + self.knight_y) % 2 == 0:
            self.wall.set_pixel(self.knight_x, self.knight_y, colors["black"])
        else:
            self.wall.set_pixel(self.knight_x, self.knight_y, colors["white"])
        moves = self.getMoves()
        # Select a move at random from the possible moves
        self.knight_x, self.knight_y = moves[random.randint(0, len(moves) - 1)]
        self.wall.set_pixel(self.knight_x, self.knight_y, colors["red"])

    def getMoves(self):
        """
        Get all possible moves that the knight can make.
        """
        moves = []
        # Don't want knight to wrap around the board because you can't
        # do that in chess
        if (self.knight_x - 2) >= 0 and (self.knight_y - 1) >= 0:
            moves.append((self.knight_x - 2, self.knight_y - 1))
        if (self.knight_x - 1) >= 0 and (self.knight_y - 2) >= 0:
            moves.append((self.knight_x - 1, self.knight_y - 2))
        if (self.knight_x - 2) >= 0 and (self.knight_y + 1) < self.wall.height:
            moves.append((self.knight_x - 2, self.knight_y + 1))
        if (self.knight_x + 1) < self.wall.width and (self.knight_y - 2) >= 0:
            moves.append((self.knight_x + 1, self.knight_y - 2))
        if (self.knight_x - 1) >= 0 and (self.knight_y + 2) < self.wall.height:
            moves.append((self.knight_x - 1, self.knight_y + 2))
        if (self.knight_x + 2) < self.wall.width and (self.knight_y - 1) >= 0:
            moves.append((self.knight_x + 2, self.knight_y - 1))
        if (self.knight_x + 2) < self.wall.width and \
          (self.knight_y + 1) < self.wall.height:
            moves.append((self.knight_x + 2, self.knight_y + 1))
        if (self.knight_x + 1) < self.wall.width and \
          (self.knight_y + 2) < self.wall.height:
            moves.append((self.knight_x + 1, self.knight_y + 2))
        return moves

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

class Bouncer(Effect):
    class Ball(object):
        def __init__(self, wall):
            self.wall = wall
            self.x = random.randint(0, self.wall.width - 1)
            self.y = random.randint(0, self.wall.height - 1)
            self.hue = random.random()
            self.dx = self.dy = 0
            while self.dx == 0 and self.dy == 0:
                self.dx = random.choice([-1, 0, 1])
                self.dy = random.choice([-1, 0, 1])
            self.tail = []
            self.tail_len = 4

        def draw(self):
            self.wall.set_pixel(self.x, self.y, (self.hue, 1, 1))
            value = 0.6
            val_step = float(value/(self.tail_len+1))
            for x, y in self.tail:
                value -= val_step
                self.wall.set_pixel(x, y, (self.hue, 1, value))

        def advance(self):
            self.tail = [(self.x, self.y)] + self.tail[:self.tail_len-1]
            self.x += self.dx
            if self.x < 0:
                self.x = 1
                self.dx = -self.dx
            elif self.x >= self.wall.width:
                self.x = self.wall.width - 2
                self.dx = -self.dx

            self.y += self.dy
            if self.y < 0:
                self.y = 1
                self.dy = -self.dy
            elif self.y >= self.wall.height:
                self.y = self.wall.height - 2
                self.dy = -self.dy

    def run(self):
        if self.wall.width < 2 or self.wall.height < 2:
            return

        balls = []
        for i in range(3):
            balls.append(self.Ball(self.wall))

        start_time = time.time()
        while time.time() - start_time < 5:
            self.wall.clear()
            for ball in balls:
                ball.draw()
                ball.advance()
            self.wall.draw()
            time.sleep(.1)

Effects = [Matrix, Bouncer]
