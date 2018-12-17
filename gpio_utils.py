import RPi.GPIO as GPIO
import time

# These pin numbers refer to the GPIO.BCM numbers.
DOOR_PIN = 5              # (OUT) Relay that unlocks door
DOORBELL_PIN = 21         # (OUT)
LED_PIN = 13              # (OUT) LED for the CALL_BUTTON
CALL_BUTTON_PIN  = 19     # (IN) Button to trigger start outgoing call.
DOOR_BUTTON_PIN = 26      # (IN)

def setup():
  GPIO.setmode(GPIO.BCM)            # Set pin numbering mode using GPIO.setmode(GPIO.BCM)
  GPIO.setup(DOOR_PIN, GPIO.OUT)
  GPIO.output(DOOR_PIN, 1)          # Keep door locked
  GPIO.setup(DOORBELL_PIN, GPIO.OUT)
  GPIO.output(DOORBELL_PIN, 0)      # Keep doorbell low
  GPIO.setup(LED_PIN, GPIO.OUT)
  GPIO.output(LED_PIN, 1)           # Keep this LED ON.
  GPIO.setup(CALL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(DOOR_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def pulse_relay(pulse_pin=DOOR_PIN, delay=2, invert=False):
  setup()
  if (invert == False):
    GPIO.output(pulse_pin, False)
    time.sleep(delay)
    GPIO.output(pulse_pin, True)
  else:
    GPIO.output(pulse_pin, True)
    time.sleep(delay)
    GPIO.output(pulse_pin, False)

def flash_led(led_pin=LED_PIN, stay_on=False, delay=0.1, blink_count=10):
  setup()
  for j in range(0, blink_count):
    GPIO.output(led_pin, True)
    time.sleep(delay)
    GPIO.output(led_pin, False)
    time.sleep(delay)
  if stay_on:
    GPIO.output(led_pin, True)
  
if __name__ == '__main__':
  setup()
  pass
