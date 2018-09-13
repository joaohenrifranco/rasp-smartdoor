import RPi.GPIO as GPIO
import time

# These pin numbers refer to the GPIO.BCM numbers.
RELAY_PIN = 5
LED_PIN = 23

def setup():
  GPIO.setmode(GPIO.BCM)            # Set pin numbering mode using GPIO.setmode(GPIO.BCM)
  GPIO.setup(RELAY_PIN, GPIO.OUT)
  GPIO.output(RELAY_PIN, 1)         # Keep door locked
  GPIO.setup(LED_PIN, GPIO.OUT)
  GPIO.output(LED_PIN, 1)           # Keep this LED ON.

def pulse_relay(relay_pin=RELAY_PIN, delay=2):
  setup()
  GPIO.output(relay_pin, False)
  time.sleep(delay)
  GPIO.output(relay_pin, True)

def flash_led(led_pin=LED_PIN, stay_on=False, delay=0.1, blink_count=10):
  setup()

  for j in range(0, blink_count):
    GPIO.output(led_pin, True)
    time.sleep(delay)
    GPIO.output(led_pin, False)
    time.sleep(delay)
  if stay_on:
    GPIO.output(led_pin, True)
  
  GPIO.cleanup(led_pin)

if __name__ == '__main__':
  setup()