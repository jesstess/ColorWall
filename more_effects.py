import ascii8x8
import random
import time
from effects import colors

def HueTest(wall):
    print "HueTest"
    wall.clear()

    hue = 0
    while hue < 1:
        hsv = (hue, 1, 1)
        for x in range(wall.width):
            for y in range(wall.height):
                wall.set_pixel(x, y, hsv)
        wall.draw()
        hue = hue + .01
        time.sleep(.05)

def SaturationTest(wall):
    print "SaturationTest"
    wall.clear()

    hue = random.random()
    saturation = 0
    while saturation < 1:
        hsv = (hue, saturation, 1)
        for x in range(wall.width):
            for y in range(wall.height):
                wall.set_pixel(x, y, hsv)
        wall.draw()
        saturation = saturation + .01
        time.sleep(.05)

def ValueTest(wall):
    print "ValueTest"
    wall.clear()

    hue = random.random()
    value = 0
    while value < 1:
        hsv = (hue, 1, value)
        for x in range(wall.width):
            for y in range(wall.height):
                wall.set_pixel(x, y, hsv)
        wall.draw()
        value = value + .01
        time.sleep(.05)

def Checkerboards(wall):
    print "Checkerboards"
    wall.clear()

    for i in range(10):
        for x in range(wall.width):
            for y in range(wall.height):
                if (x + y + i) % 2 == 0:
                    wall.set_pixel(x, y, colors["black"])
                else:
                    wall.set_pixel(x, y, colors["yellow"])
        wall.draw()
        time.sleep(0.5)

def Columns(wall):
    print "Columns"
    wall.clear()

    hue = random.random()
    start_time = time.time()
    while time.time() - start_time < 5:
        for x in range(wall.width):
            for y in range(wall.height):
                hsv = (hue, 1, 1)
                wall.set_pixel(x, y, hsv)
                wall.draw()
                time.sleep(.02)
                wall.clear()
                hue = (hue + .05) % 1

def Rainbow(wall):
    print "Rainbow"
    wall.clear()

    hue = random.random()
    hue_spacing = 1.0/(wall.width * wall.height)
    delay = .1

    # Draw rainbow stripes from right to left.
    for i in range(wall.width - 1, -1, -1):
        for j in range(wall.height - 1, -1, -1):
            hsv = (hue, 1, 1)
            wall.set_pixel(i, j, hsv)
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
        wall.draw()

    time.sleep(1)

    # Shift the wall hues for a few seconds.
    start_time = time.time()
    while time.time() - start_time < 5:
        for i in range(wall.width):
            for j in range(wall.height):
                hsv = wall.get_pixel(i, j)
                new_hue = (hsv[0] + hue_spacing/4) % 1
                new_hsv = (new_hue, hsv[1], hsv[2])
                wall.set_pixel(i, j, new_hsv)
        wall.draw()

    time.sleep(1)


def Twinkle(wall):
    print "Twinkle"
    wall.clear()

    start_time = time.time()
    while time.time() - start_time < 5:
        x = random.randint(0, wall.width - 1)
        y = random.randint(0, wall.height - 1)
        # Stick to blueish colors.
        hue = .65 + random.uniform(-1, 1) * .1
        value = random.random()
        hsv = (hue, 1, value)
        wall.set_pixel(x, y, hsv)
        wall.draw()
        time.sleep(.01)

