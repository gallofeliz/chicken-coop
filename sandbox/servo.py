# Raspberry Pi + MG90S Servo PWM Control Python Code
#
#
import RPi.GPIO as GPIO
import time

time.sleep(1)

# setup the GPIO pin for the servo
servo_pin = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)

# setup PWM process
pwm = GPIO.PWM(servo_pin, 50) # 50 Hz (20 ms PWM period)
#pwm.start(7.6) # start PWM by rotating to 90 degrees
#    pwm.ChangeDutyCycle(ii) # rotate to 0 degrees
#time.sleep(0.3)
#pwm.ChangeDutyCycle(2.4)
#time.sleep(0.3)
#pwm.ChangeDutyCycle(12.4)
#time.sleep(0.3)


pwm.start(7.6)
time.sleep(0.3)

#steps = 5.0/50

#for i in range(0, 50):
#  pwm.ChangeDutyCycle(5.0 + steps*i)
#  time.sleep(0.1)

for i in range(0,20):
  pwm.ChangeDutyCycle(12.4)
  time.sleep(0.3)
  pwm.ChangeDutyCycle(2.4)
  time.sleep(0.3)





pwm.ChangeDutyCycle(0) # this prevents jitter
pwm.stop() # stops the pwm on 13
GPIO.cleanup() # good practice when finished using a pin
