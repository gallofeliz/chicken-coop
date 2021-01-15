import RPi.GPIO as GPIO
import time
import datetime
from RpiMotorLib import RpiMotorLib
    
GpioPins = [24,25,8,7]

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)


# Set Switch GPIO as input
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

zeroFound=False

def sensorCallback(channel):
    global zeroFound

    # Called if sensor output goes LOW
    if GPIO.input(16) == 1:
        zeroFound = True

GPIO.add_event_detect(16, GPIO.BOTH, callback=sensorCallback,  bouncetime=50)

pts=3850

def right(pt, speed = 'fast'):
  sp = 0.002

  if speed == 'slow':
    sp=0.01

  mymotortest.motor_run(GpioPins , sp, pt, True, False, "wave")
def left(pt):
  mymotortest.motor_run(GpioPins , .002, pt, False, False, "wave")

while zeroFound == False:
    right(8)
    time.sleep(0.01)

left(pts + 50)
right(pts)
left(pts)
right(pts)

# Reset GPIO settings
GPIO.cleanup()

