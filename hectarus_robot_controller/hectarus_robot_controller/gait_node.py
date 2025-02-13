import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Int32
import time
import math

coxa = 2.55
femur = 6.508
tibia = 7.964
l = 6.508
maju = 4
gait = 0 #0 tripod, 1 wave, 2 tetrapod


def IK_berdiri():
    maju = 0
    alpha1 = math.asin(l/femur)
    h = math.sqrt(math.pow(femur,2)+math.pow(tibia,2)-(2*femur*tibia*math.cos(alpha1))-(math.sin(alpha1)*math.sin(alpha1)*femur*femur))
    sudut_base_coxa_tengah = math.degrees(math.atan(maju/(l+coxa)))
    P = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)) #panjang diagonal setelah kaki maju
    P = P-coxa
    M = math.sqrt(math.pow(h,2)+math.pow(P,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(M,2)-math.pow(tibia,2))/(2*femur*M)))
    sudut_coxa_femur_2_tengah = math.degrees(math.acos((math.pow(M,2)+math.pow(h,2)-math.pow(P,2))/(2*h*M)))
    sudut_coxa_femur_total = sudut_coxa_femur_1_tengah + sudut_coxa_femur_2_tengah
    sudut_femur_tibia_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(M,2))/(2*tibia*femur)))

    PD = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)-(2*maju*(l+coxa)*math.cos(math.radians(135))))
    sudut_base_coxa_depan = math.degrees(math.acos((math.pow((l+coxa),2)+math.pow(PD,2)-math.pow(maju,2))/(2*(l+coxa)*PD)))
    PD = PD-coxa
    MD = math.sqrt(math.pow(h,2)+math.pow(PD,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(MD,2)-math.pow(tibia,2))/(2*femur*MD)))
    sudut_coxa_femur_2_depan = math.degrees(math.acos((math.pow(MD,2)+math.pow(h,2)-math.pow(PD,2))/(2*h*MD)))
    sudut_coxa_femur_total_depan = sudut_coxa_femur_1_depan + sudut_coxa_femur_2_depan
    sudut_femur_tibia_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MD,2))/(2*tibia*femur)))


    PB = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)-(2*maju*(l+coxa)*math.cos(math.radians(45))))
    sudut_base_coxa_belakang = math.degrees(math.acos((math.pow((l+coxa),2)+math.pow(PB,2)-math.pow(maju,2))/(2*(l+coxa)*PB)))
    PB = PB - coxa
    MB = math.sqrt(math.pow(h,2)+math.pow(PB,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(MB,2)-math.pow(tibia,2))/(2*femur*M)))
    sudut_coxa_femur_2_belakang = math.degrees(math.acos((math.pow(MB,2)+math.pow(h,2)-math.pow(PB,2))/(2*h*MB)))
    sudut_coxa_femur_total_belakang = sudut_coxa_femur_1_belakang + sudut_coxa_femur_2_belakang
    sudut_femur_tibia_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MB,2))/(2*tibia*femur)))
    return (sudut_base_coxa_tengah, sudut_coxa_femur_total, sudut_femur_tibia_tengah, sudut_base_coxa_depan, sudut_coxa_femur_total_depan, sudut_femur_tibia_depan, sudut_base_coxa_belakang, sudut_coxa_femur_total_belakang, sudut_femur_tibia_belakang)
    

sudut_base_coxa_tengah_berdiri, sudut_coxa_femur_total_berdiri, sudut_femur_tibia_tengah_berdiri, sudut_base_coxa_depan_berdiri, sudut_coxa_femur_total_depan_berdiri, sudut_femur_tibia_depan_berdiri, sudut_base_coxa_belakang_berdiri, sudut_coxa_femur_total_belakang_berdiri, sudut_femur_tibia_belakang_berdiri = IK_berdiri()

