from flask import Flask,request
import requests
import socket
import time, threading
import random
app = Flask(__name__)

servers = []
server_ip = ""
@app.route('/infect/', methods=['POST','GET'])
def infect():
    global servers
    global server_ip
    server_ip = request.host
    if request.method == 'POST':
        servers += request.json["Servers"]
        servers = list(set(servers))
        for i in servers:
            print(i)
    return request.host

def sneeze():
    global servers
    global server_ip
    if len(servers) > 0:
        jsonServers = {"Servers":servers+[server_ip]}
        s = random.choice(servers)
        r = requests.post("http://"+s+"/infect/", json=jsonServers)
        r.status_code
    threading.Timer(10, sneeze).start()


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    sneeze()
    app.run(port=port)
