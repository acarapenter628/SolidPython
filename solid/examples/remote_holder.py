#! /usr/bin/env python3
import sys

from solid import *
from solid.utils import *

SEGMENTS = 48

REMOTE_WIDTH = 43.5
REMOTE_DEPTH = 11
HOLDER_HEIGHT = 65

BOTTOM_WALL_HEIGHT = 32
VOLUME_BUTTON_WIDTH = 13
BOTTOM_DIP_HEIGHT = 13

WALL_WIDTH = 3


# Must be false if this will be exported to FreeCAD
# Either for testing
USE_NUM_SEGMENTS = False


#####
# This is a holder for the remote to a Sony DSX-A415BT car stero
# It works as-is, but it can be opened in FreeCAD and rounded to pretty it up a bit
# Simply print it and glue some velcro or magnets to the back so you can mount it wherever you want
#####


def basic_geometry():

    # Main shell
    shell = cube([REMOTE_WIDTH + 2*WALL_WIDTH, REMOTE_DEPTH + 2*WALL_WIDTH, HOLDER_HEIGHT + WALL_WIDTH], center = True)
    shell = uncenter_vertical(shell)
    
    # Area where the remote goes
    remote = uncenter_vertical(cube([REMOTE_WIDTH, REMOTE_DEPTH, HOLDER_HEIGHT + WALL_WIDTH], center = True))
    remote = up(WALL_WIDTH)(remote)
    
    # Front/side wall removal
    # We need the back wall to give us a larger surface to adhere to, but the front and side walls just need to be big enough to keep the remote from falling out
    wall_remove = uncenter_vertical(cube([REMOTE_WIDTH + 2*WALL_WIDTH, REMOTE_DEPTH + WALL_WIDTH, HOLDER_HEIGHT + WALL_WIDTH - BOTTOM_WALL_HEIGHT], center = True))
    wall_remove = forward(WALL_WIDTH/2)(wall_remove)
    wall_remove = up((BOTTOM_WALL_HEIGHT))(wall_remove)
    
    # Cutout for the volume button
    volume_sqr = uncenter_vertical(cube([VOLUME_BUTTON_WIDTH, WALL_WIDTH, BOTTOM_WALL_HEIGHT - BOTTOM_DIP_HEIGHT], center = True))
    volume_sqr = forward((REMOTE_DEPTH + WALL_WIDTH)/2)(volume_sqr)
    volume_sqr = up(BOTTOM_DIP_HEIGHT)(volume_sqr)
    volume_cutout = volume_sqr

    remote_holder = shell - remote - wall_remove - volume_cutout

    return remote_holder


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = basic_geometry()

    if USE_NUM_SEGMENTS:
        file_out = scad_render_to_file(a, out_dir=out_dir, file_header=f'$fn = {SEGMENTS};')
    else:
        file_out = scad_render_to_file(a, out_dir=out_dir)
    print(f"{__file__}: SCAD file written to: \n{file_out}")