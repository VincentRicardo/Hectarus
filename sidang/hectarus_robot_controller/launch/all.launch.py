from launch import LaunchDescription
import launch_ros.actions



def generate_launch_description():
    return LaunchDescription([
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable= 'process_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'strafe_gait_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'tripod_gait_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'gait_node'),
#        launch_ros.actions.Node(
#            package = 'hectarus_robot_controller', executable = 'wave_gait_node'),
#        launch_ros.actions.Node(
#            package = 'hectarus_robot_controller', executable = 'tetrapod_gait_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'turn_gait_node'),
#        launch_ros.actions.Node(
#            package = 'hectarus_robot_controller', executable = 'tetrapod_gait_tangga_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'count_time_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'stop_gait_node'),
        launch_ros.actions.Node(
            package = 'hectarus_robot_controller', executable = 'gyro_node')
        ])
