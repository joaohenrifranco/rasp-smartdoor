#!/usr/bin/env python
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
                    uid = line = re.sub('[[, ]]', '', str(uid_list))
                    print("UID: " + uid)
                    status = request_unlock(uid)
                    if status == 0:
                        pulse_relay()
    except:
        rdr.cleanup()

if __name__== "__main__":
    main()