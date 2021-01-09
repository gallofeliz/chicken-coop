#!/usr/bin/env python

import socketserver, http.server, json, os, Adafruit_DHT
import RPi.GPIO as GPIO
port = 8080

GPIO.setmode(GPIO.BCM)

DHT_SENSOR = Adafruit_DHT.DHT22
TH1_PIN = int(os.environ['TH1_PIN'])
TH2_PIN = int(os.environ['TH2_PIN'])
OC3_PIN = int(os.environ['OC3_PIN'])

GPIO.setup(TH1_PIN, GPIO.IN)
GPIO.setup(TH2_PIN, GPIO.IN)
GPIO.setup(OC3_PIN, GPIO.IN)

def read_th(pin):
  humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, pin)

  if humidity is None or temperature is None:
    raise Exception('KO')

  return {
    'temperature': round(temperature, 1),
    'humidity': round(humidity)
  }

# True if detect magnetic
def read_oc(pin):
  return GPIO.input(pin) == 0

def read():
    return {
      **read_th(TH1_PIN),
      'outside': read_th(TH2_PIN),
      'humanDoorStatus': 'CLOSED' if read_oc(OC3_PIN) else 'OPEN'
      #'chickenDoorStatus': 'CLOSED', 'OPEN (PARTIAL)', 'OPEN (TOTAL)'
    }

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/favicon.ico'):
            print('Skipped')
            return

        try:
            data = read()
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(data), 'utf8'))
            print('Done ' + str(data))
        except Exception as inst:
            self.send_response(500)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(str(inst), 'utf8'))
            print('ERROR ' + str(inst))

httpd = socketserver.TCPServer(('', port), Handler)
try:
   print('Listening on ' + str(port))
   httpd.serve_forever()
except KeyboardInterrupt:
   pass
httpd.server_close()
print('Ended')
