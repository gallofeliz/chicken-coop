#!/usr/bin/env python

import socketserver, http.server, json, os, Adafruit_DHT
import RPi.GPIO as GPIO
import logging
port = 8080

GPIO.setmode(GPIO.BCM)

DHT_SENSOR = Adafruit_DHT.DHT22
TH1_PIN = int(os.environ['TH1_PIN'])
OC1_PIN = int(os.environ['OC1_PIN'])
OC2_PIN = int(os.environ['OC2_PIN'])
OC3_PIN = int(os.environ['OC3_PIN'])

GPIO.setup(TH1_PIN, GPIO.IN)
GPIO.setup(OC1_PIN, GPIO.IN)
GPIO.setup(OC2_PIN, GPIO.IN)
GPIO.setup(OC3_PIN, GPIO.IN)

def read_th(pin):
  humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, pin)

  if humidity is None or temperature is None:
    raise Exception('KO th pin ' + str(pin))

  return {
    'temperature': round(temperature, 1),
    'humidity': round(humidity)
  }

# True if detect magnetic
def read_oc(pin):
  value = GPIO.input(pin) == 0

  logging.info('OC pin ' + str(pin) + ' value ' + str(value))

  return value

def read():
    chickenDoorStatus = 'OPEN (PARTIAL)'

    try:
      inside = read_th(TH1_PIN)
    except Exception as inst:
      logging.exception('ERROR')
      inside = {}

    if read_oc(OC1_PIN):
      chickenDoorStatus = 'CLOSED'

    if read_oc(OC2_PIN):
      chickenDoorStatus = 'OPEN (TOTAL)'

    return {
      **inside,
      # Doors can be "CLOSED (LOCKED)", "CLOSED (UNLOCKED)", "CLOSED", "OPEN", "OPEN (PARTIAL)", "OPEN (TOTAL)"
      'humanDoorStatus': 'CLOSED' if read_oc(OC3_PIN) else 'OPEN',
      'chickenDoorStatus': chickenDoorStatus
    }

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/favicon.ico'):
            logging.info('Skipped')
            return

        try:
            data = read()
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(data), 'utf8'))
            logging.info('Done ' + str(data))
        except Exception as inst:
            self.send_response(500)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(str(inst), 'utf8'))
            logging.exception('ERROR')

httpd = socketserver.TCPServer(('', port), Handler)
try:
   logging.info('Listening on ' + str(port))
   httpd.serve_forever()
except KeyboardInterrupt:
   pass
httpd.server_close()
logging.info('Ended')
