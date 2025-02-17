import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import time
import RPi.GPIO as GPIO

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
            state = Int32()
            state.data = 9 #berhenti dulu
            self.publish_state.publish(state) #kirim berhenti
            wait(3)
            state = Int32()
            state.data = 1 # 1 belok kiri atau 2 belok kanan
            self.publish_state.publish(state) #kirim belok
        else:
            #self.get_logger().info("Maju")
            state = Int32()
            state.data = 0 # 0 maju
            self.publish_state.publish(state)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    GPIO.output(23, GPIO.HIGH)
    node.get_logger().info("System Ready")
    while True:
        if GPIO.input(18)==1:
            GPIO.output(23, GPIO.LOW)
            break
    rclpy.spin(node)
    rclpy.shutdown()
