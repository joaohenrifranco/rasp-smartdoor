#!/usr/bin/env python

import requests

host = '192.168.88.41'
port = '8000'

def request_unlock(uid, server_ip=host, api_path='/api/request-unlock', port=port):
  r = requests.post('http://' + server_ip + ':' + port + api_path, json={"uid": uid, "roomID": "principal", "readerPosition": 0},)
  print(r.json())
  return r.json().status

def send_log(sip, server_ip=host, api_path='/api/request-front-door-unlock', port=port):
  r = requests.post('http://' + server_ip + ':' + port + api_path, json={"sip": sip})
  return r.json().status