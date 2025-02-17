import rclpy
import RPi.GPIO as GPIO
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

TRIG = [19, 6, 22, 17, 21, 16, 25]
ECHO = [26, 13, 5, 27, 20, 12, 24]
for i in range (0,7):
    GPIO.setup(TRIG[i],GPIO.OUT)
    GPIO.output(TRIG[i], False)
    GPIO.setup(ECHO[i],GPIO.IN)

def ultrasonic(TRIG, ECHO):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = time.time()
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance


class MyNode(Node):
    def __init__(self):
        super().__init__("ultrasonik_node")
        self.timer_ = self.create_timer(1, self.calculate_send_ultrasonik)
        self.publish_data = self.create_publisher(Int32MultiArray, "/ultrasonik_", 1)

        self.ultrasonik = [0,0,0,0,0,0,0]

    def calculate_send_ultrasonik(self):
        us = Int32MultiArray()
        for i in range (0,7):
            if i != 1:
                self.ultrasonik[i] = ultrasonic(TRIG[i], ECHO[i])
                self.get_logger().info("Distance Ultrasonik " + str(i+1) + ": " + str(self.ultrasonik[i]) + " cm")
            else:
                self.ultrasonik[1] = 20
        us.data = [int(self.ultrasonik[0]),int(self.ultrasonik[1]),int(self.ultrasonik[2]),int(self.ultrasonik[3]),int(self.ultrasonik[4]),int(self.ultrasonik[5]),int(self.ultrasonik[6])]
        #self.get_logger().info("")
        self.publish_data.publish(us)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
