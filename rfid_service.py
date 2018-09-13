#!/usr/bin/env python

import RPi.GPIO as GPIO
from gpio_utils import flash_led, pulse_relay
from api_utils import request_unlock
from ReaderMFRC522 import ReaderMFRC522
import re
import time

def main():

    try:
        reader = ReaderMFRC522()
        while True:
            uid = reader.read_with_block()[:-2] # Have to discard two last digits for this implementation purpose
            print (uid)
            status = request_unlock(uid)
            print (status)
            if (status == 0):
                print ("Authorized")
                pulse_relay()
            else:
                print ("Auth error")
    except:
        print ("RFID error")

if __name__ == '__main__':
    main()