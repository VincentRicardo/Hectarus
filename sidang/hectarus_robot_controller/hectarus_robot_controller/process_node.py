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

delay = 0.2


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.BUTTON = 18
GPIO.LED = 23

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  #Button
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
    timeout = 100
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = time.time()
    time_timeout = time.time()
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
        super().__init__("process_node")
        self.timer_ = self.create_timer(1, self.process)

        self.subscriber_flag = self.create_subscription(Int32, "/flag_", self.flag_change, 1)

        self.publish_state = self.create_publisher(Int32MultiArray, "/state_", 1)
        self.publish_calibrate = self.create_publisher(Int32, "/calibrate_", 1)
        self.publish_count_time = self.create_publisher(Int32, "/count_time_", 1)
        self.publish_turn_on_roll = self.create_publisher(Int32, "/turn_on_roll_", 1)
        self.publish_turn_on_pitch = self.create_publisher(Int32, "/turn_on_pitch_", 1)
        self.publish_correction = self.create_publisher(Int32, "/correction_", 1)


        self.jarak = [0,0,0,0,0,0,0]
        self.flag = False
        self.constraint = 10

        self.loop = 0

        self.mode = 0
        self.stop = 2
        self.add_delay = 0 #0.4
        self.constraint_left = [11,8.5] #[27,16] #[11,8.5]

    def flag_change(self, message:Int32):
        self.flag = not self.flag

    def process(self):
        if self.stop == 1:
            state = Int32MultiArray()
            state.data = [9,0]
            self.publish_state.publish(state)
            return
        elif self.stop == 2:
            count_time = Int32()
            count_time.data = 1
            self.publish_count_time.publish(count_time)
            self.stop = 0

        self.jarak[0] = ultrasonic(TRIG[0], ECHO[0]) #ultrasonic depan
        if self.flag == True and self.mode == -4: 
            self.constraint = -99
            self.constraint_left = [27,15.5]
            self.add_delay = 0.4
            self.flag = False
            wait(5)

        self.get_logger().info("Jarak Depan: " + str(self.jarak[0]))
        self.get_logger().info("Constraint " + str(self.constraint))
        self.get_logger().info("Constraint Kiri: " + str(self.constraint_left))
        state = Int32MultiArray()
        calibrate = Int32()

        if self.constraint == -99 and self.loop != 3:
            self.loop += 1
        if self.constraint == -99 and self.loop == 3:
            self.constraint = 37

        if self.jarak[0] <= self.constraint:
            wait(2)
            state.data = [9,0] #berhenti
            self.publish_state.publish(state)
            wait(3)
            self.jarak[1] = ultrasonic(TRIG[2], ECHO[2])
            self.jarak[2] = ultrasonic(TRIG[5], ECHO[5])
            self.get_logger().info("Jarak Kanan : " + str(self.jarak[1]))
            self.get_logger().info("Jarak Kiri  : " + str(self.jarak[2]))
            wait(1)
            if self.mode == -2 or self.mode == -4: #jalan strafe ke kiri
                if self.mode == -4:
                    turn_on = Int32()
                    turn_on.data = 1
                    self.publish_turn_on_pitch.publish(turn_on)
                state.data = [11,0] #strafe kiri
                self.publish_state.publish(state)
                while True:
                    state.data = [11,0]
                    self.publish_state.publish(state)
                    wait(2 + self.add_delay)
                    self.jarak[2] = ultrasonic(TRIG[5], ECHO[5]) #ultrasonic kiri (6)
                    self.get_logger().info("Jarak Kiri : " + str(self.jarak[2]))
                    if self.jarak[2] <= self.constraint_left[0] and self.jarak[2] >= self.constraint_left[1]:
                        if self.mode == -2: #setelah strafe kiri, yawnya berubah, constraintnya berubah
                            self.mode = 3
                            self.constraint = 20
                            correction = Int32()
                            correction.data = 20
                            self.publish_correction.publish(correction)
                            break
                        elif self.mode == -4: #udah mentok kiri sampai titik finish
                            #looping stop
                            #berhenti trus ngeluarin time elapsed#
                            count_time = Int32()
                            count_time.data = 1
                            self.publish_count_time.publish(count_time)
                            self.stop = 1
                            #end of line#
                            break
            elif self.mode == 3:
                self.constraint = 0
                flag_data = Int32()
                flag_data.data = 1
                self.publish_correction.publish(flag_data)
                flag_data.data = 1
                self.publish_turn_on_roll.publish(flag_data)
                self.mode = -4

            else:
                if self.jarak[1] < self.jarak[2]:
                    state.data = [1,0] # 1 belok kiri atau 2 belok kanan
                    self.publish_state.publish(state)
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(1.2)
                    self.publish_state.publish(state)
                    wait(2)
                    calibrate.data = -1
                    self.mode = self.mode - 1
                    self.publish_calibrate.publish(calibrate)
                    wait(2)
                    state.data = [9,0]
                    self.publish_state.publish(state)
                    wait(3)


                elif self.jarak[2] < self.jarak[1]:
                    state.data = [2,0] # 1 belok kiri atau 2 belok kanan
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
                    state.data = [9,0]
                    self.publish_state.publish(state)
                    wait(3)
        
                else:
                    if self.mode == -2:
                        self.jarak[3] = ultrasonic(TRIG[2],ECHO[2])
                        self.get_logger().info("Jarak Kanan : " + str(self.jarak[3]))
                        if self.jarak[3] >= 10:
                            state.data = [0,1]
                        else:
                            state.data = [0,0]
                    else:
                        state.data = [0,0]
                    self.publish_state.publish(state)
        else:
            if self.mode == -2:
                self.jarak[3] = ultrasonic(TRIG[2],ECHO[2])
                self.get_logger().info("Jarak Kanan : " + str(self.jarak[3]))
                if self.jarak[3] >= 10:
                    state.data = [0,1]
                else:
                    state.data = [0,0]
            else:
                state.data = [0,0]
            self.publish_state.publish(state)


def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    time.sleep(5)
    GPIO.output(23, GPIO.HIGH)
    node.get_logger().info("System Ready")
    while True:
        if GPIO.input(18)==1:
            GPIO.output(23, GPIO.LOW)
            break
    rclpy.spin(node)
    rclpy.shutdown()
