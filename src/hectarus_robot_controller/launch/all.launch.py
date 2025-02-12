from launch import LaunchDescription
import launch_ros.actions



def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable= 'process_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'leg1_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'gait_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'leg2_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'leg3_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'leg4_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'leg5_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'leg6_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'ultrasonik_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'gyro_node')
        ])
