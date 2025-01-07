#gait kaki seribu

from time import sleep
from adafruit_servokit import ServoKit

waktu_sleep = 2

kit1 = ServoKit(channels = 16, address = 0x41)
kit2 = ServoKit(channels = 16, address = 0x40)

kit1.servo[2].angle = 70 #coxa3
kit1.servo[4].angle = 120 #femur2
kit1.servo[1].angle = 80 #femur3
kit2.servo[14].angle = 100 #femur4
kit2.servo[11].angle = 65 #femur5

kit2.servo[13].angle = 110 #coxa4
kit1.servo[3].angle = 125 #tibia2
kit1.servo[0].angle = 90 #tibia3
kit2.servo[15].angle = 95 #tibia4
kit2.servo[12].angle = 55 #tibia5

sleep(5)

kit1.servo[8].angle =  120 #coxa1
kit2.servo[7].angle =  60 #coxa6

kit1.servo[5].angle = 120 #coxa2
kit2.servo[10].angle =  60 #coxa5

kit1.servo[2].angle = 100 #coxa3
kit2.servo[13].angle = 80 #coxa4
print("Mundur")
sleep(waktu_sleep)


#femur 1 angkat
kit1.servo[7].angle = 180 #femur1
kit1.servo[6].angle = 180 #tibia1
print("Femur 1 Ngangkat")
sleep(waktu_sleep)

