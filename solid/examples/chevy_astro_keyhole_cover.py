#! /usr/bin/env python3
import sys

from solid import *
from solid.utils import *

SEGMENTS = 48

# Must be false if this will be exported to FreeCAD
# Either for testing
USE_NUM_SEGMENTS = False

# Defines for common parameters
WALL_THICKNESS = 3
MAGNET_RADIUS = 4.5
MAGNET_HEIGHT = 3

#####
# This is a cover for the keyhole/button on the second generation Chevy Astro with Dutch doors.  
# If the rear hatch is open in the rain, water gets in and shorts out the signal wires, causing it to lock/unlock repeatedly and drain the battery
# I haven't printed and tested this iteration of the cover - it was originally made in FreeCAD and then recreated here
#####

def basic_geometry():
    # First create a rough model of the keyhole/button that this object will be covering
    inner_upper_cyl = cylinder(d=24, h = 28)
    inner_lower_cyl = cylinder(d1 = 46, d2 = 34, h = 15)

    # Now that we have that, we can create the outer volume relative to it
    outer_upper_cyl = cylinder(r = inner_upper_cyl.r + WALL_THICKNESS, h = inner_upper_cyl.height + WALL_THICKNESS)
    outer_lower_cyl = cylinder(r1 = inner_lower_cyl.r1 + WALL_THICKNESS, r2 = inner_lower_cyl.r2 + WALL_THICKNESS, h = inner_lower_cyl.height + WALL_THICKNESS)
    
    # Add the segments on the side the magnets will go into
    magnet_holder_left = left(31.5)(cylinder(r = MAGNET_RADIUS + WALL_THICKNESS, h = MAGNET_HEIGHT + WALL_THICKNESS))
    magnet_holder_right = right(31.5)(cylinder(r = MAGNET_RADIUS + WALL_THICKNESS, h = MAGNET_HEIGHT + WALL_THICKNESS))
    print(magnet_holder_right)

    # Add connective tissue to attach the magnet holders to the main body
    # Easiest to just make this one big cube that covers both
    magnet_holder_connection = uncenter_vertical(cube([magnet_holder_right.x_pos * 2, magnet_holder_right.d, magnet_holder_right.height], center = True))
    print(magnet_holder_connection)
    
    # Now add the holes for the magnets
    # Creating these first and using the parameters for the magnet holders would have better demonstrated the improvements in this fork, but this felt easier
    magnet_left = left(31.5)(cylinder(r = MAGNET_RADIUS, h = MAGNET_HEIGHT))
    magnet_right = right(31.5)(cylinder(r = MAGNET_RADIUS, h = MAGNET_HEIGHT))
    
    outer_volume = outer_upper_cyl + outer_lower_cyl + magnet_holder_left + magnet_holder_right + magnet_holder_connection
    negative_space = inner_upper_cyl + inner_lower_cyl + magnet_left + magnet_right
    combined = outer_volume - negative_space

    return combined


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = basic_geometry()

    if USE_NUM_SEGMENTS:
        file_out = scad_render_to_file(a, out_dir=out_dir, file_header=f'$fn = {SEGMENTS};')
    else:
        file_out = scad_render_to_file(a, out_dir=out_dir)
    print(f"{__file__}: SCAD file written to: \n{file_out}")