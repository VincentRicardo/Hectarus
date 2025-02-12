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
delay = 0.2

class MyNode(Node):
    def __init__(self):
        super().__init__("leg6_node")
        self.subscriber_angle = self.create_subscription(Int32MultiArray, "/angle_", self.move, 1)

    def move(self, message = Int32MultiArray):
        if message.data[9] == 0: #maju
            if message.data[10] == 0: #tripod
                wait(10)
                for i in range(0, 46, 5):
                    kit2.servo[8].angle = 55 - i #femur6
                    kit2.servo[9].angle = 45 - (i) #tibia6
                wait(delay)

                kit2.servo[7].angle = 90 - message.data[3] #coxa6
                wait(delay)

                kit2.servo[9].angle = (45 + message.data[5]) #tibia6
                kit2.servo[8].angle = (55 - message.data[4]) #femur6
                wait(delay)

                kit2.servo[7].angle = 90 #coxa6
                kit2.servo[8].angle = 55 #femur6
                kit2.servo[9].angle = 45 #tibia6
            if message.data[10] == 1: #wave
                pass
            if message.data[10] == 2: #tetrapod
                pass

        if message.data[9] == 1: #belok kiri/kanan bergantung derajat di gait
            wait(10)
            kkit2.servo[8].angle = 0 #femur6
            wait(delay)

            kit2.servo[7].angle = message.data[0] #coxa6
            wait(delay)

            for i in range (0, 50, 5):
                kit2.servo[8].angle = 0 + (i+10) #femur6
                kit2.servo[9].angle = 0 + (i) #tibia6
            wait(delay)

            kit2.servo[7].angle = 90 #coxa6
            kit2.servo[8].angle = 55 #femur6
            kit2.servo[9].angle = 45 #tibia6


        if message.data[9] == 9: #berhenti
            kit2.servo[7].angle = 90 #coxa6
            kit2.servo[8].angle = 55  #femur6
            kit2.servo[9].angle = 45 #tibia6
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
