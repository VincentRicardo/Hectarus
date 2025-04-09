import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import time
import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
import board
import busio
import time
import adafruit_vl53l0x

#i2c = busio.I2C(board.SCL, board.SDA)
#vl53 = adafruit_vl53l0x.VL53L0X(i2c, 41)


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
        self.timer_ = self.create_timer(1, self.process)

        self.subscriber_flag = self.create_subscription(Int32, "/flag_", self.flag_change, 1)

        self.publish_state = self.create_publisher(Int32, "/state_", 1)
        self.publish_calibrate = self.create_publisher(Int32, "/calibrate_", 1)

        self.jarak = [0,0,0,0,0,0,0]
        self.flag = False
        self.constraint = 10

        self.trigger_strafe = 0

    def flag_change(self, message:Int32):
        self.flag = not self.flag

    def process(self):
        self.jarak[0] = ultrasonic(TRIG[0], ECHO[0]) #vl53.range/10
        if self.flag == True:
            self.constraint = 3
        else:
            self.constraint = 10
        self.get_logger().info("Jarak Depan: " + str(self.jarak[0]))
        self.get_logger().info("Constraint " + str(self.constraint))
        state = Int32()
        calibrate = Int32()
        if self.jarak[0] <= self.constraint:
            wait(2)
            state.data = 9 #berhenti dulu
            self.publish_state.publish(state) #kirim berhenti
            wait(3)
            self.jarak[1] = ultrasonic(TRIG[2], ECHO[2])
            self.jarak[2] = ultrasonic(TRIG[5], ECHO[5])
            self.get_logger().info("Jarak Kanan : " + str(self.jarak[1]))
            self.get_logger().info("Jarak Kiri  : " + str(self.jarak[2]))
            wait(1)
            #self.get_logger().info("Ada halangan didepan")
            if self.trigger_strafe == -2:
                state.data = 11
                self.publish_state.publish(state)
                while True:
                    state.data = 11
                    self.publish_state.publish(state)
                    wait(2.5)
                    self.jarak[2] = ultrasonic(TRIG[5], ECHO[5])
                    self.get_logger().info("Jarak Kiri : " + str(self.jarak[2]))
                    if self.jarak[2] <= 10:
                        self.trigger_strafe = 2
                        break
                #strafe kiri gatau sampe mana pokoknya sampe kiri nya dah deket
                #ganti flag supaya nanti strafe kanan sampe kanannya dah deket
            elif self.trigger_strafe == 2:
                state.data = 22
                self.publish_state.publish(state)
                while True:
                    state.data = 22
                    self.publish_state.publish(state)
                    wait(2.5)
                    self.jarak[1] = ultrasonic(TRIG[5], ECHO[5])
                    self.get_logger().info("Jarak Kanan : " + str(self.jarak[1]))
                    if self.jarak[1] <= 10:
                        self.trigger_strafe = 0
                        break
            else:
                if self.jarak[1] < self.jarak[2]:
                    state.data = 1 # 1 belok kiri atau 2 belok kanan
                    self.publish_state.publish(state) #kirim belok
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(2)
                    calibrate.data = -1
                    self.trigger_strafe = self.trigger_strafe - 1
                    self.publish_calibrate.publish(calibrate)
                    wait(2)
                    state.data = 9
                    self.publish_state.publish(state)
                    wait(3)
                elif self.jarak[2] < self.jarak[1]:
                    state.data = 2 # 1 belok kiri atau 2 belok kanan
                    self.publish_state.publish(state) #kirim belok
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(2)
                    calibrate.data = 1
                    self.trigger_strafe = self.trigger_strafe + 1
                    self.publish_calibrate.publish(calibrate)
                    wait(2)
                    state.data = 9
                    self.publish_state.publish(state)
                    wait(3)
                else:
                    state.data = 0
                    self.publish_state.publish(state)
        else:
            #self.get_logger().info("Maju")
            state.data = 0
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
