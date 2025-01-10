import math

coxa = 2.5052
femur = 7 #+2.8
tibia = 8
h1 = 6.7 #tinggi dari joint coxa-femur ke tanah pada saat masih pake python
l = 6.88
#kalo pengen tibianya tegak lurus kebawah, sudut femur-tibia sama sudut coxa-femur harusnya sama. Semakin besar sudut coxa-femurnya
#badannya bakal jadi lebih tinggi


#Mau sepanjang atau selebar apa kakinya itu nanti hasilnya bakal keliatan setinggi apa badannya (masukin panjang, outputnya tinggi)
alpha1 = math.asin(l/femur)
print("Sudut: " + str(math.degrees(alpha1)) + " derajat")
h = math.sqrt(math.pow(femur,2)+math.pow(tibia,2)-(2*femur*tibia*math.cos(alpha1))-(math.sin(alpha1)*math.sin(alpha1)*femur*femur))
print("Tinggi Lantai ke Base : " + str(h) + " cm")
print("")

#----------------------------------------------#
maju = 3 #cm

#IK kaki tengah (kiri)

sudut_base_coxa_tengah = math.degrees(math.atan(maju/l))
print("Besar Sudut Base Coxa : " + str(sudut_base_coxa_tengah) + " derajat")

P = math.sqrt(math.pow(maju,2)+math.pow(l,2)) #panjang diagonal setelah kaki maju
print("Panjang Diagonal Maju : " + str(P) + " cm")

M = math.sqrt(math.pow(h,2)+math.pow(P,2)) #panjang garis miring antara femur tibia
print("Panjang Garis Miring Antar Femur Tibia : " + str(M) + " cm")

sudut_coxa_femur_1_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(M,2)-math.pow(tibia,2))/(2*femur*M)))
print("Besar Sudut Coxa Femur 1: " + str(sudut_coxa_femur_1_tengah) + " derajat")

sudut_coxa_femur_2_tengah = math.degrees(math.acos((math.pow(M,2)+math.pow(h,2)-math.pow(P,2))/(2*h*M)))
print("Besar Sudut Coxa Femur 2: " + str(sudut_coxa_femur_2_tengah) + " derajat")

sudut_coxa_femur_total = sudut_coxa_femur_1_tengah + sudut_coxa_femur_2_tengah
print("Besar Sudut Coxa Femur Total : " + str(sudut_coxa_femur_total) + " derajat")

sudut_femur_tibia_tengah = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(M,2))/(2*tibia*femur)))
print("Besar Sudut Femur Tibia : " + str(sudut_femur_tibia_tengah) + " derajat")
print("")
#----------------------------------------#
#IK kaki depan (kiri)
PD = math.sqrt(math.pow(maju,2)+math.pow(l,2)-(2*maju*l*math.cos(math.radians(135))))
print("Panjang Garis Miring Maju : " + str(PD) + " cm")
sudut_base_coxa_depan = math.degrees(math.acos((math.pow(l,2)+math.pow(PD,2)-math.pow(maju,2))/(2*l*PD)))
print("Besar Sudut Base Coxa : " + str(sudut_base_coxa_depan) + " derajat")

MD = math.sqrt(math.pow(h,2)+math.pow(PD,2)) #panjang garis miring antara femur tibia
print("Panjang Garis Miring Antar Femur Tibia : " + str(MD) + " cm")

sudut_coxa_femur_1_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(MD,2)-math.pow(tibia,2))/(2*femur*MD)))
print("Besar Sudut Coxa Femur 1: " + str(sudut_coxa_femur_1_depan) + " derajat")

sudut_coxa_femur_2_depan = math.degrees(math.acos((math.pow(MD,2)+math.pow(h,2)-math.pow(PD,2))/(2*h*MD)))
print("Besar Sudut Coxa Femur 2: " + str(sudut_coxa_femur_2_depan) + " derajat")

sudut_coxa_femur_total = sudut_coxa_femur_1_depan + sudut_coxa_femur_2_depan
print("Besar Sudut Coxa Femur Total : " + str(sudut_coxa_femur_total) + " derajat")

sudut_femur_tibia_depan = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MD,2))/(2*tibia*femur)))
print("Besar Sudut Femur Tibia : " + str(sudut_femur_tibia_depan) + " derajat")
print("")

#----------------------------------#
#IK kaki belakang (kiri)
sudut_base_coxa_belakang = math.degrees(math.asin(maju/l))
print("Besar Sudut Base Coxa : " + str(sudut_base_coxa_belakang) + " derajat")

PB = math.sqrt(math.pow(l,2)-math.pow(maju,2)) #panjang diagonal setelah kaki maju
print("Panjang Diagonal Maju : " + str(PB) + " cm")

MB = math.sqrt(math.pow(h,2)+math.pow(PB,2)) #panjang garis miring antara femur tibia
print("Panjang Garis Miring Antar Femur Tibia : " + str(MB) + " cm")

sudut_coxa_femur_1_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(MB,2)-math.pow(tibia,2))/(2*femur*M)))
print("Besar Sudut Coxa Femur 1: " + str(sudut_coxa_femur_1_belakang) + " derajat")

sudut_coxa_femur_2_belakang = math.degrees(math.acos((math.pow(MB,2)+math.pow(h,2)-math.pow(PB,2))/(2*h*MB)))
print("Besar Sudut Coxa Femur 2: " + str(sudut_coxa_femur_2_belakang) + " derajat")

sudut_coxa_femur_total_belakang = sudut_coxa_femur_1_belakang + sudut_coxa_femur_2_belakang
print("Besar Sudut Coxa Femur Total : " + str(sudut_coxa_femur_total_belakang) + " derajat")

sudut_femur_tibia_belakang = math.degrees(math.acos((math.pow(femur,2)+math.pow(tibia,2)-math.pow(MB,2))/(2*tibia*femur)))
print("Besar Sudut Femur Tibia : " + str(sudut_femur_tibia_belakang) + " derajat")
print("")