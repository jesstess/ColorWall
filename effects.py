import time

# A dictionary of hsv values for some common colors.
colors = {"black":(0, 0, 0), "white":(0, 0, 1), "gray":(0, 0, 0.5),
          "red":(0, 1, 1), "blue":(0.66, 1, 1), "yellow":(0.16, 1, 1),
          "purple":(0.85, 1, 0.5), "green":(0.33, 1, 0.5),
          "orange":(0.083, 1, 1), "pink":(0.9, 1, 1), "lime":(0.33, 1, 1),
          "baby blue":(0.66, 0.5, 1), "cyan":(0.5, 1, 1),
          "brown":(0.07, 0.86, 0.54), "beige":(0.083, 0.32, 1),
          "indigo":(0.75, 1, 0.5), "dark gray":(0, 0, 0.15),
          "light gray":(0, 0, 0.75), "maroon":(0, 1, 0.5),
          "navy":(0.66, 1, 0.25)}

def SolidColorTest(wall):
    print "SolidColorTest"

    color = colors["blue"]
    for x in range(wall.width):
        for y in range(wall.height):
            wall.set_pixel(x, y, color)

    wall.draw()
    time.sleep(2)

def DictionaryTest(wall):
    print "DictionaryTest"

    for color in colors.keys():
        for x in range(wall.width):
            for y in range(wall.height):
                wall.set_pixel(x, y, colors[color])
        wall.draw()
        time.sleep(0.5)

def RainbowTest(wall):
    print "RainbowTest"
