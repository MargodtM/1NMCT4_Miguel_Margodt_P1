import RPi.GPIO as GPIO
import time
import picamera
from gpiozero import MotionSensor
from time import gmtime, strftime

from DbClass import DbClass

GPIO.setmode(GPIO.BCM)

knop1 = 12
knop2 = 16
knop3 = 20
knop4 = 21

ledGROEN = 18
ledGEEL = 23
ledROOD = 24

GPIO.setup(knop1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(knop2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(knop3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(knop4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(ledGROEN, GPIO.OUT)
GPIO.setup(ledGEEL, GPIO.OUT)
GPIO.setup(ledROOD, GPIO.OUT)

input_state1 = GPIO.input(knop1)
input_state2 = GPIO.input(knop2)
input_state3 = GPIO.input(knop3)
input_state4 = GPIO.input(knop4)

correct=[1,1,4,3]
list=[]

cameraState = "on"
GPIO.output(ledGROEN, GPIO.HIGH)
GPIO.output(ledROOD, GPIO.LOW)
GPIO.output(ledGEEL, GPIO.LOW)

camera = picamera.PiCamera()
pir = MotionSensor(4)

aantal = 4
while True:
    input_state1 = GPIO.input(knop1)
    if input_state1 == False:
        print("Sequence started")
        GPIO.output(ledGEEL, GPIO.HIGH)
        time.sleep(1)
        for i in range(4):
            while True:
                input_state1 = GPIO.input(knop1)
                input_state2 = GPIO.input(knop2)
                input_state3 = GPIO.input(knop3)
                input_state4 = GPIO.input(knop4)

                if (input_state1 == False):
                    GPIO.output(ledGEEL, GPIO.LOW)
                    list.append(1)
                    print("knop 1 gedrukt")
                    break
                if (input_state2 == False):
                    GPIO.output(ledGEEL, GPIO.LOW)
                    list.append(2)
                    print("knop 2 gedrukt")
                    break
                if (input_state3 == False):
                    GPIO.output(ledGEEL, GPIO.LOW)
                    list.append(3)
                    print("knop 3 gedrukt")
                    break
                if (input_state4 == False):
                    GPIO.output(ledGEEL, GPIO.LOW)
                    print("knop 4 gedrukt")
                    list.append(4)
                    break
                time.sleep(0.1)
                print("waiting for button")
                GPIO.output(ledGEEL,GPIO.HIGH)
            time.sleep(0.5)
        print(list)
        if list[0] == correct[0] and list[1] == correct[1] and list[2] == correct[2] and list[3] == correct[3]:
            print("CORRECT ayyy")
            if (cameraState == "on"):
                cameraState = "off"
                GPIO.output(ledROOD, GPIO.HIGH)
                GPIO.output(ledGEEL, GPIO.LOW)
                GPIO.output(ledGROEN, GPIO.LOW)
            else:
                cameraState = "on"
                GPIO.output(ledROOD, GPIO.LOW)
                GPIO.output(ledGEEL, GPIO.LOW)
                GPIO.output(ledGROEN, GPIO.HIGH)
            del list[3]
            del list[2]
            del list[1]
            del list[0]
            continue
        else:
            print("FOOUT AYY")
            del list[3]
            del list[2]
            del list[1]
            del list[0]
            continue

    if cameraState == "on":
        if pir.motion_detected:
            datetime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            name= strftime("%Y%m%d%H%M%S.jpg", gmtime())
            camid="1"
            camera.capture('/home/pi/Project/static/images/' + name)
            Db_layer = DbClass()
            Db_layer.takePicture(name,datetime,camid)
            i = 0
            for i in range(20):
                time.sleep(1)
                input_state1 = GPIO.input(knop1)
                if input_state1 == False:
                    break
        continue
    else:
        continue