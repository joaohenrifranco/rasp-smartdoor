#!/usr/bin/env python
import RPi.GPIO as GPIO
from gpio_utils import flash_led, pulse_relay
from api_utils import request_unlock
from pirc522 import RFID
import re

rdr = RFID()

def main():
    try:
        while True:
            rdr.wait_for_tag()
            (error, tag_type) = rdr.request()
            if not error:
                print("Tag detected")
                (error, uid_list) = rdr.anticoll()
                if not error:
                    uid = ''
                    for element in uid_list:
                        uid += str(hex(element)[2:])
                    print("UID: " + uid)
                    status = request_unlock(uid)
                    if status == 0:
                        pulse_relay()
                        delay(1000)
    except:
        rdr.cleanup()

if __name__== "__main__":
    main()