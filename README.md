# OASC-Benchmark
This benchmark is an accompaniment to our SIGGRAPH'18 paper *Object-Aware Guidance for Autonomous Scene Reconstruction*. You can find more information from our [paper](#) and [project website](#).

## Citation
If you find our work useful in your research, please consider citing:

## Introduction
The Object-Aware Scanning Benchmark (OASC), which aims to facilitate quantitative evaluation of object-aware scene scanning and reconstruction, is a collection of Gazebo virtual scenes, based on existing scene dataset SUNCG[Song et al. 2017]. We select 66 appropriate human-modeled synthetic scenes which are suitable for robot autoscanning and slightly adjust them to avoid collision. The collection contains 5 scene categories, including bedroom, living room, kitchen, bathroom and office.

## Evaluation metrics
You can evaluate the performance of object-aware scanning from several aspects.
### Object recognition
For object recognition task, each object class label can be found in SUNCG/ModelCategoryMapping.csv. We use SUNCG model id as Gazebo model name, so the correspondence between model name and object category is straightforward.
### Single-view object detection
You can use both original rendering RGBD images from SUNCG or simulated color and depth images from Gazebo, however the latter lacks of ground truth and you may have to annotate by yourself.
### Object-level segmentation
### Object coverage rate & coverage quality

## Requirements
Our benchmark and tools are mainly tested in Ubuntu 14.04 and ROS Indigo (with Gazebo 2.2.3), although other environmnet may still work. If you are a novice to ROS, you can get more information from [here](www.ros.org)

## Usage
