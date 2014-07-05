#!/usr/bin/env python

import argparse, sys

from wall import Wall
import effects

"""
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", type=int,
                        action="store", dest="width",
                        default=8, help="wall width")
    parser.add_argument("-t", "--height", type=int,
                        action="store", dest="height",
                        default=8, help="wall height")
    parser.add_argument("-e", "--effects",
                        nargs='+', dest="effects",
                        help="specific effects you wish to run")
    args = parser.parse_args()

    wall = Wall(args.width, args.height)

    if args.effects:
        effects_to_run = [getattr(effects, a) for a in args.effects \
                              if hasattr(effects, a)]

    else:
        effects_to_run = effects.Effects

    for effect in effects_to_run:
        new_effect = effect(wall)
        print new_effect.__class__.__name__
        new_effect.run()
