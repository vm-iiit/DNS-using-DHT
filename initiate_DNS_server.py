import sys
import math
import threading
from flask import Flask
import Utility_functions as uf
from node_structure import Node, finger_table
from flaskthreads import AppContextThread
from flask import request

import requests

global DNS_server

successful_response = {'job':True}
failed_response = {'job':False}

DNS_url = "127.0.0.1:6969/"
url_prefix = "http://"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", message="Hello Flask!");   

@app.route("/get_ip")
def get_ip():

	global DNS_server
	return DNS_server.return_my_ip()

@app.route('/node_join', methods=['GET', 'POST'])
def node_join():
	

	print(request.data.decode("utf-8"))
	return successful_response

if __name__ == "__main__":

	ip_port = sys.argv[1]
	mode = sys.argv[2]              #i to initiate DNS, a to add node


	ip_address, port = ip_port.split(':')

	threading.Thread(target = app.run, kwargs={"host":ip_address, "port":port, "debug":False}).start()


	with open('config.txt', 'r') as input_file:
		max_nodes_value = int(input_file.readline().strip().split('=')[1].strip())
		m = math.ceil(math.log2(max_nodes_value))

	
	DNS_server = Node(ip_address, port, m)

	if mode == "i":
		
		with open('data.txt', 'r') as input_file:

			for line in input_file.readlines():

				url, ip_address = line.strip().split()
				DNS_server.url_ip_map[url] = ip_address

	else :

		DNS_server = Node(ip_address, port, m)
		DNS_server.successor = DNS_server.hashed_node_ID

		response = requests.get(url_prefix+DNS_url+'get_ip')
		
		peer_ip_address, peer_port = response.text.strip().split(':')

		data = {'a':10, 'b':12}
		response = requests.post(url_prefix+peer_ip_address+':'+peer_port+'/node_join', json=data)


		






		






