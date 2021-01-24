# Import required libraries
import RPi.GPIO as GPIO
import time
import datetime

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

print ("Setup GPIO pin as input")

# Set Switch GPIO as input
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def sensorCallback(channel):
# Called if sensor output goes LOW
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    print(GPIO.input(16))

def sensorCallback2(channel):
# Called if sensor output goes HIGH
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    print ("Sensor HIGH " + stamp)

# Wrap main content in a try block so we can
# catch the user pressing CTRL-C and run the
# GPIO cleanup function. This will also prevent
# the user seeing lots of unnecessary error
# messages.

print('hellllo')
GPIO.add_event_detect(16, GPIO.BOTH, callback=sensorCallback,  bouncetime=50)

try:
    # Loop until users quits with CTRL-C
    while True :
        time.sleep(0.1)

except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()
