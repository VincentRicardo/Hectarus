import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import math
from adafruit_servokit import ServoKit

kit1 = ServoKit(channels=16, address=0x40)
kit2 = ServoKit(channels=16, address=0x41)

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
        super().__init__("leg2_node")
        self.subscriber_angle = self.create_subscription(Int32MultiArray, "/angle_", self.move, 1)

    def move(self, message = Int32MultiArray):
        if message.data[9] == 0: #maju
            if message.data[10] == 0: #tripod
                wait(10)
                for i in range(0, 46, 5):
                    kit1.servo[4].angle = 125 + i #femur2
                    kit1.servo[3].angle = 135 + (i) #tibia2
                wait(delay)

                kit1.servo[5].angle = 90 + message.data[0] #coxa2
                wait(delay)

                kit1.servo[3].angle = 135 - message.data[2] #tibia2
                kit1.servo[4].angle = 125 + message.data[1] #femur2
                wait(delay)

                kit1.servo[5].angle = 90 #coxa2
                kit1.servo[4].angle = 125 #femur2
                kit1.servo[3].angle = 135 #tibia2
            if message.data[10] == 1: #wave
                pass
            if message.data[10] == 2: #tetrapod
                pass

        if message.data[9] == 1: #belok kiri/kanan bergantung derajat di gait
            wait(10)
            kit1.servo[4].angle = 180 #femur2
            wait(delay)

            kit1.servo[5].angle = message.data[3] #coxa2
            wait(delay)

            for i in range (0, 50, 5):
                kit1.servo[4].angle = 180 - (i+10) #femur2
                kit1.servo[3].angle = 180 - (i) #tibia2
            wait(delay)

            kit1.servo[5].angle = 90 #coxa2
            kit1.servo[4].angle = 125 #femur2
            kit1.servo[3].angle = 135 #tibia2

        if message.data[9] == 9: #berhenti
            kit1.servo[5].angle = 90 #coxa2
            kit1.servo[4].angle = 125 #femur2
            kit1.servo[3].angle = 135 #tibia2
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
