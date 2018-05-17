# -*- coding: utf-8 -*-
"""
    scripts.gazebo_model
    ~~~~~~~~~~~~~~~~~~~

    A class to describe a model in gazebo.

    :copyright: (c) 2018 by Xia Xi.
    :license: MIT License, see LICENSE for more details.
"""

class GazeboModel(object):

    """ A model in gazebo. """

    def __init__(self, name, pose, mesh_name='', bounding_box=()):
        self.__name = name
        self.__pose = pose
        if mesh_name:
            self.__mesh_name = mesh_name
        else:
            self.__mesh_name = name
        self.__bounding_box = bounding_box

    def get_model_name(self):
        """ return model name. """
        return self.__name

    def set_model_name(self, name):
        """ set model name. """
        self.__name = name

    def get_mesh_name(self):
        """ return mesh name. """
        return self.__mesh_name

    def set_mesh_name(self, mesh_name):
        """ set mesh name. """
        self.__mesh_name = mesh_name

    def get_pose(self):
        """ return model pose. """
        return self.__pose

    def set_pose(self, pose):
        """ set model pose. """
        self.__pose = pose

    def get_bounding_box(self):
        """ return model bounding box. """
        return self.__bounding_box[0], self.__bounding_box[1], self.__bounding_box[2]

    def set_bounding_box(self, bounding_box):
        """ set model bounding box. """
        self.__bounding_box = bounding_box
