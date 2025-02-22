import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import math
from adafruit_servokit import ServoKit
import time
import numpy as np

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
        rows = message.layout.dim[0].size
        cols = message.layout.dim[1].size
        data = np.array(message.data).reshape(rows, cols)
        self.get_logger().info(f"Data: {data}")

        #femur 1 4 angkat
        kit1.servo[7].angle = data[3][4] + 45 #femur1
        kit2.servo[14].angle = 180 - data[3][7] - 45 #femur4
        kit1.servo[6].angle = 180 - data[3][5] + 45 #tibia1
        kit2.servo[15].angle = data[3][8] - 45 #tibia4
        wait(delay)
        
        #coxa 1 4 maju sisanya mundur
        kit1.servo[8].angle =  90 + data[0][3] #coxa1
        kit2.servo[13].angle = 90 - data[0][6+9] #coxa4
        
        kit2.servo[7].angle =  90 - data[1][3+9] #coxa6
        kit2.servo[8].angle = (180 - data[3][4]) - data[1][4+9] #femur6
        kit2.servo[9].angle = (data[3][5]) + data[1][5+9] #tibia6
        
        kit1.servo[5].angle = 90 + data[1][0] #coxa2
        kit1.servo[4].angle = data[3][1] + data[1][1] #femur2
        kit1.servo[3].angle = 180 - data[3][2] - data[1][2] #tibia2

        kit2.servo[10].angle = 90 - data[2][0+9] #coxa5
        kit2.servo[11].angle = (180 - data[3][1]) - data[2][1+9] #femur5
        kit2.servo[12].angle = (data[3][2]) + data[2][2+9] #tibia5

        kit1.servo[2].angle = 90 + data[2][6] #coxa3
        kit1.servo[1].angle = data[3][7] + data[2][7] #femur3
        kit1.servo[0].angle = 180 - data[3][8] - data[2][8] #tibia3


        #femur 1 4 turun dan tibia turun sekalian adjust ngambil kaki
        kit1.servo[6].angle = 180 - data[3][5] - data[0][5] #tibia1
        kit2.servo[15].angle = (data[3][8]) + data[0][8+9] #tibia4
        wait(0.1)
        kit1.servo[7].angle = data[3][4] + data[0][4] #femur1
        kit2.servo[14].angle = (180 - data[3][7]) - data[0][7+9] #femur4
        wait(delay)

        #femur tibia 3 5 naik
        kit1.servo[1].angle = data[3][7] + 45 #femur3
        kit2.servo[11].angle = 180 - data[3][1] - 45 #femur5
        kit1.servo[0].angle = 180 - data[3][8] + 45 #tibia3
        kit2.servo[12].angle = data[3][2] - 45 #tibia5
        wait(delay)

 	#coxa 3 5 maju sisanya mundur
        kit1.servo[8].angle =  90 + data[1][3] #coxa1
        kit1.servo[7].angle = data[3][4] + data[1][4] #femur1
        kit1.servo[6].angle = 180 - data[3][5] - data[1][5] #tibia1

        kit2.servo[7].angle =  90 - data[2][3+9] #coxa6
        kit2.servo[8].angle = (180 - data[3][4]) - data[2][4+9] #femur6
        kit2.servo[9].angle = (data[3][5]) + data[2][5+9] #tibia6

        kit1.servo[5].angle = 90 + data[2][0] #coxa2
        kit1.servo[4].angle = data[3][1] + data[2][1] #femur2
        kit1.servo[3].angle = 180 - data[3][2] - data[2][2] #tibia2

        kit1.servo[2].angle = 90 + data[0][6] #coxa3
        kit2.servo[10].angle = 90 - data[0][0+9] #coxa5

        kit2.servo[13].angle = 90 - data[1][6+9] #coxa4
        kit2.servo[14].angle = (180 - data[3][7]) - data[1][7+9] #femur4
        kit2.servo[15].angle = (data[3][8]) + data[1][8+9] #tibia4

	#femur tibia 3 turun
        kit1.servo[0].angle = 180 - data[3][8] - data[0][8] #tibia3
        kit2.servo[12].angle = (data[3][2]) + data[0][2+9] #tibia5
        wait(0.1)
        kit1.servo[1].angle = data[3][7] + data[0][7] #femur3
        kit2.servo[11].angle = (180 - data[3][1]) - data[0][1+9] #femur5
        wait(delay)

        #femur 2 6 angkat
        kit1.servo[4].angle = data[3][1] + 45 #femur2
        kit2.servo[8].angle = 180 - data[3][4] - 45 #femur6
        kit1.servo[3].angle = 180 - data[3][2] + 45 #tibia2
        kit2.servo[9].angle =  data[3][5] - 45 #tibia6
        wait(delay)

        #coxa 2 6 maju sisanya mundur
        kit1.servo[8].angle =  90 + data[2][3] #coxa1
        kit1.servo[7].angle = data[3][4] + data[2][4] #femur1
        kit1.servo[6].angle = 180 - data[3][5] - data[2][5] #tibia1

        kit1.servo[5].angle = 90 + data[0][0] #coxa2
        kit2.servo[7].angle =  90 - data[0][3+9] #coxa6

        kit2.servo[10].angle = 90 - data[1][0+9] #coxa5
        kit2.servo[11].angle = (180 - data[3][1]) - data[1][1+9] #femur5
        kit2.servo[12].angle = (data[3][2]) + data[1][2+9] #tibia5

        kit1.servo[2].angle = 90 + data[1][6] #coxa3
        kit1.servo[1].angle = data[3][7] + data[1][7] #femur3
        kit1.servo[0].angle = 180 - data[3][8] - data[1][8] #tibia3

        kit2.servo[13].angle = 90 - data[2][6+9] #coxa4
        kit2.servo[14].angle = (180 - data[3][7]) - data[2][7+9] #femur4
        kit2.servo[15].angle = (data[3][8]) + data[2][8+9] #tibia4

	#femur tibia 2 turun
        kit1.servo[3].angle = 180 - data[3][2] - data[0][2] #tibia2
        kit2.servo[9].angle = (data[3][5]) + data[0][5+9] #tibia6
        wait(0.1)
        kit1.servo[4].angle = data[3][1] + data[0][1] #femur2
        kit2.servo[8].angle = (180 - data[3][4]) - data[0][4+9] #femur6
        wait(delay)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
