# Code by Gabriel Milan https://github.com/gabriel-milan/
# Adapted from SimpleMFRC522 @ https://github.com/pimylifeup/MFRC522-python

import RPi.GPIO as GPIO
from MFRC522 import MFRC522
  
class ReaderMFRC522:
  
  def __init__(self):
    self.READER = MFRC522()
  
  def uid_to_hex (self, uid):
    output = ""
    for num in uid:
      output += hex(num)[2:]
    return output

  def read_no_block(self):
    (status, tagType) = self.READER.MFRC522_Request(self.READER.PICC_REQIDL)
    if status != self.READER.MI_OK:
        return None
    (status, uid) = self.READER.MFRC522_Anticoll()
    if status != self.READER.MI_OK:
        return None
    hex_id = self.uid_to_hex(uid)
    return hex_id
  
  def read_with_block(self):
    uid = None
    while (uid == None):
      uid = self.read_no_block()
    return uid