def KnightMoves(wall):
    if wall.width < 2 or wall.height < 2:
        return

    print "KnightMoves"
    wall.clear()

    for x in range(wall.width):
        for y in range(wall.height):
            if (x + y) % 2 == 0:
                wall.set_pixel(x, y, colors["black"])
            else:
                wall.set_pixel(x, y, colors["white"])
    # Pick a random starting location for the knight
    knight_x = random.randint(0, wall.width - 1)
    knight_y = random.randint(0, wall.height - 1)
    wall.set_pixel(knight_x, knight_y, colors["red"])
    wall.draw()

    def move(knight_x, knight_y):
        """
        Move the knight.
        """

    def getMoves(knight_x, knight_y):
        """
        Get all possible moves that the knight can make.
        """
        moves = []
        # Don't want knight to wrap around the board because you can't
        # do that in chess
        if (knight_x - 2) >= 0 and (knight_y - 1) >= 0:
            moves.append((knight_x - 2, knight_y - 1))
        if (knight_x - 1) >= 0 and (knight_y - 2) >= 0:
            moves.append((knight_x - 1, knight_y - 2))
        if (knight_x - 2) >= 0 and (knight_y + 1) < wall.height:
            moves.append((knight_x - 2, knight_y + 1))
        if (knight_x + 1) < wall.width and (knight_y - 2) >= 0:
            moves.append((knight_x + 1, knight_y - 2))
        if (knight_x - 1) >= 0 and (knight_y + 2) < wall.height:
            moves.append((knight_x - 1, knight_y + 2))
        if (knight_x + 2) < wall.width and (knight_y - 1) >= 0:
            moves.append((knight_x + 2, knight_y - 1))
        if (knight_x + 2) < wall.width and \
          (knight_y + 1) < wall.height:
            moves.append((knight_x + 2, knight_y + 1))
        if (knight_x + 1) < wall.width and \
          (knight_y + 2) < wall.height:
            moves.append((knight_x + 1, knight_y + 2))
        return moves

    start_time = time.time()
    while time.time() - start_time < 12:
        # Update the knight's position
        if (knight_x + knight_y) % 2 == 0:
            wall.set_pixel(knight_x, knight_y, colors["black"])
        else:
            wall.set_pixel(knight_x, knight_y, colors["white"])
        moves = getMoves(knight_x, knight_y)
        # Select a move at random from the possible moves
        knight_x, knight_y = moves[random.randint(0, len(moves) - 1)]
        wall.set_pixel(knight_x, knight_y, colors["red"])

        wall.draw()
        time.sleep(0.75)

def LetterTest(wall):
    """
    Cycle through the letters of the alphabet.

    Minimum wall size: 8 x 8.
    """
    print "LetterTest"
    wall.clear()

    if wall.width < 8 or wall.height < 8:
        return

    color = random.random()
    foreground = (color, 1, 1)
    # Make the foreground and background complementary colors.
    background = ((color + .5) % 1, 1, 1)

    # Center the letters on the wall
    x_offset = int((wall.width - 8) / 2)
    y_offset = int((wall.height - 8) / 2)

    # Display upper and lower case letters. The break between 90 and 97 is
    # for non-letter keyboard characters.
    for ord in range(65, 91) + range(97, 123):
        wall.clear()

        # Set every pixel to the background color, since ascii8x8 will only
        # color an 8x8 section.
        for x in range(wall.width):
            for y in range(wall.height):
                wall.set_pixel(x, y, background)

        # Color the letter.
        ascii8x8.draw_chr(chr(ord), wall, foreground, background,
                          x_offset, y_offset)
        wall.draw()
        time.sleep(.1)

def Message(wall):
    print "Message"
    wall.clear()

    message = [
        '                                                                      ',
        '     **  * * *** * *  ** *  *    *  **     **  **  ** *   * *         ',
        '     * * * *  *  * * * * ** *    * *      *   * * * * *   * *         ',
        '     **   *   *  *** * * * **    *  *     *   * * * * *   * *         ',
        '     *    *   *  * * * * *  *    *   *    *   * * * * *               ',
        '     *    *   *  * * **  *  *    * **      ** **  **  *** * *         ',
        ]

    if wall.height < 6 or wall.width < 2:
        return

    col = 0
    start_time = time.time()
    while time.time() - start_time < 10:
        wall.clear()
        for x in range(wall.width):
            for y in range(wall.height):
                if y >= len(message):
                    break
                dot = message[y][(x+col) % len(message[0])]
                if dot != ' ':
                    wall.set_pixel(x, y, (.333, 1, 1))
        wall.draw()
        col += 1
        time.sleep(0.07)
