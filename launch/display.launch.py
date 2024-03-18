import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='urdf_test').find('urdf_test')
    urdfModelPat = os.path.join(pkg_share, 'urdf/robot_xacro.xacro')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/rviz.rviz')

    with open(urdfModelPat, 'r') as infp:
        robot_desc = infp.read()
    params = {'robot_description': robot_desc}

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params])

    gazebo_launch_cmd = launch.actions.ExecuteProcess(
        cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[params]
    )

    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'Robot1', '-topic', 'robot_description'],
        output='screen'
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=[default_rviz_config_path],
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=urdfModelPat,
                                             description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                             description='Absolute path to rviz config file'),
        joint_state_publisher_node,
        robot_state_publisher_node,
        gazebo_launch_cmd,
        spawn_entity,
        rviz_node
    ])
