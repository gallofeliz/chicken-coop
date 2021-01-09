import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib
    
GpioPins = [24,25,8,7]

# Declare an named instance of class pass a name and motor type
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")

# call the function pass the parameters
# Example: To run A stepper motor connected to GPIO pins 18, 23, 24, 25 (18-IN1 23-IN2 24-IN3, 25-IN4) for step delay of .01 second for 100 step control signal sequence, in clockwise direction, verbose output off , in half step mode, with an init start delay of 50mS

pts=3750

def right(pt):
  mymotortest.motor_run(GpioPins , .002, pt, True, False, "wave", .05)
def left(pt):
  mymotortest.motor_run(GpioPins , .002, pt, False, False, "wave", .05)

left(pts/2)
#right(16)
#left(pts/2)

#print('wave')
#mymotortest.motor_run(GpioPins , .005, 512/2, False, False, "wave", .05)
#mymotortest.motor_run(GpioPins , .005, 512/2, True, False, "wave", .05)
#print('half')
#mymotortest.motor_run(GpioPins , .005, 512/2, False, False, "half", .05)
#print('full')
#mymotortest.motor_run(GpioPins , .005, 512/2, False, False, "full", .05)

# good practise to cleanup GPIO at some point before exit
GPIO.cleanup()
