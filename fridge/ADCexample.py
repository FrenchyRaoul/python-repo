#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
import MySQLdb
import datetime
import dhtreader

db = MySQLdb.connect(host="192.168.1.138",
                     user="pi",
                     passwd="raspberry",
                     db="beer")
db.autocommit(True)
cur = db.cursor()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
DEBUG = 1

dhtreader.init()


# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)

    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)  # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3  # we only need to send 5 bits here
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout >>= 1  # first bit is 'null' so drop it
    return adcout


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
adcnum = 0;

relay = 1
targetTemp = 75

while True:

    tempDHT, humidity = dhtreader.read(22, 26)

    temp_adc = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)

    millivolts = temp_adc * (3300.0 / 1024.0)
    tempC = (millivolts - 500) / 10.0
    tempF = tempC * 2 + 30
    tempF2 = tempDHT * 2 + 30
    tempAve = float((tempF + tempF2) / 2)

    if (tempAve > targetTemp):
        relay = 1
    else:
        relay = 0

        # print "temp1 is", tempF, " temp2 is", tempF2, "humidity is", humidity, "%"
    print
    "Average Temp is", tempAve, "humidity is", humidity, "relay is", relay

    timenow = datetime.datetime.now()
    year = timenow.year
    month = timenow.month
    day = timenow.day
    hour = timenow.hour
    minute = timenow.minute
    second = timenow.second

    sql = "INSERT INTO temperature (year,month,day,hour,minute,second,temperature,temperature2, humidity) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
    year, month, day, hour, minute, second, tempF, tempF2, humidity)
    cur.execute(sql)

    time.sleep(2)