try:
    while True:
        #coxa 1 maju sisanya mundur 5 derajat
        kit1.servo[8].angle = 120 #coxa1
        kit2.servo[7].angle = 65 #coxa6

        kit1.servo[5].angle = 115 #coxa2
        kit2.servo[10].angle = 65 #coxa5

        kit1.servo[2].angle = 95 #coxa3
        kit2.servo[13].angle = 85 #coxa4
        print("Coxa 1 Maju 30 Derajat dari posisi berdiri, sisanya mundur 5 Derajat")
        sleep(waktu_sleep)


        #femur 1 turun dan tibia turun sekalian adjust ngambil kaki
        for i in range (10, 50, 10):
            kit1.servo[7].angle = 180 - i #femur1
            kit1.servo[6].angle = 180 - (i-10) #tibia1
        print("Femur Tibia 1 Turun")
        sleep(waktu_sleep)

        #femur 2 angkat
        kit1.servo[4].angle = 180 #femur2
        kit1.servo[3].angle = 180 #tibia2
	print("Femur Tibia 2 Angkat")
	sleep(waktu_sleep)

        #coxa 2 maju sisanya mundur 5 derajat
        kit1.servo[8].angle = 115 #coxa1
        kit2.servo[7].angle = 70 #coxa6

        kit1.servo[5].angle = 120 #coxa2
        kit2.servo[10].angle = 70 #coxa5

        kit1.servo[2].angle = 90 #coxa3
        kit2.servo[13].angle = 90 #coxa4
        print("Coxa 2 Maju 30 Derajat dari posisi berdiri, sisanya mundur 5 Derajat")
        sleep(waktu_sleep)

	#femur tibia 2 turun
        for i in range (10, 50, 10):
            kit1.servo[4].angle = 160 - (i) #femur2
            kit1.servo[3].angle = 160 - (i-5) #tibia2
	print("Femur 2 Turun")
	sleep(waktu_sleep)

        #femur tibia 3 naik
        kit1.servo[1].angle = 120 #femur3
        kit1.servo[0].angle = 120 #tibia3

 	#coxa 3 maju sisanya mundur 5 derajat
        kit1.servo[8].angle = 110 #coxa1
        kit2.servo[7].angle = 75 #coxa6

        kit1.servo[5].angle = 115 #coxa2
        kit2.servo[10].angle = 75 #coxa5

        kit1.servo[2].angle = 100 #coxa3
        kit2.servo[13].angle = 95 #coxa4
        print("Coxa 3 Maju 30 Derajat dari posisi berdiri, sisanya mundur 5 Derajat")
        sleep(waktu_sleep)

	#femur tibia 3 turun
	for i in range (10, 50, 10):
            kit1.servo[1].angle = 120 - i #femur3
            kit1.servo[0].angle = 120 - (i-10) #tibia3
	print("Femur Tibia 3 Turun")
	sleep(waktu_sleep)

	#femur 4 angkat
        kit2.servo[14].angle = 60 #femur4
        kit2.servo[15].angle = 60 #tibia4
        print("Femur 4 Ngangkat")
        sleep(waktu_sleep)

	#coxa 4 maju sisanya mundur 5 derajat
        kit1.servo[8].angle = 105 #coxa1
        kit2.servo[7].angle = 80 #coxa6

        kit1.servo[5].angle = 110 #coxa2
        kit2.servo[10].angle = 80 #coxa5

        kit1.servo[2].angle = 95 #coxa3
        kit2.servo[13].angle = 80 #coxa4
        print("Coxa 4 Maju 30 Derajat dari posisi berdiri, sisanya mundur 5 Derajat")
        sleep(waktu_sleep)
	    
	#femur tibia 4 turun
	for i in range (10, 50, 10):
            kit2.servo[14].angle = 60 + i #femur4
            kit2.servo[15].angle = 60 + (i-5) #tibia4
        print("Femur Tibia 4 Turun")
        sleep(waktu_sleep)

	#femur 5 angkat
	kit2.servo[11].angle = 0 #femur5
	kit2.servo[12].angle = 0 #tibia5
	print("Femur 5 Ngangkat")
	sleep(waktu_sleep)

	#coxa 5 maju sisanya mundur 5 derajat
        kit1.servo[8].angle = 100 #coxa1
        kit2.servo[7].angle = 85 #coxa6

        kit1.servo[5].angle = 105 #coxa2
        kit2.servo[10].angle = 60 #coxa5

        kit1.servo[2].angle = 90 #coxa3
        kit2.servo[13].angle = 85 #coxa4
        print("Coxa 5 Maju 30 Derajat dari posisi berdiri, sisanya mundur 5 Derajat")
        sleep(waktu_sleep)
	    
	#femur tibia 5 turun
	for i in range (10, 50, 10):
            kit2.servo[11].angle = 20 + (i+5) #femur5
            kit2.servo[12].angle = 20 + (i-5) #tibia5
	print("Femur Tibia 5 Turun")
	sleep(waktu_sleep)

	#femur 6 angkat
        kit2.servo[8].angle = 0 #femur6
        kit2.servo[9].angle = 0 #tibia6
        print("Femur 6 Ngangkat")
        sleep(waktu_sleep)

	#coxa 6 maju sisanya mundur 5 derajat
        kit1.servo[8].angle = 95 #coxa1
        kit2.servo[7].angle = 60 #coxa6

        kit1.servo[5].angle = 100 #coxa2
        kit2.servo[10].angle = 65 #coxa5

        kit1.servo[2].angle = 85 #coxa3
        kit2.servo[13].angle = 90 #coxa4
        print("Coxa 6 Maju 30 Derajat dari posisi berdiri, sisanya mundur 5 Derajat")
        sleep(waktu_sleep)
	    
	#femur tibia 6 turun
	for i in range (10, 50, 10):
            kit2.servo[8].angle = 0 + i #femur6
            kit2.servo[9].angle = 0 + (i-10) #tibia6
        print("Femur Tibia 6 Turun")
        sleep(waktu_sleep)
	    
	#femur 1 angkat
	kit1.servo[7].angle = 180 #femur1
	kit1.servo[6].angle = 180 #tibia1
	print("Femur 1 Ngangkat")
	sleep(waktu_sleep)

except KeyboardInterrupt:
	kit1.servo[8].angle = 90 #coxa1
	kit1.servo[7].angle = 140 #femur1
	kit1.servo[6].angle = 150 #tibia1

	kit2.servo[7].angle = 90 #coxa6
	kit2.servo[8].angle = 40  #femur6
	kit2.servo[9].angle = 30 #tibia6

	kit1.servo[5].angle = 90 #coxa2
	kit1.servo[4].angle = 140 #femur2
	kit1.servo[3].angle = 145 #tibia2

	kit2.servo[10].angle = 90 #coxa5
	kit2.servo[11].angle = 45 #femur5
	kit2.servo[12].angle = 35 #tibia5

	kit1.servo[2].angle = 90 #coxa3
	kit1.servo[1].angle = 140 #femur3
	kit1.servo[0].angle = 150 #tibia3

	kit2.servo[13].angle = 90 #coxa4
	kit2.servo[14].angle = 40 #femur4
	kit2.servo[15].angle = 35 #tibia4




