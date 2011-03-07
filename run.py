#!/usr/bin/env python

import optparse, sys

from wall import Wall
import effects

"""
"""

if __name__ == "__main__":
    parser = optparse.OptionParser("""Usage: %prog [options]""")
    parser.add_option("-w", "--width", type="int",
                      action="store", dest="width",
                      default=8, help="wall width")
    parser.add_option("-t", "--height", type="int",
                      action="store", dest="height",
                      default=8, help="wall height")
    (opts, args) = parser.parse_args(sys.argv[1:])

    wall = Wall(opts.width, opts.height)

    if args:
        effects_to_run = [getattr(effects, a) for a in args \
                              if hasattr(effects, a)]
    else:
        effects_to_run = effects.Effects

    for effect in effects_to_run:
        new_effect = effect(wall)
        print new_effect.__class__.__name__
        new_effect.run()
