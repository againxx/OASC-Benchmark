#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    scripts.json_2_world
    ~~~~~~~~~~~~~~~~~~~~

    An excutable file to convert SUNCG house.json to gazebo .world file

    :copyright: (c) 2018 by Xia Xi.
    :license: MIT License, see LICENSE for more details.
"""
# pylint: disable=line-too-long

import sys
import os
import json
import csv
import shutil
import numpy as np

from gazebo_model import GazeboModel
from world_writer import WorldWriter
from sdf_writer import write_sdf
from eulerangles import mat2euler

SUNCG_PATH = "/home/ustc-1314/suncg_data/"
WORLD_PATH = "/home/ustc-1314/ProjectData/SunCG/benchmark/"
MLX_PATH = "/home/ustc-1314/ProjectData/SunCG/"
GRAY_TEXTURE_PATH = "/home/ustc-1314/ProjectData/SunCG/"
GAPS_PATH = "/home/ustc-1314/gaps/bin/x86_64/"
SUNCG_METADATA_PATH = SUNCG_PATH + "SUNCGtoolbox-master/metadata/"
MANUAL_DAE_PATH = "/home/ustc-1314/ProjectData/SunCG/manual_dae_object/"
OBJECT_BLACKLIST = ['254', '323', '324', '325', '333',
                    '346', '688', '736', '540', '689',
                    's__1847']
FREE_COLLISION_LIST = ['148', '149', '153', '235',
                       '238', '280', '313', '632',
                       's__487', 's__1647']


class Json2World(object):
    """ Main class convert SUNCG house.json to gazebo .world file. """

    def __init__(self, h_id):
        self.__house_id = h_id
        self.__house_data = {}
        self.__room_objects_data = []
        self.__model_class_data = {}
        self.load_json_data()
        self.load_csv_data()

        if not os.path.exists(WORLD_PATH + self.__house_id):
            os.mkdir(WORLD_PATH + self.__house_id, 0o755)

    def load_json_data(self):
        """ Load house.json file. """
        json_path = SUNCG_PATH + "house/" + self.__house_id + "/house.json"
        with open(json_path) as json_file:
            self.__house_data = json.load(json_file)

    def load_csv_data(self):
        """ Load ModelCategoryMapping.csv in SUNCG metadata. """
        csv_path = SUNCG_METADATA_PATH + "ModelCategoryMapping.csv"
        with open(csv_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.__model_class_data[row["model_id"]] = {
                    "fine_class": row["fine_grained_class"],
                    "coarse_class": row["coarse_grained_class"],
                    "nyu_class": row["nyuv2_40class"]
                }

    def find_room_objects(self, room_id):
        """ Find all objects in the given room. """
        level_id = room_id[0]
        nodes = self.__house_data["levels"][int(level_id)]["nodes"]
        for node in nodes:
            if node["id"] == room_id:
                if node["type"] == "Room":
                    object_ids = node["nodeIndices"]
                    break
                else:
                    print("Wrong room ID!")
        model_names_counter = {}
        for object_id in object_ids:
            if nodes[object_id]["type"] != "Object":
                continue
            model_name = nodes[object_id]["modelId"]
            if model_name in OBJECT_BLACKLIST:
                continue
            if model_names_counter.get(model_name) is not None:
                model_names_counter[model_name] += 1
            else:
                model_names_counter[model_name] = 0
            self.__room_objects_data.append(
                GazeboModel(
                    model_name + '_' + str(model_names_counter[model_name]),
                    compute_pose_by_transform(nodes[object_id]["transform"]),
                    model_name))

        self.translate_objects_2_origin()
        self.translate_objects_2_ground()

    def translate_objects_2_origin(self):
        """ Translate objects to world origin. """
        object_center = np.zeros(2)
        for object_data in self.__room_objects_data:
            object_center += np.array(object_data.get_pose()[:2])
        object_center /= len(self.__room_objects_data)

        for object_data in self.__room_objects_data:
            new_pose = object_data.get_pose()
            new_pose[0] -= object_center[0]
            new_pose[1] -= object_center[1]
            new_pose[0] *= 1.2
            new_pose[1] *= 1.2
            object_data.set_pose(new_pose)

    def translate_objects_2_ground(self):
        """ Translate objects to fit world ground. """
        object_min_z = float("inf")
        for object_data in self.__room_objects_data:
            if object_data.get_pose()[2] < object_min_z:
                object_min_z = object_data.get_pose()[2]

        for object_data in self.__room_objects_data:
            new_pose = object_data.get_pose()
            new_pose[2] -= object_min_z
            object_data.set_pose(new_pose)

    def generate_daes(self, room_id):
        """ Generate .dae files from .obj files. """
        object_dir = WORLD_PATH + self.__house_id + '/' + room_id + '/'
        for object_name in os.listdir(object_dir):
            for file_name in os.listdir(object_dir + object_name):
                if file_name.find(".obj") != -1:
                    command = "meshlabserver -i " \
                            + object_dir + object_name + '/' + file_name \
                            + " -o " + object_dir + object_name + '/' + file_name[:-4] + ".dae" \
                            + " -m wt -s " + MLX_PATH + "rotate_suncg2gazebo.mlx > /dev/null 2>&1"
                    os.system(command)

    def collect_objects(self, room_id):
        """ Copy SUNCG objects & textures to room dir. """
        object_src_path = SUNCG_PATH + "object/"
        object_dst_path = WORLD_PATH + self.__house_id + '/' + room_id + '/'
        for object_data in self.__room_objects_data:
            if not os.path.exists(
                    object_dst_path + object_data.get_mesh_name()):
                shutil.copytree(object_src_path + object_data.get_mesh_name(),
                                object_dst_path + object_data.get_mesh_name())

                mtl_path = object_dst_path + object_data.get_mesh_name() \
                         + '/' + object_data.get_mesh_name() + ".mtl"
                new_mtl_lines = []
                with open(mtl_path) as mtl_file:
                    for line in mtl_file.readlines():
                        if line[:6] == "map_Kd":
                            texture_name = line[line.rfind('/') + 1: -1]
                            texture_relative_path = line[line.find("texture"): -1]
                            shutil.copy(SUNCG_PATH + texture_relative_path,
                                        object_dst_path + object_data.get_mesh_name() + '/')
                            new_mtl_lines.append("map_Kd " + texture_name + '\n')
                        else:
                            if new_mtl_lines and \
                               len(new_mtl_lines[-1]) >= 5 and \
                               new_mtl_lines[-1][:5] == "illum":
                                shutil.copy(GRAY_TEXTURE_PATH + "gray.jpg",
                                            object_dst_path + object_data.get_mesh_name() + '/')
                                new_mtl_lines.append("map_Kd gray.jpg\n")
                            new_mtl_lines.append(line)

                with open(mtl_path, 'w') as mtl_file:
                    mtl_file.writelines(new_mtl_lines)

    def compute_bounding_boxes(self, room_id):
        """ Use gaps to compute bounding box of objects. """
        object_dir = WORLD_PATH + self.__house_id + '/' + room_id + '/'
        for object_data in self.__room_objects_data:
            command = GAPS_PATH + "mshinfo " + object_dir \
                    + object_data.get_mesh_name() + '/' \
                    + object_data.get_mesh_name() + ".obj"
            bounding_box = os.popen(command)
            bounding_box = bounding_box.readlines()[0].split()
            if object_data.get_mesh_name() in FREE_COLLISION_LIST:
                object_data.set_bounding_box((bounding_box[2], bounding_box[0], '0'))
            else:
                object_data.set_bounding_box((bounding_box[2], bounding_box[0], '2'))

    def generate_sdfs(self, room_id):
        """ Generate .sdf files for every object. """
        object_dir = WORLD_PATH + self.__house_id + '/' + room_id + '/'
        for object_data in self.__room_objects_data:
            sdf_path = object_dir + object_data.get_mesh_name() + '/' \
                     + object_data.get_mesh_name() + ".sdf"
            if not os.path.exists(sdf_path):
                write_sdf(object_data, sdf_path)

    def generate_model_config(self, room_id):
        """ Generate model.config files for every object. """
        object_dir = WORLD_PATH + self.__house_id + '/' + room_id + '/'
        for object_data in self.__room_objects_data:
            config_path = object_dir + object_data.get_mesh_name() + '/model.config'
            if not os.path.exists(config_path):
                with open(config_path, 'w') as config_file:
                    config_file.write('<?xml version="1.0"?>\n\n')
                    config_file.write('<model>\n')
                    config_file.write('  <name>' + object_data.get_mesh_name() + '</name>\n')
                    config_file.write('  <version>1.0</version>\n')
                    config_file.write('  <sdf version="1.4">' + object_data.get_mesh_name() + '.sdf</sdf>\n\n')
                    config_file.write('  <author>\n')
                    config_file.write('    <name>Xi Xia</name>\n')
                    config_file.write('    <email>againxx@mail.ustc.edu.cn</email>\n')
                    config_file.write('  </author>\n\n')
                    config_file.write('  <description>\n')
                    config_file.write('    A model from SUNCG dataset.\n')
                    config_file.write('  </description>\n')
                    config_file.write('</model>\n')

    def generate_world(self, room_id):
        """ Generate .world file for the room. """
        object_dir = WORLD_PATH + self.__house_id + '/' + room_id + '/'
        world_writer = WorldWriter(object_dir + 'room.world')
        world_writer.write_header()
        for object_data in self.__room_objects_data:
            dae_size = os.path.getsize(object_dir + object_data.get_mesh_name() + '/'
                                       + object_data.get_mesh_name() + ".dae")
            if dae_size == 0 and os.path.exists(
                    MANUAL_DAE_PATH + object_data.get_mesh_name() + ".dae"):
                os.remove(object_dir + object_data.get_mesh_name() + '/'
                          + object_data.get_mesh_name() + ".dae")
                shutil.copy(MANUAL_DAE_PATH + object_data.get_mesh_name() + ".dae",
                            object_dir + object_data.get_mesh_name() + '/')
            world_writer.add_object(object_data)
        world_writer.write_footer()

    def build_room(self, room_id):
        """ Generate a .world file for a given room. """
        if os.path.exists(WORLD_PATH + self.__house_id + '/' + room_id):
            return
        else:
            os.mkdir(WORLD_PATH + self.__house_id + '/' + room_id)
        self.find_room_objects(room_id)
        self.collect_objects(room_id)
        self.generate_daes(room_id)
        self.compute_bounding_boxes(room_id)
        self.generate_sdfs(room_id)
        self.generate_model_config(room_id)
        self.generate_world(room_id)


def compute_pose_by_transform(transform):
    """ Compute object pose by transformation matrix. """
    transform = np.matrix(transform).reshape(4, 4, order='F')
    scale_matrix = np.matrix(np.identity(4))
    for i in range(3):
        scale_matrix[i, i] = np.linalg.norm(transform[:, i])
    transform *= scale_matrix.I

    coordinate_transform = np.matrix(
        [[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=np.float)
    transform[0:3, 0:3] = coordinate_transform * transform[
        0:3, 0:3] * coordinate_transform.T
    transform[0:3, 3] = coordinate_transform * transform[0:3, 3]
    z_angle, y_angle, x_angle = mat2euler(transform[0:3, 0:3])
    pose = [
        transform[0, 3], transform[1, 3], transform[2, 3],
        x_angle, y_angle, z_angle
    ]
    return pose


def main():
    """ Main entry function """
    if len(sys.argv) < 2:
        print("Don't provide house ID!")
        return

    json_2_world = Json2World(sys.argv[1])

    if len(sys.argv) < 3:
        print("Don't provide room ID!")
        return

    json_2_world.build_room(sys.argv[2])


if __name__ == "__main__":
    main()
