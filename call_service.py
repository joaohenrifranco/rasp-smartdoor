#!/usr/bin/env python

import os
import linphone
import logging
import signal
import time
import RPi.GPIO as GPIO
import io
import time
from gpio_utils import flash_led, pulse_relay, setup, CALL_BUTTON_PIN, DOORBELL_PIN, DOOR_BUTTON_PIN, DOOR_PIN

# Asterisk SIP credentials
USERNAME = '201'
PASSWORD = 'porta201'

# WAITSECONDS controls the amount of time calling from doorbell.
WAITSECONDS = 60

# Asterisk Host
host = '192.168.88.159'

# doorbellToAddress is the SIP (or URL) address that will be called when the 'doorbell' is pressed.
doorbellToAddress = 'sip:111@' + host  # Who to 'ring'. SIP address format

# Sound for local 'doorbell ring'. Person pushing button hears this.
doorBellSoundWav = '../sounds/doorbell-1.wav' 

class SecurityCamera:
  def __init__(self, username='', password='', whitelist=[], camera='', snd_capture='', snd_playback=''):
    self.quit = False
    setup()

    self.whitelist = whitelist
    callbacks = {
      'call_state_changed': self.call_state_changed,
      'dtmf_received': self.dtmf_received, 
    }

    # Configure the linphone core
    logging.basicConfig(level=logging.INFO)
    signal.signal(signal.SIGINT, self.signal_handler)
    linphone.set_log_handler(self.log_handler)
    self.core = linphone.Core.new(callbacks, None, None)
    self.core.max_calls = 1
    self.core.echo_cancellation_enabled = True
    self.core.video_capture_enabled = True
    self.core.video_display_enabled = False
    self.core.stun_server = host
    self.core.firewall_policy = linphone.FirewallPolicy.PolicyUseIce
    if len(camera):
      self.core.video_device = camera

    if len(snd_capture):
      self.core.capture_device = snd_capture
    if len(snd_playback):
      self.core.playback_device = snd_playback

    # Only enable PCMU and PCMA audio codecs
    for codec in self.core.audio_codecs:
      if codec.mime_type == 'PCMA' or codec.mime_type == 'PCMU':
        self.core.enable_payload_type(codec, True)
      else:
        self.core.enable_payload_type(codec, False)

    # Only enable VP8 video codec
    for codec in self.core.video_codecs:
      if codec.mime_type == 'VP8':
        self.core.enable_payload_type(codec, True)
      else:
        self.core.enable_payload_type(codec, False)

    self.configure_sip_account(username, password)

  def signal_handler(self, signal, frame):
    self.core.terminate_all_calls()
    self.quit = True

  def log_handler(self, level, msg):
    method = getattr(logging, level)
    method(msg)

  def call_state_changed(self, core, call, state, message):
    if state == linphone.CallState.IncomingReceived:
      params = core.create_call_params(call)
      core.accept_call_with_params(call, params)

  def configure_sip_account(self, username, password):
    # Configure the SIP account
    proxy_cfg = self.core.create_proxy_config()
    proxy_cfg.identity_address = self.core.create_address(('sip:{username}@'+host).format(username=username))
    proxy_cfg.server_addr = 'sip:'+host+';transport=udp'
    proxy_cfg.register_enabled = True
    self.core.add_proxy_config(proxy_cfg)
    auth_info = self.core.create_auth_info(username, None, password, None, None, host)
    self.core.add_auth_info(auth_info)

  def dtmf_received(self, core, call, digits):
    logging.debug('on_dtmf_digit (%s)', str(digits))
    print("#\n" * 10)
    print("OPEN DOOR!")
    print("#\n" * 10)
    os.system('aplay /home/pi/sounds/OPEN_DOOR.wav')
    pulse_relay()

  def run(self):
    while not self.quit:
      # Check the push buttons
      button_call_pressed = False
      button_select_pressed = False     
      button_door_pressed = False
 
      if 0 != CALL_BUTTON_PIN:
        button_call_pressed = not GPIO.input(CALL_BUTTON_PIN)

      if 0 != DOOR_BUTTON_PIN:
        button_door_pressed = not GPIO.input(DOOR_BUTTON_PIN)

      if button_door_pressed:
        os.system('aplay /home/pi/sounds/OPEN_DOOR.wav')
        pulse_relay()

      if button_call_pressed and self.core.current_call is None:
        pulse_relay(DOORBELL_PIN, delay=0.2, invert = True)
        # We do not check the time here. They can keep 'ringing' the doorbell if they want
        # but it won't matter once a call is initiated.
        print('Call button pressed!')

        try:
          params = self.core.create_call_params(None)
          params.audio_enabled = True
          params.video_enabled = True
          params.audio_multicast_enabled = False  # Set these = True if you want multiple
          params.video_multicast_enabled = False  # people to connect at once.
          address = linphone.Address.new(doorbellToAddress)
          self.core.play_local(doorBellSoundWav)
          self.current_call = self.core.invite_address_with_params(address, params)
          flash_led(delay=0.2, stay_on=True)
          
          if None is self.current_call:
            logging.error('Error creating call and inviting with params... outgoing call aborted.')

        except KeyboardInterrupt:
          self.quit = True
          break
      
      # Iterate
      self.core.iterate()
      time.sleep(0.03)

def main():
  door = SecurityCamera(username=USERNAME, password=PASSWORD, whitelist=[('sip:210@'+host)], camera='Webcam V4L2: /dev/video0', snd_capture='ALSA: USB camera', snd_playback='ALSA: default device')
  door.run()

if __name__ == '__main__':
  main()