def IK_maju(maju):
    alpha1 = math.asin(l/femur)
    h = math.sqrt(math.pow(femur,2)+math.pow(tibia,2)-(2*femur*tibia*math.cos(alpha1))-(math.sin(alpha1)*math.sin(alpha1)*femur*femur))
    sudut_base_coxa_tengah = math.degrees(math.atan(maju/(l+coxa)))
    P = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)) #panjang diagonal setelah kaki maju
    P = P-coxa
    M = math.sqrt(math.pow(h,2)+math.pow(P,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(M,2)-math.pow(tibia,2))/(2*femur*M)))
    sudut_coxa_femur_2_tengah = math.degrees(math.acos((math.pow(M,2)+math.pow(h,2)-math.pow(P,2))/(2*h*M)))
    sudut_coxa_femur_total = sudut_coxa_femur_1_tengah + sudut_coxa_femur_2_tengah
    sudut_femur_tibia_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(M,2))/(2*tibia*femur)))

    PD = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)-(2*maju*(l+coxa)*math.cos(math.radians(135))))
    sudut_base_coxa_depan = math.degrees(math.acos((math.pow((l+coxa),2)+math.pow(PD,2)-math.pow(maju,2))/(2*(l+coxa)*PD)))
    PD = PD-coxa
    MD = math.sqrt(math.pow(h,2)+math.pow(PD,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(MD,2)-math.pow(tibia,2))/(2*femur*MD)))
    sudut_coxa_femur_2_depan = math.degrees(math.acos((math.pow(MD,2)+math.pow(h,2)-math.pow(PD,2))/(2*h*MD)))
    sudut_coxa_femur_total_depan = sudut_coxa_femur_1_depan + sudut_coxa_femur_2_depan
    sudut_femur_tibia_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MD,2))/(2*tibia*femur)))

    PB = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)-(2*maju*(l+coxa)*math.cos(math.radians(45))))
    sudut_base_coxa_belakang = math.degrees(math.acos((math.pow((l+coxa),2)+math.pow(PB,2)-math.pow(maju,2))/(2*(l+coxa)*PB)))
    PB = PB - coxa
    MB = math.sqrt(math.pow(h,2)+math.pow(PB,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(MB,2)-math.pow(tibia,2))/(2*femur*M)))
    sudut_coxa_femur_2_belakang = math.degrees(math.acos((math.pow(MB,2)+math.pow(h,2)-math.pow(PB,2))/(2*h*MB)))
    sudut_coxa_femur_total_belakang = sudut_coxa_femur_1_belakang + sudut_coxa_femur_2_belakang
    sudut_femur_tibia_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MB,2))/(2*tibia*femur)))
    base_coxa_tengah, coxa_femur_tengah, femur_tibia_tengah, base_coxa_depan, coxa_femur_depan, femur_tibia_depan, base_coxa_belakang, coxa_femur_belakang, femur_tibia_belakang = IK_berdiri()

    return (sudut_base_coxa_tengah-base_coxa_tengah, sudut_coxa_femur_total-coxa_femur_tengah, sudut_femur_tibia_tengah - femur_tibia_tengah, sudut_base_coxa_depan - base_coxa_depan, sudut_coxa_femur_total_depan - coxa_femur_depan, sudut_femur_tibia_depan - femur_tibia_depan, sudut_base_coxa_belakang - base_coxa_belakang, sudut_coxa_femur_total_belakang - coxa_femur_belakang, sudut_femur_tibia_belakang - femur_tibia_belakang)


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
        super().__init__("gait_node")

        self.subscriber_move = self.create_subscription(Int32MultiArray, "/gait_", self.move, 1) #fungsi buat mulai jalan tapi harus dapet data gyro dulu dengan fungsi trigger

        self.publish_tripod_angle = self.create_publisher(Int32MultiArray, "/tripod_angle_", 1)
        self.publish_wave_angle = self.create_publisher(Int32MultiArray, "/wave_angle_", 1)
        self.publish_tetrapod_angle = self.create_publisher(Int32MultiArray, "/tetrapod_angle_", 1)
        self.publish_turn_angle = self.create_publisher(Int32MultiArray, "/turn_angle_", 1)
        self.publish_stop_angle = self.create_publisher(Int32MultiArray, "/stop_angle_", 1)

    def move(self, message = Int32MultiArray):
        self.get_logger().info("Receiving Yaw = " + str(message.data[0])+ " & Roll = " + str(message.data[1]) + ", & State = " + str(message.data[2]))
        if message.data[2] == 0: #maju
            if gait == 0: #tripod
                angle = Int32MultiArray()
                a, b, c, d, e, f, g, h, i = IK_maju(maju)
                angle.data = [int(a), int(b), int(c), int(d), int(e), int(f), int(g), int(h), int(i), int(sudut_coxa_femur_total_berdiri), int(sudut_femur_tibia_tengah_berdiri), int(sudut_coxa_femur_total_depan_berdiri), int(sudut_femur_tibia_depan_berdiri), int(sudut_coxa_femur_total_belakang_berdiri), int(sudut_femur_tibia_belakang_berdiri)]
                self.get_logger().info("Sending Tripod Angle")
                self.publish_tripod_angle.publish(angle)
            if gait == 1: #wave
                step = maju
                decrement_wave = maju/5
                for i in range (6):
                    base_coxa_tengah, coxa_femur_tengah, femur_tibia_tengah, base_coxa_depan, coxa_femur_depan, femur_tibia_depan, base_coxa_belakang, coxa_femur_belakang, femur_tibia_belakang = IK_maju(step)
                    message.data[i] = [int(base_coxa_tengah), int(coxa_femur_tengah), int(femur_tibia_tengah), int(base_coxa_depan), int(coxa_femur_depan), int(femur_tibia_depan), int(base_coxa_belakang), int(coxa_femur_belakang), int(femur_tibia_belakang)]
                    step = step - decrement
                message.data[6] = [int(sudut_base_coxa_tengah_berdiri), int(sudut_coxa_femur_total_berdiri), int(sudut_femur_tibia_tengah_berdiri), int(sudut_base_coxa_depan_berdiri), int(sudut_coxa_femur_total_depan_berdiri), int(sudut_femur_tibia_depan_berdiri), int(sudut_base_coxa_belakang_berdiri), int(sudut_coxa_femur_total_belakang_berdiri), int(sudut_femur_tibia_belakang_berdiri)]
                self.get_logger().info("Sending Wave Angle")
                self.publish_wave_angle.publish(angle)
            if gait == 2: #tetrapod
                pass

        if message.data[2] == 1: #kiri
            angle = Int32MultiArray()
            angle.data = [60, int(sudut_coxa_femur_total_berdiri), int(sudut_femur_tibia_tengah_berdiri), 60, int(sudut_coxa_femur_total_depan_berdiri), int(sudut_femur_tibia_depan_berdiri), 60, int(sudut_coxa_femur_total_belakang_berdiri), int(sudut_femur_tibia_belakang_berdiri)]
            self.get_logger().info("Sending Angle Left")
            self.publish_turn_angle.publish(angle)

        if message.data[2] == 2 :
            angle = Int32MultiArray()
            angle.data = [120, int(sudut_coxa_femur_total_berdiri), int(sudut_femur_tibia_tengah_berdiri), 120, int(sudut_coxa_femur_total_depan_berdiri), int(sudut_femur_tibia_depan_berdiri), 120, int(sudut_coxa_femur_total_belakang_berdiri), int(sudut_femur_tibia_belakang_berdiri)]
            self.get_logger().info("Sending Angle Right")
            self.publish_turn_angle.publish(angle)

        if message.data[2] == 9 :
            angle = Int32MultiArray()
            angle.data = [90, int(sudut_coxa_femur_total_berdiri), int(sudut_femur_tibia_tengah_berdiri), 90, int(sudut_coxa_femur_total_depan_berdiri), int(sudut_femur_tibia_depan_berdiri), 90, int(sudut_coxa_femur_total_belakang_berdiri), int(sudut_femur_tibia_belakang_berdiri)]
            self.get_logger().info("Stop")
            self.publish_stop_angle.publish(angle)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()
