#!/usr/bin/env python

import optparse, sys

from wall import Wall
import effects, advanced_effects

"""
"""

if __name__ == "__main__":
    parser = optparse.OptionParser("""Usage: %prog [options]""")
    parser.add_option("-w", "--width", type="int",
                      action="store", dest="width",
                      default=8, help="Sets the wall width.")
    parser.add_option("-t", "--height", type="int",
                      action="store", dest="height",
                      default=8, help="Sets the wall height.")
    parser.add_option("-a", "--advanced", action="store_true",
                      dest="advanced",
                      help="Runs the advanced effects.")
    parser.add_option("-s", "--skip-normal", action="store_true",
                      dest="skip_normal",
                      help="Skips running normal effects.")
    (opts, args) = parser.parse_args(sys.argv[1:])

    wall = Wall(opts.width, opts.height)

    if opts.skip_normal:
        print "***Skipping normal effects***"
    else:
        print "***Normal effects follow***"
        effects.SolidColorTest(wall)
        effects.HueTest(wall)
        effects.SaturationTest(wall)
        effects.ValueTest(wall)
        effects.DictionaryTest(wall)
        effects.RainbowTest(wall)
        effects.Checkerboards(wall)
        effects.Columns(wall)
        effects.Rainbow(wall)
        effects.Twinkle(wall)
        effects.KnightMoves(wall)
        effects.LetterTest(wall)
        effects.Message(wall)

    if opts.advanced:
        print "***Advanced effects follow***"
        effects_to_run = advanced_effects.Effects
        for effect in effects_to_run:
            new_effect = effect(wall)
            print new_effect.__class__.__name__
            new_effect.run()
    else:
        print "***Skipping advanced effects***"
