# Copyright (c) 2022 PAL Robotics S.L. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.frontend.parse_substitution import parse_substitution
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_pal.include_utils import include_scoped_launch_py_description
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node


def generate_launch_description():

    # @TODO: robot pose publisher
    # @TODO: tf lookup
    # @TODO: dynamic footprint

    # Create the launch description and populate
    ld = LaunchDescription()

    launch_args = declare_launch_arguments()

    for arg in launch_args.values():
        ld.add_action(arg)

    declare_actions(ld, launch_args)

    return ld


def declare_launch_arguments() -> Dict:

    arg_dict = {}

    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='false',
        description='Use sim time. ')

    arg_dict[sim_time_arg.name] = sim_time_arg

    robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='tiago_dual',
        description='Name of the robot. ',
        choices=['pmb2', 'tiago', 'pmb3', 'tiago_dual'])

    arg_dict[robot_name.name] = robot_name

    arm_right = DeclareLaunchArgument(
        'arm_type_right',
        default_value='tiago-arm',
        description='Which type of the right arm.',
        choices=['no-arm', 'tiago-arm', 'sea'])

    arg_dict[arm_right.name] = arm_right

    arm_left = DeclareLaunchArgument(
        'arm_type_left',
        default_value='tiago-arm',
        description='Which type of the left arm.',
        choices=['no-arm', 'tiago-arm', 'sea'])

    arg_dict[arm_left.name] = arm_left

    end_effector_right = DeclareLaunchArgument(
        'end_effector_right',
        default_value='pal-gripper',
        description='End effector model of the right arm.',
        choices=['pal-gripper', 'pal-hey5', 'custom', 'no-end-effector'])

    arg_dict[end_effector_right.name] = end_effector_right

    end_effector_left = DeclareLaunchArgument(
        'end_effector_left',
        default_value='pal-gripper',
        description='End effector model of the left arm.',
        choices=['pal-gripper', 'pal-hey5', 'custom', 'no-end-effector'])

    arg_dict[end_effector_left.name] = end_effector_left

    ft_sensor_right = DeclareLaunchArgument(
        'ft_sensor_right',
        default_value='schunk-ft',
        description='FT sensor model. ',
        choices=['schunk-ft', 'no-ft-sensor'])

    arg_dict[ft_sensor_right.name] = ft_sensor_right

    ft_sensor_left = DeclareLaunchArgument(
        'ft_sensor_left',
        default_value='schunk-ft',
        description='FT sensor model. ',
        choices=['schunk-ft', 'no-ft-sensor'])

    arg_dict[ft_sensor_left.name] = ft_sensor_left

    wrist_model_right = DeclareLaunchArgument(
        'wrist_model_right',
        default_value='wrist-2010',
        description='Wrist model. ',
        choices=['wrist-2010', 'wrist-2017'])

    arg_dict[wrist_model_right.name] = wrist_model_right

    wrist_model_left = DeclareLaunchArgument(
        'wrist_model_left',
        default_value='wrist-2010',
        description='Wrist model. ',
        choices=['wrist-2010', 'wrist-2017'])

    arg_dict[wrist_model_left.name] = wrist_model_left

    camera_model = DeclareLaunchArgument(
        'camera_model',
        default_value='orbbec-astra',
        description='Head camera model. ',
        choices=['no-camera', 'orbbec-astra', 'orbbec-astra-pro', 'asus-xtion'])

    arg_dict[camera_model.name] = camera_model

    laser_model = DeclareLaunchArgument(
        'laser_model',
        default_value='sick-571',
        description='Base laser model. ',
        choices=['no-laser', 'sick-571', 'sick-561', 'sick-551', 'hokuyo'])

    arg_dict[laser_model.name] = laser_model

    has_screen = DeclareLaunchArgument(
        'has_screen',
        default_value='false',
        description='Define if the robot has a screen. ',
        choices=['true', 'false'])

    arg_dict[has_screen.name] = has_screen

    base_type = DeclareLaunchArgument(
        'base_type',
        default_value='pmb2',
        description='Define base type of the robot. ',
        choices=['pmb2', 'omni_base'])

    arg_dict[base_type.name] = base_type

    namespace = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Define namespace of the robot. ')

    arg_dict[namespace.name] = namespace

    return arg_dict


def declare_actions(launch_description: LaunchDescription, launch_args: Dict):

    default_controllers = include_scoped_launch_py_description(
        pkg_name='tiago_dual_controller_configuration',
        paths=['launch', 'default_controllers.launch.py'])

    launch_description.add_action(default_controllers)

    play_motion2 = include_scoped_launch_py_description(
        pkg_name='tiago_dual_bringup',
        paths=['launch', 'tiago_dual_play_motion2.launch.py'],
        launch_configurations={"robot_name": LaunchConfiguration("robot_name"),
                               "arm_type_right": LaunchConfiguration("arm_type_right"),
                               "arm_type_left": LaunchConfiguration("arm_type_left"),
                               "end_effector_right": LaunchConfiguration("end_effector_right"),
                               "end_effector_left": LaunchConfiguration("end_effector_left"),
                               "ft_sensor_right": LaunchConfiguration("ft_sensor_right"),
                               "ft_sensor_left": LaunchConfiguration("ft_sensor_left"),
                               "use_sim_time": LaunchConfiguration("use_sim_time")})

    launch_description.add_action(play_motion2)

    twist_mux = include_scoped_launch_py_description(
        pkg_name='tiago_dual_bringup',
        paths=['launch', 'twist_mux.launch.py'],
    )

    launch_description.add_action(twist_mux)

    robot_state_publisher = include_scoped_launch_py_description(
        pkg_name='tiago_dual_description',
        paths=['launch', 'robot_state_publisher.launch.py'],
        launch_configurations={"robot_name": LaunchConfiguration("robot_name"),
                               "arm_type_right": LaunchConfiguration("arm_type_right"),
                               "arm_type_left": LaunchConfiguration("arm_type_left"),
                               "end_effector_right": LaunchConfiguration("end_effector_right"),
                               "end_effector_left": LaunchConfiguration("end_effector_left"),
                               "ft_sensor_right": LaunchConfiguration("ft_sensor_right"),
                               "ft_sensor_left": LaunchConfiguration("ft_sensor_left"),
                               "wrist_model_right": LaunchConfiguration("wrist_model_right"),
                               "wrist_model_left": LaunchConfiguration("wrist_model_left"),
                               "laser_model": LaunchConfiguration("laser_model"),
                               "camera_model": LaunchConfiguration("camera_model"),
                               "base_type": LaunchConfiguration("base_type"),
                               "has_screen": LaunchConfiguration("has_screen"),
                               "namespace": LaunchConfiguration("namespace"),
                               "use_sim_time": LaunchConfiguration("use_sim_time"),
                               })

    launch_description.add_action(robot_state_publisher)

    return
