# -*- coding: utf-8 -*-
"""
    scripts.sdf_writer
    ~~~~~~~~~~~~~~~~~~~

    A class to write gazebo .sdf file

    :copyright: (c) 2018 by Xia Xi.
    :license: MIT License, see LICENSE for more details.
"""

# pylint: disable=line-too-long

from gazebo_model import GazeboModel


def write_sdf(model, path):
    """ Write model info into a .sdf file. """
    if isinstance(model, GazeboModel):
        with open(path, 'w') as sdf_file:
            bb_x, bb_y, bb_z = model.get_bounding_box()
            sdf_file.write("<?xml version='1.0'?>\n")
            sdf_file.write("<sdf version='1.4'>\n")
            sdf_file.write("  <model name='" + model.get_mesh_name() + "'>\n")
            sdf_file.write("    <pose>0 0 0 0 0 0</pose>\n")
            sdf_file.write("    <static>true</static>\n")
            sdf_file.write("    <link name='link'>\n")
            sdf_file.write("      <collision name='collision'>\n")
            sdf_file.write("        <pose>0 0 0 0 0 0</pose>\n")
            sdf_file.write("        <geometry>\n")
            sdf_file.write("          <box>\n")
            sdf_file.write("            <size>" + bb_x + ' ' + bb_y + ' ' + bb_z + "</size>\n")
            sdf_file.write("          </box>\n")
            sdf_file.write("        </geometry>\n")
            sdf_file.write("      </collision>\n")
            sdf_file.write("      <visual name='visual'>\n")
            sdf_file.write("        <pose>0 0 0 0 0 0</pose>\n")
            sdf_file.write("        <geometry>\n")
            sdf_file.write("          <mesh><uri>model://" + model.get_mesh_name() + '/' + model.get_mesh_name() + ".dae</uri></mesh>\n")
            sdf_file.write("        </geometry>\n")
            sdf_file.write("      </visual>\n")
            sdf_file.write("    </link>\n")
            sdf_file.write("  </model>\n")
            sdf_file.write("</sdf>\n")
