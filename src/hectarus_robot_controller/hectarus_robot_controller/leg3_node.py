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
        super().__init__("leg3_node")
        self.subscriber_angle = self.create_subscription(Int32MultiArray, "/angle_", self.move, 1)

    def move(self, message = Int32MultiArray):
        if message.data[9] == 0: #maju
            if message.data[10] == 0: #tripod
                for i in range(0, 46, 5):
                    kit1.servo[1].angle = 125 + i #femur3
                    kit1.servo[0].angle = 135 + (i) #tibia3
                wait(delay)

                kit1.servo[2].angle = 90 + message.data[6] #coxa3
                wait(delay)

                kit1.servo[0].angle = 135 - message.data[8] #tibia3
                kit1.servo[1].angle = 125 + message.data[7] #femur3
                wait(delay)

                kit1.servo[2].angle = 90 #coxa3
                kit1.servo[1].angle = 125 #femur3
                kit1.servo[0].angle = 135 #tibia3
                wait(10)
            if message.data[10] == 1: #wave
                pass
            if message.data[10] == 2: #tetrapod
                pass

        if message.data[9] == 1: #belok kiri/kanan bergantung derajat di gait
            kit1.servo[1].angle = 180 #femur3
            wait(delay)

            kit1.servo[2].angle = message.data[6] #coxa3
            wait(delay)

            for i in range (0, 50, 5):
                kit1.servo[1].angle = 180 - (i+10) #femur3
                kit1.servo[0].angle = 180 - (i) #tibia3
            wait(delay)

            kit1.servo[2].angle = 90 #coxa3
            kit1.servo[1].angle = 125 #femur3
            kit1.servo[0].angle = 135 #tibia3
            wait(10)

        if message.data[9] == 9: #berhenti
            kit1.servo[2].angle = 90 #coxa3
            kit1.servo[1].angle = 125 #femur3
            kit1.servo[0].angle = 135 #tibia3
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
