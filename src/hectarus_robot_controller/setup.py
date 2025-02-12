import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'hectarus_robot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hectarus',
    maintainer_email='hectarus@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "process_node = hectarus_robot_controller.process_node:main",
            "gyro_node = hectarus_robot_controller.gyro_node:main",
            "ultrasonik_node = hectarus_robot_controller.ultrasonik_node:main",
            "gait_node = hectarus_robot_controller.gait_node:main",
            "leg1_node = hectarus_robot_controller.leg1_node:main",
            "leg2_node = hectarus_robot_controller.leg2_node:main",
            "leg3_node = hectarus_robot_controller.leg3_node:main",
            "leg4_node = hectarus_robot_controller.leg4_node:main",
            "leg5_node = hectarus_robot_controller.leg5_node:main",
            "leg6_node = hectarus_robot_controller.leg6_node:main"
        ],
    },
)
