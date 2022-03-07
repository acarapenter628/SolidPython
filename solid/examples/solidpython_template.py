#! /usr/bin/env python3
import sys

from solid import *
from solid.utils import *

SEGMENTS = 256

# Should be False if this uses circles or arcs and will be exported to FreeCAD
# True or False can be used for testing
# Should be True if it will be exported as an STL directly from OpenSCAD
# This changes the number of segments used to create circles in the OpenSCAD renderer
USE_NUM_SEGMENTS = True


################
# Rotations:
################
# Rotate around the axis, not around the center of that object: 
#     Make sure to rotate before moving

# def rot_z_to_down(obj:OpenSCADObject)
# def rot_z_to_right(obj:OpenSCADObject)
# def rot_z_to_left(obj:OpenSCADObject)
# def rot_z_to_forward(obj:OpenSCADObject)
# def rot_z_to_back(obj:OpenSCADObject)

# and

# def rot_z_to_x(obj:OpenSCADObject)
# def rot_z_to_neg_x(obj:OpenSCADObject)
# def rot_z_to_neg_y(obj:OpenSCADObject)
# def rot_z_to_y(obj:OpenSCADObject)
# def rot_x_to_y(obj:OpenSCADObject)
# def rot_x_to_neg_y(obj:OpenSCADObject)


###############
# Translations:
###############
# up(z:float)
# down(z: float)
# right(x: float)
# left(x: float)
# forward(y: float)
# back(y: float)

# uncenter_vertical(base_object: OpenSCADObject)


###################
# Object Parameters:
###################
# height
# width
# depth
# x_pos
# y_pos
# z_pos
# d, d1, d2
# r, r1, r2


def basic_geometry():
    volume_sqr = cube([13, 3, 19], center = True)  # Create a cube
    volume_sqr = uncenter_vertical(volume_sqr)  # Align the bottom with the XY Plane
    print(volume_sqr)  # Print info about it
    
    volume_cyl = cylinder(d = 13, h = 10, center = True) # Create a cylinder
    volume_cyl = rot_z_to_back(volume_cyl) # Rotate
    volume_cyl = up(volume_sqr.height)(volume_cyl) # Shift up
    print(volume_cyl)  # Print info about it

    return volume_sqr + volume_cyl # Add them together


if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = basic_geometry()

    if USE_NUM_SEGMENTS:
        file_out = scad_render_to_file(a, out_dir=out_dir, file_header=f'$fn = {SEGMENTS};')
    else:
        file_out = scad_render_to_file(a, out_dir=out_dir)
    print(f"{__file__}: SCAD file written to: \n{file_out}")