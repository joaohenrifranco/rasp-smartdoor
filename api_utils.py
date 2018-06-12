import requests

HOST = '192.168.88.41'
PORT = '8000'

def request_unlock(uid, server_ip=HOST, api_path='/api/request-unlock', port=PORT):
  r = requests.post(
    'http://' + server_ip + ':' + port + api_path,
    json={'uid': uid, 'roomID': 'principal', 'readerPosition': 0}
    )
  return r.json()['status']

def send_log(sip, server_ip=HOST, api_path='/api/request-front-door-unlock', port=PORT):
  r = requests.post('http://' + server_ip + ':' + port + api_path, json={'sip': sip})
  return r.json()['status']