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


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_pal.include_utils import include_scoped_launch_py_description
from launch_pal.arg_utils import LaunchArgumentsBase, launch_arg_factory
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentDeclaration(LaunchArgumentsBase):
    use_sim_time: DeclareLaunchArgument = DeclareLaunchArgument(
        name='use_sim_time',
        default_value='False',
        description='Use simulation time')
    namespace: DeclareLaunchArgument = DeclareLaunchArgument(
        name='namespace',
        default_value='',
        description='Define namespace of the robot. ')


def generate_launch_description():

    # @TODO: robot pose publisher
    # @TODO: tf lookup
    # @TODO: dynamic footprint

    # Create the launch description and populate
    ld = LaunchDescription()
    robot_name = "tiago_dual"
    has_robot_config = True
    custom_args = ArgumentDeclaration()
    launch_args = launch_arg_factory(custom_args,
                                     has_robot_config=has_robot_config, robot_name=robot_name)

    launch_args.add_to_launch_description(ld)

    declare_actions(ld, launch_args)

    return ld


def declare_actions(launch_description: LaunchDescription, launch_args: LaunchArgumentsBase):

    default_controllers = include_scoped_launch_py_description(
        pkg_name='tiago_dual_controller_configuration',
        paths=['launch', 'default_controllers.launch.py'],
        launch_arguments={"arm_type_right": launch_args.arm_type_right,
                          "arm_type_left": launch_args.arm_type_left,
                          "end_effector_right": launch_args.end_effector_right,
                          "end_effector_left": launch_args.end_effector_left,
                          "ft_sensor_right": launch_args.ft_sensor_right,
                          "ft_sensor_left": launch_args.ft_sensor_left,
                          })

    launch_description.add_action(default_controllers)

    play_motion2 = include_scoped_launch_py_description(
        pkg_name='tiago_dual_bringup',
        paths=['launch', 'tiago_dual_play_motion2.launch.py'],
        launch_arguments={"arm_type_right": launch_args.arm_type_right,
                          "arm_type_left": launch_args.arm_type_left,
                          "end_effector_right": launch_args.end_effector_right,
                          "end_effector_left": launch_args.end_effector_left,
                          "ft_sensor_right": launch_args.ft_sensor_right,
                          "ft_sensor_left": launch_args.ft_sensor_left,
                          "use_sim_time": launch_args.use_sim_time})

    launch_description.add_action(play_motion2)

    twist_mux = include_scoped_launch_py_description(
        pkg_name='tiago_dual_bringup',
        paths=['launch', 'twist_mux.launch.py'],
    )

    launch_description.add_action(twist_mux)

    robot_state_publisher = include_scoped_launch_py_description(
        pkg_name='tiago_dual_description',
        paths=['launch', 'robot_state_publisher.launch.py'],
        launch_arguments={"arm_type_right": launch_args.arm_type_right,
                          "arm_type_left": launch_args.arm_type_left,
                          "end_effector_right": launch_args.end_effector_right,
                          "end_effector_left": launch_args.end_effector_left,
                          "ft_sensor_right": launch_args.ft_sensor_right,
                          "ft_sensor_left": launch_args.ft_sensor_left,
                          "wrist_model_right": launch_args.wrist_model_right,
                          "wrist_model_left": launch_args.wrist_model_left,
                          "laser_model": launch_args.laser_model,
                          "camera_model": launch_args.camera_model,
                          "base_type": launch_args.base_type,
                          "has_screen": launch_args.has_screen,
                          "namespace": launch_args.namespace,
                          "use_sim_time": launch_args.use_sim_time,
                          })

    launch_description.add_action(robot_state_publisher)

    return
