from time import sleep
from adafruit_servokit import ServoKit

import math

kit1 = ServoKit(channels = 16, address = 0x41)
kit2 = ServoKit(channels = 16, address = 0x40)

coxa = 2.644
femur = 6.436
tibia = 8.122
l = 6.436
maju = 4
forward = maju

roll = 0

lebar_depan_belakang = 24.5
lebar_tengah = 33.5

panjang_depan_belakang = 23.3
panjang_depan_tengah = 11.65

def nilai_h(panjang, derajat):
    #alpha1 = math.asin(l/femur)
    #if derajat != 0:
    #    alpha1 = math.radians(180) - alpha1
    #h = math.sqrt(math.pow(femur,2)+math.pow(tibia,2)-(2*femur*tibia*math.cos(alpha1))-(math.sin(alpha1)*math.sin(alpha1)*femur*femur)) 
    h = tibia + (math.tan(math.radians(derajat))*panjang)
    alpha1 = math.acos(((femur*tibia)-(math.sqrt((math.pow(femur,2)*math.pow(tibia,2))+(math.pow(femur,2)*(math.pow(h,2)-math.pow(tibia,2))))))/math.pow(femur,2))
    l = math.sin(alpha1)*femur
    return h, l

def IK_berdiri_tengah():
    maju = 0
    h,l = nilai_h(panjang_depan_tengah, abs(roll))
    print("H tengah: ", str(h))
    sudut_base_coxa_tengah = math.degrees(math.atan(maju/(l+coxa)))
    P = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)) #panjang diagonal setelah kaki maju
    P = P-coxa
    M = math.sqrt(math.pow(h,2)+math.pow(P,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(M,2)-math.pow(tibia,2))/(2*femur*M)))
    sudut_coxa_femur_2_tengah = math.degrees(math.acos((math.pow(M,2)+math.pow(h,2)-math.pow(P,2))/(2*h*M)))
    sudut_coxa_femur_total = sudut_coxa_femur_1_tengah + sudut_coxa_femur_2_tengah
    sudut_femur_tibia_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(M,2))/(2*tibia*femur)))
    return (sudut_base_coxa_tengah, sudut_coxa_femur_total, sudut_femur_tibia_tengah)

def IK_berdiri_depan():
    maju = 0
    h,l = nilai_h(panjang_depan_belakang, -min(roll, 0))
    print("H depan: " + str(h))
    PD = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)-(2*maju*(l+coxa)*math.cos(math.radians(135))))
    sudut_base_coxa_depan = math.degrees(math.acos((math.pow((l+coxa),2)+math.pow(PD,2)-math.pow(maju,2))/(2*(l+coxa)*PD)))
    PD = PD-coxa
    MD = math.sqrt(math.pow(h,2)+math.pow(PD,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(MD,2)-math.pow(tibia,2))/(2*femur*MD)))
    sudut_coxa_femur_2_depan = math.degrees(math.acos((math.pow(MD,2)+math.pow(h,2)-math.pow(PD,2))/(2*h*MD)))
    sudut_coxa_femur_total_depan = sudut_coxa_femur_1_depan + sudut_coxa_femur_2_depan
    sudut_femur_tibia_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MD,2))/(2*tibia*femur)))
    return (sudut_base_coxa_depan, sudut_coxa_femur_total_depan, sudut_femur_tibia_depan)

def IK_berdiri_belakang():
    maju = 0
    h,l = nilai_h(panjang_depan_belakang, max(roll, 0))
    print("H belakang: " + str(h))
    PB = math.sqrt(math.pow(maju,2)+math.pow((l+coxa),2)-(2*maju*(l+coxa)*math.cos(math.radians(45))))
    sudut_base_coxa_belakang = math.degrees(math.acos((math.pow((l+coxa),2)+math.pow(PB,2)-math.pow(maju,2))/(2*(l+coxa)*PB)))
    PB = PB - coxa
    MB = math.sqrt(math.pow(h,2)+math.pow(PB,2)) #panjang garis miring antara femur tibia
    sudut_coxa_femur_1_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(MB,2)-math.pow(tibia,2))/(2*femur*MB)))
    sudut_coxa_femur_2_belakang = math.degrees(math.acos((math.pow(MB,2)+math.pow(h,2)-math.pow(PB,2))/(2*h*MB)))
    sudut_coxa_femur_total_belakang = sudut_coxa_femur_1_belakang + sudut_coxa_femur_2_belakang
    sudut_femur_tibia_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MB,2))/(2*tibia*femur)))
    return (sudut_base_coxa_belakang, sudut_coxa_femur_total_belakang, sudut_femur_tibia_belakang)

base_coxa_tengah_berdiri, coxa_femur_tengah_berdiri, femur_tibia_tengah_berdiri = IK_berdiri_tengah()
base_coxa_depan_berdiri, coxa_femur_depan_berdiri, femur_tibia_depan_berdiri = IK_berdiri_depan()
base_coxa_belakang_berdiri, coxa_femur_belakang_berdiri, femur_tibia_belakang_berdiri = IK_berdiri_belakang()

print("Tengah :" + str(base_coxa_tengah_berdiri) + ", " + str(coxa_femur_tengah_berdiri) + ", " + str(femur_tibia_tengah_berdiri))
print("Depan :" + str(base_coxa_depan_berdiri) + ", " + str(coxa_femur_depan_berdiri) + ", " + str(femur_tibia_depan_berdiri))
print("Belakang :" + str(base_coxa_belakang_berdiri) + ", " + str(coxa_femur_belakang_berdiri) + ", " + str(femur_tibia_belakang_berdiri))



kit1.servo[8].angle = 90 #coxa1
kit1.servo[7].angle = coxa_femur_depan_berdiri+35 #femur1
kit1.servo[6].angle = (180-femur_tibia_depan_berdiri)+45 #tibia1

kit2.servo[7].angle = 90 #coxa6
kit2.servo[8].angle = 180-(coxa_femur_depan_berdiri+35) #femur6
kit2.servo[9].angle = femur_tibia_depan_berdiri-45 #tibia6

kit1.servo[5].angle = 90 #coxa2
kit1.servo[4].angle = coxa_femur_tengah_berdiri+35 #femur2
kit1.servo[3].angle = (180-femur_tibia_tengah_berdiri)+45 #tibia2

kit2.servo[10].angle = 90 #coxa5
kit2.servo[11].angle = 180-(coxa_femur_tengah_berdiri+35) #femur5
kit2.servo[12].angle = femur_tibia_tengah_berdiri - 45 #tibia5

kit1.servo[2].angle = 90 #coxa3
kit1.servo[1].angle = coxa_femur_belakang_berdiri + 35 #femur3
kit1.servo[0].angle = (180-femur_tibia_belakang_berdiri) + 45 #tibia3

kit2.servo[13].angle = 90 #coxa4
kit2.servo[14].angle = 180-(coxa_femur_belakang_berdiri+35) #femur4
kit2.servo[15].angle = femur_tibia_belakang_berdiri - 45 #tibia4
