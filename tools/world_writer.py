# -*- coding: utf-8 -*-
"""
    scripts.world_writer
    ~~~~~~~~~~~~~~~~~~~

    A class to write gazebo .world file

    :copyright: (c) 2018 by Xia Xi.
    :license: MIT License, see LICENSE for more details.
"""

# pylint: disable=line-too-long

from gazebo_model import GazeboModel


class WorldWriter(object):

    """ Write gazebo .world file. """

    def __init__(self, path):
        self.__file_path = path
        self.__file = None

    def __open_file(self):
        """ Open world file with append mode. """
        if self.__file is None:
            self.__file = open(self.__file_path, 'a')

    def __close_file(self):
        """ Close world file. """
        if self.__file is not None:
            self.__file.close()
            self.__file = None

    def write_header(self):
        """ Write necessary header info into world file. """
        self.__open_file()
        self.__file.write("<sdf version='1.4'>\n")
        self.__file.write("  <world name='default'>\n")

        self.__write_sun_light()
        self.__write_ground_plane()
        self.__write_physics()
        self.__write_scene()
        self.__write_spherical_coordinates()

        self.__close_file()

    def write_footer(self):
        """ Write necessary footer info into .world file. """
        self.__open_file()
        self.__file.write("    <gui fullscreen='0'>\n")
        self.__file.write("      <camera name='user_camera'>\n")
        self.__file.write("        <pose>0 0 10 0 0 0</pose>\n")
        self.__file.write("        <view_controller>orbit</view_controller>\n")
        self.__file.write("      </camera>\n")
        self.__file.write("    </gui>\n")
        self.__file.write("  </world>\n")
        self.__file.write("/sdf>\n")
        self.__close_file()

    def add_object(self, new_object):
        """ Write a new object info to world file. """
        if isinstance(new_object, GazeboModel):
            bb_x, bb_y, bb_z = new_object.get_bounding_box()
            pose = new_object.get_pose()
            pose = [str(round(x, 6)) for x in pose]

            self.__open_file()
            self.__file.write("    <model name='" + new_object.get_model_name() + "'>\n")
            self.__file.write("      <pose>"
                              + pose[0] + ' ' + pose[1] + ' ' + pose[2] + ' '
                              + pose[3] + ' ' + pose[4] + ' ' + pose[5] + "</pose>\n")
            self.__file.write("      <static>1</static>\n")
            self.__file.write("      <link name='link'>\n")
            self.__file.write("        <collision name='collision'>\n")
            self.__file.write("          <pose>0 0 0 0 -0 0</pose>\n")
            self.__file.write("          <geometry>\n")
            self.__file.write("            <box>\n")
            self.__file.write("              <size>" + bb_x + ' ' + bb_y + ' ' + bb_z + "</size>\n")
            self.__file.write("            </box>\n")
            self.__file.write("          </geometry>\n")
            self.__file.write("          <max_contacts>10</max_contacts>\n")
            self.__file.write("          <surface>\n")
            self.__file.write("            <bounce/>\n")
            self.__file.write("            <friction>\n")
            self.__file.write("              <ode/>\n")
            self.__file.write("            </friction>\n")
            self.__file.write("            <contact>\n")
            self.__file.write("              <ode/>\n")
            self.__file.write("            </contact>\n")
            self.__file.write("          </surface>\n")
            self.__file.write("        </collision>\n")
            self.__file.write("        <visual name='visual'>\n")
            self.__file.write("          <pose>0 0 0 0 -0 0</pose>\n")
            self.__file.write("          <geometry>\n")
            self.__file.write("            <mesh>\n")
            self.__file.write("              <uri>model://" + new_object.get_mesh_name() + "/" + new_object.get_mesh_name() + ".dae</uri>\n")
            self.__file.write("            </mesh>\n")
            self.__file.write("          </geometry>\n")
            self.__file.write("        </visual>\n")
            self.__file.write("        <velocity_decay>\n")
            self.__file.write("          <linear>0</linear>\n")
            self.__file.write("          <angular>0</angular>\n")
            self.__file.write("        </velocity_decay>\n")
            self.__file.write("        <self_collide>0</self_collide>\n")
            self.__file.write("        <kinematic>0</kinematic>\n")
            self.__file.write("        <gravity>1</gravity>\n")
            self.__file.write("      </link>\n")
            self.__file.write("    </model>\n")
            self.__close_file()

    def __write_sun_light(self):
        """ Add sun light info into .world file. """
        self.__file.write("    <light name='sun' type='directional'>\n")
        self.__file.write("      <cast_shadows>1</cast_shadows>\n")
        self.__file.write("      <pose>0 0 10 0 -0 0</pose>\n")
        self.__file.write("      <diffuse>0.8 0.8 0.8 1</diffuse>\n")
        self.__file.write("      <specular>0.2 0.2 0.2 1</specular>\n")
        self.__file.write("      <attenuation>\n")
        self.__file.write("        <range>1000</range>\n")
        self.__file.write("        <constant>0.9</constant>\n")
        self.__file.write("        <linear>0.01</linear>\n")
        self.__file.write("        <quadratic>0.001</quadratic>\n")
        self.__file.write("      </attenuation>\n")
        self.__file.write("      <direction>-0.5 0.1 -0.9</direction>\n")
        self.__file.write("    </light>\n")

    def __write_ground_plane(self):
        """ Add ground plane info into .world file. """
        self.__file.write("    <model name='ground_plane'>\n")
        self.__file.write("      <static>1</static>\n")
        self.__file.write("      <link name='link'>\n")
        self.__file.write("        <collision name='collision'>\n")
        self.__file.write("          <geometry>\n")
        self.__file.write("            <plane>\n")
        self.__file.write("              <normal>0 0 1</normal>\n")
        self.__file.write("              <size>100 100</size>\n")
        self.__file.write("            </plane>\n")
        self.__file.write("          </geometry>\n")
        self.__file.write("          <surface>\n")
        self.__file.write("            <friction>\n")
        self.__file.write("              <ode>\n")
        self.__file.write("                <mu>100</mu>\n")
        self.__file.write("                <mu2>50</mu2>\n")
        self.__file.write("              </ode>\n")
        self.__file.write("            </friction>\n")
        self.__file.write("            <bounce/>\n")
        self.__file.write("            <contact>\n")
        self.__file.write("              <ode/>\n")
        self.__file.write("            </contact>\n")
        self.__file.write("          </surface>\n")
        self.__file.write("          <max_contacts>10</max_contacts>\n")
        self.__file.write("        </collision>\n")
        self.__file.write("        <visual name='visual'>\n")
        self.__file.write("          <cast_shadows>0</cast_shadows>\n")
        self.__file.write("          <geometry>\n")
        self.__file.write("            <plane>\n")
        self.__file.write("              <normal>0 0 1</normal>\n")
        self.__file.write("              <size>100 100</size>\n")
        self.__file.write("            </plane>\n")
        self.__file.write("          </geometry>\n")
        self.__file.write("          <material>\n")
        self.__file.write("            <script>\n")
        self.__file.write("              <uri>file://media/materials/scripts/gazebo.material</uri>\n")
        self.__file.write("              <name>Gazebo/Grey</name>\n")
        self.__file.write("            </script>\n")
        self.__file.write("          </material>\n")
        self.__file.write("        </visual>\n")
        self.__file.write("        <velocity_decay>\n")
        self.__file.write("          <linear>0</linear>\n")
        self.__file.write("          <angular>0</angular>\n")
        self.__file.write("        </velocity_decay>\n")
        self.__file.write("        <self_collide>0</self_collide>\n")
        self.__file.write("        <kinematic>0</kinematic>\n")
        self.__file.write("        <gravity>1</gravity>\n")
        self.__file.write("      </link>\n")
        self.__file.write("    </model>\n")

    def __write_physics(self):
        """ Write physics info into .world file. """
        self.__file.write("    <physics type='ode'>\n")
        self.__file.write("      <max_step_size>0.001</max_step_size>\n")
        self.__file.write("      <real_time_factor>1</real_time_factor>\n")
        self.__file.write("      <real_time_update_rate>1000</real_time_update_rate>\n")
        self.__file.write("      <gravity>0 0 -9.8</gravity>\n")
        self.__file.write("    </physics>\n")

    def __write_scene(self):
        """ Write scene info into .world file. """
        self.__file.write("    <scene>\n")
        self.__file.write("      <ambient>0.4 0.4 0.4 1</ambient>\n")
        self.__file.write("      <background>0.7 0.7 0.7 1</background>\n")
        self.__file.write("      <shadows>1</shadows>\n")
        self.__file.write("    </scene>\n")

    def __write_spherical_coordinates(self):
        """ Write spherical coordinates info into .world file. """
        self.__file.write("    <spherical_coordinates>\n")
        self.__file.write("      <surface_model>EARTH_WGS84</surface_model>\n")
        self.__file.write("      <latitude_deg>0</latitude_deg>\n")
        self.__file.write("      <longitude_deg>0</longitude_deg>\n")
        self.__file.write("      <elevation>0</elevation>\n")
        self.__file.write("      <heading_deg>0</heading_deg>\n")
        self.__file.write("    </spherical_coordinates>\n")
