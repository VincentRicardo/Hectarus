import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import math
from adafruit_servokit import ServoKit
import time

kit1 = ServoKit(channels=16, address=0x41)
kit2 = ServoKit(channels=16, address=0x40)

delay = 0.2

def wait(waktu):
    flag = True
    myTime = time.time()
    while flag == True:
        currentTime = time.time()
        if currentTime - myTime < waktu:
            flag = True
        elif currentTime - myTime >= waktu:
            flag = False

class MyNode(Node):
    def __init__(self):
        super().__init__("tetrapod_gait_node")
        self.subscriber_angle = self.create_subscription(Int32MultiArray, "/tetrapod_angle_", self.move, 1)

    def move(self, message = Int32MultiArray):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
