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
        super().__init__("wave_gait_node")
        self.subscriber_angle = self.create_subscription(Int32MultiArray, "/wave_angle_", self.move, 1)

    def move(self, message = Int32MultiArray):
        #femur 1 angkat
        kit1.servo[7].angle = 170 #femur1
        kit1.servo[6].angle = 180 #tibia1
        wait(delay)
        
        #coxa 1 maju sisanya mundur
        kit1.servo[8].angle =  90 + message.data[0][3] #coxa1
        
        kit2.servo[7].angle =  90 - message.data[1][3] #coxa6
        kit2.servo[8].angle = (180 - message.data[6][4]) - message.data[1][4] #femur6
        kit2.servo[9].angle = (180 - message.data[6][5]) + message.data[1][5] #tibia6
        
        kit1.servo[5].angle = 90 + message.data[5][0] #coxa2
        kit1.servo[4].angle = message.data[6][1] + message.data[5][1] #femur2
        kit1.servo[3].angle = message.data[6][2] - message.data[5][2] #tibia2

        kit2.servo[10].angle = 90 - message.data[2][0] #coxa5
        kit2.servo[11].angle = (180 - message.data[6][1]) - message.data[2][1] #femur5
        kit2.servo[12].angle = (180 - message.data[6][2]) + message.data[2][2] #tibia5

        kit1.servo[2].angle = 90 + message.data[4][6] #coxa3
        kit1.servo[1].angle = message.data[6][7] + message.data[4][7] #femur3
        kit1.servo[0].angle = message.data[6][8] - message.data[4][8] #tibia3

        kit2.servo[13].angle = 90 - message.data[3][6] #coxa4
        kit2.servo[14].angle = (180 - message.data[6][7]) - message.data[3][7] #femur4
        kit2.servo[15].angle = (180 - message.data[6][8]) + message.data[3][8] #tibia4
        wait(delay)


        #femur 1 turun dan tibia turun sekalian adjust ngambil kaki
        kit1.servo[6].angle = message.data[6][5] - message.data[0][5] #tibia1
        sleep(0.1)
        kit1.servo[7].angle = message.data[6][4] + message.data[0][4] #femur1
        wait(delay)

        #femur 2 angkat
        kit1.servo[4].angle = 170 #femur2
        kit1.servo[3].angle = 180 #tibia2
        wait(delay)

        #coxa 2 maju sisanya mundur
        kit1.servo[8].angle =  90 + message.data[1][3] #coxa1
        kit1.servo[7].angle = message.data[6][4] + message.data[1][4] #femur1
        kit1.servo[6].angle = message.data[6][5] - message.data[1][5] #tibia1
        
        kit2.servo[7].angle =  90 - message.data[2][3] #coxa6
        kit2.servo[8].angle = (180 - message.data[6][4]) - message.data[2][4] #femur6
        kit2.servo[9].angle = (180 - message.data[6][5]) + message.data[2][5] #tibia6

        kit1.servo[5].angle = 90 + message.data[1][0] #coxa2

        kit2.servo[10].angle = 90 - message.data[3][0] #coxa5
        kit2.servo[11].angle = (180 - message.data[6][1]) - message.data[3][1] #femur5
        kit2.servo[12].angle = (180 - message.data[6][2]) + message.data[3][2] #tibia5

        kit1.servo[2].angle = 90 + message.data[5][6] #coxa3
        kit1.servo[1].angle = message.data[6][7] + message.data[5][7] #femur3
        kit1.servo[0].angle = message.data[6][8] - message.data[5][8] #tibia3

        kit2.servo[13].angle = 90 - message.data[4][6] #coxa4
        kit2.servo[14].angle = (180 - message.data[6][7]) - message.data[4][7] #femur4
        kit2.servo[15].angle = (180 - message.data[6][8]) + message.data[4][8] #tibia4
        wait(delay)

	#femur tibia 2 turun
        kit1.servo[3].angle = message.data[6][2] - message.data[1][2] #tibia2
        sleep(0.1)
        kit1.servo[4].angle = message.data[6][1] + message.data[1][1] #femur2
        wait(delay)

        #femur tibia 3 naik
        kit1.servo[1].angle = 170 #femur3
        kit1.servo[0].angle = 180 #tibia3

 	#coxa 3 maju sisanya mundur 5 derajat
        kit1.servo[8].angle =  90 + message.data[2][3] #coxa1
        kit1.servo[7].angle = message.data[6][4] + message.data[2][4] #femur1
        kit1.servo[6].angle = message.data[6][5] - message.data[2][5] #tibia1
        
        kit2.servo[7].angle =  90 - message.data[3][3] #coxa6
        kit2.servo[8].angle = (180 - message.data[6][4]) - message.data[3][4] #femur6
        kit2.servo[9].angle = (180 - message.data[6][5]) + message.data[3][5] #tibia6

        kit1.servo[5].angle = 90 + message.data[1][0] #coxa2
        kit1.servo[4].angle = message.data[6][1] + message.data[1][1] #femur2
        kit1.servo[3].angle = message.data[6][2] - message.data[1][2] #tibia2

        kit2.servo[10].angle = 90 - message.data[4][0] #coxa5
        kit2.servo[11].angle = (180 - message.data[6][1]) - message.data[4][1] #femur5
        kit2.servo[12].angle = (180 - message.data[6][2]) + message.data[4][2] #tibia5

        kit1.servo[2].angle = 90 + message.data[0][6] #coxa3

        kit2.servo[13].angle = 90 - message.data[5][6] #coxa4
        kit2.servo[14].angle = (180 - message.data[6][7]) - message.data[5][7] #femur4
        kit2.servo[15].angle = (180 - message.data[6][8]) + message.data[5][8] #tibia4
        wait(delay)

	#femur tibia 3 turun
        kit1.servo[0].angle = message.data[6][8] - message.data[0][8] #tibia3
        sleep(0.1)
        kit1.servo[1].angle = message.data[6][7] + message.data[0][7] #femur3
        wait(delay)

	#femur 4 angkat
        kit2.servo[14].angle = 10 #femur4
        kit2.servo[15].angle = 0 #tibia4
        wait(delay)

	#coxa 4 maju sisanya mundur 5 derajat
        kit1.servo[8].angle =  90 + message.data[3][3] #coxa1
        kit1.servo[7].angle = message.data[6][4] + message.data[3][4] #femur1
        kit1.servo[6].angle = message.data[6][5] - message.data[3][5] #tibia1
        
        kit2.servo[7].angle =  90 - message.data[4][3] #coxa6
        kit2.servo[8].angle = (180 - message.data[6][4]) - message.data[4][4] #femur6
        kit2.servo[9].angle = (180 - message.data[6][5]) + message.data[4][5] #tibia6

        kit1.servo[5].angle = 90 + message.data[2][0] #coxa2
        kit1.servo[4].angle = message.data[6][1] + message.data[2][1] #femur2
        kit1.servo[3].angle = message.data[6][2] - message.data[2][2] #tibia2

        kit2.servo[10].angle = 90 - message.data[5][0] #coxa5
        kit2.servo[11].angle = (180 - message.data[6][1]) - message.data[5][1] #femur5
        kit2.servo[12].angle = (180 - message.data[6][2]) + message.data[5][2] #tibia5

        kit1.servo[2].angle = 90 + message.data[1][6] #coxa3
        kit1.servo[1].angle = message.data[6][7] + message.data[1][7] #femur3
        kit1.servo[0].angle = message.data[6][8] - message.data[1][8] #tibia3

        kit2.servo[13].angle = 90 - message.data[0][6] #coxa4

        wait(delay)
	    
	#femur tibia 4 turun
        kit2.servo[15].angle = (180 - message.data[6][8]) + message.data[0][8] #tibia4
        sleep(0.1)
        kit2.servo[14].angle = (180 - message.data[6][7]) - message.data[0][7] #femur4
        wait(delay)

	#femur 5 angkat
        kit2.servo[11].angle = 10 #femur5
        kit2.servo[12].angle = 0 #tibia5
        wait(delay)

	#coxa 5 maju sisanya mundur 5 derajat
        kit1.servo[8].angle =  90 + message.data[4][3] #coxa1
        kit1.servo[7].angle = message.data[6][4] + message.data[4][4] #femur1
        kit1.servo[6].angle = message.data[6][5] - message.data[4][5] #tibia1
        
        kit2.servo[7].angle =  90 - message.data[5][3] #coxa6
        kit2.servo[8].angle = (180 - message.data[6][4]) - message.data[5][4] #femur6
        kit2.servo[9].angle = (180 - message.data[6][5]) + message.data[5][5] #tibia6

        kit1.servo[5].angle = 90 + message.data[3][0] #coxa2
        kit1.servo[4].angle = message.data[6][1] + message.data[3][1] #femur2
        kit1.servo[3].angle = message.data[6][2] - message.data[3][2] #tibia2

        kit2.servo[10].angle = 90 - message.data[0][0] #coxa5

        kit1.servo[2].angle = 90 + message.data[2][6] #coxa3
        kit1.servo[1].angle = message.data[6][7] + message.data[2][7] #femur3
        kit1.servo[0].angle = message.data[6][8] - message.data[2][8] #tibia3

        kit2.servo[13].angle = 90 - message.data[1][6] #coxa4
        kit2.servo[14].angle = (180 - message.data[6][7]) - message.data[1][7] #femur4
        kit2.servo[15].angle = (180 - message.data[6][8]) + message.data[1][8] #tibia4
        wait(delay)
	    
	#femur tibia 5 turun
        kit2.servo[12].angle = (180 - message.data[6][2]) + message.data[0][2] #tibia5
        sleep(0.1)
        kit2.servo[11].angle = (180 - message.data[6][1]) - message.data[0][1] #femur5
        wait(delay)

	#femur 6 angkat
        kit2.servo[8].angle = 10 #femur6
        kit2.servo[9].angle = 0 #tibia6
        wait(delay)

	#coxa 6 maju sisanya mundur 5 derajat
        kit1.servo[8].angle =  90 + message.data[5][3] #coxa1
        kit1.servo[7].angle = message.data[6][4] + message.data[5][4] #femur1
        kit1.servo[6].angle = message.data[6][5] - message.data[5][5] #tibia1
        
        kit2.servo[7].angle =  90 - message.data[0][3] #coxa6

        kit1.servo[5].angle = 90 + message.data[4][0] #coxa2
        kit1.servo[4].angle = message.data[6][1] + message.data[4][1] #femur2
        kit1.servo[3].angle = message.data[6][2] - message.data[4][2] #tibia2

        kit2.servo[10].angle = 90 - message.data[1][0] #coxa5
        kit2.servo[11].angle = (180 - message.data[6][1]) - message.data[1][1] #femur5
        kit2.servo[12].angle = (180 - message.data[6][2]) + message.data[1][2] #tibia5

        kit1.servo[2].angle = 90 + message.data[3][6] #coxa3
        kit1.servo[1].angle = message.data[6][7] + message.data[3][7] #femur3
        kit1.servo[0].angle = message.data[6][8] - message.data[3][8] #tibia3

        kit2.servo[13].angle = 90 - message.data[2][6] #coxa4
        kit2.servo[14].angle = (180 - message.data[6][7]) - message.data[2][7] #femur4
        kit2.servo[15].angle = (180 - message.data[6][8]) + message.data[2][8] #tibia4
        wait(delay)
	    
	#femur tibia 6 turun
        kit2.servo[9].angle = (180 - message.data[6][4]) + message.data[0][5] #tibia6
        sleep(0.1)
        kit2.servo[8].angle = (180 - message.data[6][5]) - message.data[0][4] #femur6
        wait(delay)
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
