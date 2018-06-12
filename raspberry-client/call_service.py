#!/usr/bin/env python
import linphone
import logging
import signal
import time
import RPi.GPIO as GPIO
import io
import time
from gpio_utils import flash_led, pulse_relay
from api_utils import send_log

# Asterisk SIP credentials
USERNAME = '201'
PASSWORD = 'porta'

# These pin numbers refer to the GPIO.BCM numbers.
CALL_BUTTON_PIN  = 18    # Button to trigger start outgoing call.

# WAITSECONDS controls the amount of time calling from doorbell.
WAITSECONDS = 60

# Asterisk Host
host = '192.168.88.41'

# doorbellToAddress is the SIP (or URL) address that will be called when the 'doorbell' is pressed.
doorbellToAddress = 'sip:666@' + host  # Who to 'ring'. SIP address format

# Sound for local 'doorbell ring'. Person pushing button hears this.
# doorBellSoundWav = './sounds/doorbell-1.wav' 

class SecurityCamera:
  def __init__(self, username='', password='', whitelist=[], camera='', snd_capture='', snd_playback=''):
    self.quit = False
    GPIO.setmode(GPIO.BCM) # set pin numbering mode using GPIO.setmode(GPIO.BCM)
    GPIO.setup(CALL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    self.whitelist = whitelist
    callbacks = {
      'call_state_changed': self.call_state_changed,
      'dtmf_received': self.dtmf_received, 
    }

    # Configure the linphone core
    #logging.basicConfig(level=logging.INFO)
    signal.signal(signal.SIGINT, self.signal_handler)
    linphone.set_log_handler(self.log_handler)
    self.core = linphone.Core.new(callbacks, None, None)
    self.core.max_calls = 1
    self.core.echo_cancellation_enabled = False
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
      if call.remote_address.as_string_uri_only() in self.whitelist:
        params = core.create_call_params(call)
        core.accept_call_with_params(call, params)
      else:
        core.decline_call(call, linphone.Reason.Declined)
        chat_room = core.get_chat_room_from_uri(self.whitelist[0])
        msg = chat_room.create_message(call.remote_address_as_string + ' tried to call')
        chat_room.send_chat_message(msg)

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
    digits = chr(digits)
  
  def run(self):
    while not self.quit:
      # Check the push buttons
      button_call_pressed = False
      button_select_pressed = False
      
      if 0 != CALL_BUTTON_PIN:
        button_call_pressed = not GPIO.input(CALL_BUTTON_PIN)

      if button_call_pressed and self.core.current_call is None:
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
          
          self.current_call = self.core.invite_address_with_params(address, params)
          flash_led(stay_on=True)
          
          if None is self.current_call:
            logging.error('Error creating call and inviting with params... outgoing call aborted.')

        except KeyboardInterrupt:
          self.quit = True
          break
      
      # Iterate
      self.core.iterate()
      time.sleep(0.03)

def main():
  door = SecurityCamera(username=USERNAME, password=PASSWORD, whitelist=[('sip:210@'+host)], camera='Webcam V4L2: /dev/video0', snd_capture='ALSA: USB2.0 PC CAMERA', snd_playback='ALSA: VM-5')
  door.run()

if __name__== '__main__':
  main()