import requests

HOST = '192.168.88.41'
PORT = '80'

def request_unlock(uid, server_ip=HOST, api_path='/api/request-unlock', port=PORT):
  r = requests.post(
    'http://' + server_ip + ':' + port + api_path,
    json={'uid': uid, 'roomID': 'PRINCIPAL', 'readerPosition': 0}
    )
  return r.json()['status']
