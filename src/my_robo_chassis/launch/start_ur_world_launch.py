#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
#from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_prefix
from launch.substitutions import Command, LaunchConfiguration, PythonExpression

pkg_name='my_robo_chassis'

def generate_launch_description():

    #pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_models_dir = get_package_share_directory(pkg_name)

    install_dir = get_package_prefix(pkg_name)
    world_file_name = 'test_world1.world'
    world_path = os.path.join(pkg_name, 'worlds', world_file_name)
    if 'GAZEBO_MODEL_PATH' in os.environ:
        gazebo_models_path = os.path.join(pkg_models_dir, 'models')
        os.environ['GAZEBO_MODEL_PATH'] = gazebo_models_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] =  install_dir + "/share"

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'
        
        
        
       

    world = LaunchConfiguration('world')
    
 
 
    declare_world_cmd = DeclareLaunchArgument(
    	name='world',
    	default_value=world_path,
    	description='Full path to the world model file to load')
    
    
    
    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]
        ),
    	launch_arguments={'world': world}.items()
    )    

    
    return LaunchDescription([
        DeclareLaunchArgument(
          'world',
          default_value=[os.path.join(pkg_name, 'worlds', world_file_name), ''], # Change name of world file if required. world_fle_name added by aditya
          description='SDF world file'),
        gazebo,
        declare_world_cmd 
        # ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'], output='screen'),
    ])
