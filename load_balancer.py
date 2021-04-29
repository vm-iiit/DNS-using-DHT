from flask import Flask
from random import randint
import requests
from flask import request
import threading
import time

successful_response = {'job':True}
url_prefix = "http://127.0.0.1:"

dns_ip_address = "127.0.0.1"
dns_port = "9090"

app = Flask(__name__)

servers = []

@app.route('/', methods = ['GET', 'POST'])
def client_query():

    data = eval(request.data.decode("utf-8"))
    index = randint(0,len(servers)-1)
    response = requests.post(url_prefix + servers[index]+'/query', json = data)

    return response.json()

@app.route('/get_ip', methods = ['GET', 'POST'])
def get_ip_of_member_node():

    index = randint(0,len(servers)-1)
    response = requests.get(url_prefix + servers[index]+'/get_ip')
    return response.json()['val']

@app.route("/add_node", methods = ['GET', 'POST'])
def add_server():

    port_number = eval(request.data.decode("utf-8"))['val']
    servers.append(port_number)
    return successful_response

def check_heartbeat(index):

    try:
        response = requests.get(url_prefix + servers[index]+'/check_heartbeat')
    except:
        del servers[index]
    
if __name__ == "__main__":

    threading.Thread(target = app.run, kwargs={"host":dns_ip_address, "port":dns_port, "debug":False}).start()

    index = 0
    while True:

        time.sleep(1)
        if len(servers):
            check_heartbeat(index)
            index = (index+1) % len(servers)