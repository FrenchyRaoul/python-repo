#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import pygame

pygame.init()

GPIO.setmode(GPIO.BOARD)

# This is for GPIO pin labeled 16 on Breakout
GPIO.setup(36, GPIO.OUT)
GPIO.setup(29, GPIO.IN)
a = 1
b = 0.025

while True:
	input = GPIO.input(29)
	if input == 0:
		b = 0.25
	if input == 1:
		b = 0.5
	time.sleep(b)
	a = not(a)
	GPIO.output(36, a)	

