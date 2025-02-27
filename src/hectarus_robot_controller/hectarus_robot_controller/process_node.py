import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import time

#kit1 = ServoKit(channels=16, address=0x41)
#kit2 = ServoKit(channels=16, address=0x40)

delay = 0.2


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.BUTTON = 18
GPIO.LED = 23

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button with pull>GPIO.setup(23, GPIO.OUT)  # LED
GPIO.setup(23, GPIO.OUT)  # LED
GPIO.output(23, GPIO.LOW)

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
        super().__init__("process_node")
        self.subscriber_ultrasonik = self.create_subscription(Int32MultiArray, "/ultrasonik_", self.ultrasonik_state, 1)


        self.publish_state = self.create_publisher(Int32, "/state_", 1)

        self.ultrasonik = [0,0,0,0,0,0,0]

    def ultrasonik_state(self, message = Int32MultiArray):
        self.ultrasonik = [message.data[0], message.data[1], message.data[2], message.data[3], message.data[4], message.data[5], message.data[6]]
        if self.ultrasonik[0] <= 4 :
            #self.get_logger().info("Ada halangan didepan")
            wait(2)
            state = Int32()
            state.data = 9 #berhenti dulu
            self.publish_state.publish(state) #kirim berhenti
            wait(5)
            state = Int32()
            state.data = 1 # 1 belok kiri atau 2 belok kanan
            self.publish_state.publish(state) #kirim belok
            wait(1.2)
            self.publish_state.publish(state)
            wait(1.2)
            self.publish_state.publish(state)
            wait(2)
            state.data = 9
            self.publish_state.publish(state)
            wait(3)
        else:
            #self.get_logger().info("Maju")
            state = Int32()
            state.data = 0 # strafe kiri
            self.publish_state.publish(state)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    #coxa ke tengah
#    kit1.servo[8].angle = 90 #coxa1
#    kit2.servo[7].angle = 90 #coxa6
#    kit1.servo[5].angle = 90 #coxa2
#    kit2.servo[10].angle = 90 #coxa5
#    kit1.servo[2].angle = 90 #coxa3
#    kit2.servo[13].angle = 90 #coxa4
#    wait(1)
    #femur naik
#    kit1.servo[7].angle = 170 #femur1
#    kit2.servo[8].angle = 10 #femur6
#    kit1.servo[4].angle = 170 #femur2
#    kit2.servo[11].angle = 10 #femur5
#    kit1.servo[1].angle = 170 #femur3
#    kit2.servo[14].angle = 10 #femur4

#    kit1.servo[6].angle = 100 #tibia1
#    kit2.servo[9].angle = 80 #tibia6
#    kit1.servo[3].angle = 100 #tibia2
#    kit2.servo[12].angle = 80 #tibia5
#    kit1.servo[0].angle = 100 #tibia3
#    kit2.servo[15].angle = 80 #tibia4
#    wait(0.5)
    #tibia naik
#    kit1.servo[6].angle = 180
#    kit2.servo[9].angle = 0
#    kit1.servo[3].angle = 180
#    kit2.servo[12].angle = 0
#    kit1.servo[0].angle = 180
#    kit2.servo[15].angle = 0
#    wait(0.5)
    #femur turun berdiri + tibia adjust
#    for i in range (0, 46, 5):
#        kit1.servo[6].angle = 180 - (i) #tibia1
#        kit2.servo[9].angle = 0 + (i) #tibia6
#        kit1.servo[3].angle = 180 - (i) #tibia2
#        kit2.servo[12].angle = 0 + (i) #tibia5
#        kit1.servo[0].angle = 180 - (i) #tibia3
#        kit2.servo[15].angle = 0 + (i) #tibia4
#        kit1.servo[7].angle = 180 - (i+5) #femur1
#        kit2.servo[8].angle = 0 + (i+10) #femur6
#        kit1.servo[4].angle = 180 - (i+5) #femur2
#        kit2.servo[11].angle = 0 + (i+10) #femur5
#        kit1.servo[1].angle = 180 - (i+5) #femur3
#        kit2.servo[14].angle = 0 + (i+10) #femur4
    GPIO.output(23, GPIO.HIGH)
    node.get_logger().info("System Ready")
    while True:
        if GPIO.input(18)==1:
            GPIO.output(23, GPIO.LOW)
            break
    rclpy.spin(node)
    rclpy.shutdown()
