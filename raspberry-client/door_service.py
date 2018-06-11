#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# These pin numbers refer to the GPIO.BCM numbers.
RELAY = 5
CALL_LED_PIN     = 23    # LED to indicate call status

def setup():
  GPIO.setmode(GPIO.BCM) # set pin numbering mode using GPIO.setmode(GPIO.BCM)
  GPIO.setup(RELAY, GPIO.OUT)
  GPIO.output(RELAY, 0)
  GPIO.setup(CALL_LED_PIN, GPIO.OUT)
  GPIO.output(CALL_LED_PIN, 1)     # Keep this LED ON.


def pulse_relay(self, relay=RELAY, delay=1):
  setup()
  GPIO.output(relay, False)
  time.sleep(delay)
  GPIO.output(relay, True)

def flash_led(ledpin=CALL_LED_PIN, stay_on=False, delay=0.1, blink_count=10):
  setup()
  for j in range(0, blink_count):
    if ledpin:
      GPIO.output(ledpin, True)
      time.sleep(delay)
    if ledpin:
      GPIO.output(ledpin, False)
      time.sleep(delay)

  if stay_on and ledpin:
    GPIO.output(ledpin, True)