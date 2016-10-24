#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
import MySQLdb
import datetime
import dhtreader
from movingaverage import movingaverage

# databaseConnect = raw_input('Steam to database? (yes or no)')
databaseConnect = 'no'

while databaseConnect!=('yes') and databaseConnect!=('no'):
	databaseConnect = raw_input('Incorrect Input. Stream to database? (yes or no)')

if databaseConnect=='yes':
	db = MySQLdb.connect(host="192.168.1.138",user="pi",passwd="raspberry",db="beer")
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
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
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
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout
 
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
RELAY = 12
 
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

GPIO.setup(RELAY, GPIO.OUT)
 
# 10k trim pot connected to adc #0
adcnum = 0;

relayEnable = 1
relayOffTime = datetime.datetime.now()
relayOnTime = datetime.datetime.now()
minOnTimeMinutes = 3
minOffTimeMinutes = 3
targetTemp = 50

print "Relay starting state:",relayEnable

if relayEnable == 1:
	GPIO.output(RELAY,0)
elif relayEnable ==0:
	GPIO.output(RELAY,1)

minOnTimeSeconds = minOnTimeMinutes * 60
minOffTimeSeconds = minOffTimeMinutes * 60
 
print "Entering Loop."
try:
	while True:
#		k=1
#		while k<10:
#			try:
#				print 'dht read start'
#				tempDHT, humidity = dhtreader.read(22, 26)
#				print 'dht read successful'
#				break
#			except TypeError:
#				k += 1        
#
		print "reading adc"
		temp_adc = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
		
		millivolts = temp_adc * ( 5010.0 / 1024.0)  
		tempC = (millivolts - 500) / 10.0
		tempF = tempC * 2 + 30
		#tempF2 = tempDHT * 2 + 30
		#itempAve = float((tempF+tempF2)/2)
		
		timenow = datetime.datetime.now()
		year = timenow.year
		month = timenow.month
		day = timenow.day
		hour = timenow.hour
		minute = timenow.minute
		second = timenow.second

		
		if relayEnable==0:
			currentOffTime = timenow - relayOffTime
			currentOffTimeSeconds = currentOffTime.total_seconds()
			if (currentOffTimeSeconds>minOffTimeSeconds) and (tempF>targetTemp):
				relayEnable = 1
				relayOnTime = timenow
				GPIO.output(RELAY,0)
				print "Relay has switched on."
			print "The relay has been off for", currentOffTimeSeconds," seconds."
		elif relayEnable==1:
			currentOnTime = timenow - relayOnTime
			currentOnTimeSeconds = currentOnTime.total_seconds()
			if (currentOnTimeSeconds>minOnTimeSeconds) and (tempF<targetTemp):
				relayEnable = 0
				relayOffTime = timenow
				GPIO.output(RELAY,1)
				print "Relay has switched off." 
			print "The relay has been on for", currentOnTimeSeconds,"seconds."		
		#print "temp_adc: ", temp_adc
		#print "millivolts: ", millivolts
		#print "tempC: ", tempC
		#print "tempF: ", tempF
		#print "temp1 is", tempF, " temp2 is", tempF2
		print "Average Temp is", tempF 
		print "-------------------------------"

		
		if databaseConnect=='yes':
			sql = "INSERT INTO temperature (year,month,day,hour,minute,second,temperature,temperature2, humidity) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (year,month,day,hour,minute,second,tempF,tempF2,humidity)
			cur.execute(sql)

		time.sleep(2)
except Exception as e:
	print e
	print "Attempting to turn of fridge."
	try:
		GPIO.output(RELAY,1)
		print "Relay disengage signal sent. Program terminating"
	except:
		print "Failed to disengage relay. Program terminating"
