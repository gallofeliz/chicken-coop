FROM python@sha256:98493ebbff033eabdacaaea238c3f0ad6b46e284d2ba91ef419068d4a9ddaea2

RUN apk add --no-cache gcc musl-dev

RUN pip install Adafruit_DHT
RUN pip install RPi.GPIO

WORKDIR /app

ADD main.py

CMD ./main.py
