import sys
import math
import threading
from flask import Flask
import Utility_functions as uf
from node_structure import Node, finger_table
from flask import request
import time

import requests

global DNS_server

successful_response = {'job':True}
failed_response = {'job':False}

DNS_url = "127.0.0.1:7070/"
url_prefix = "http://"

refresh_time_seconds = 1

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", message="Hello Flask!");   

@app.route("/get_ip")
def get_ip():

	global DNS_server
	return DNS_server.return_my_ip()

@app.route("/check_heartbeat")
def heartbeat():
	return successful_response

@app.route('/node_join', methods=['GET', 'POST'])
def node_join():

	data_dict = eval(request.data.decode("utf-8"))

	arg = uf.get_hash(data_dict['ip']+data_dict['port'], DNS_server.m)

	successor = DNS_server.find_successor(arg)
	
	return {'val':successor}

@app.route('/find_successor', methods=['GET', 'POST'])
def get_successor():
	data_dict = eval(request.data.decode("utf-8"))

	successor = DNS_server.find_successor(data_dict['ID'])
	return {'val': successor}

@app.route('/get_predecessor')
def return_predecessor():
	return {'val':DNS_server.predecessor}

@app.route('/notify', methods=['GET', 'POST'])
def notify():
	
	data_dict = eval(request.data.decode("utf-8"))

	if DNS_server.predecessor == None or \
		DNS_server.predecessor == (DNS_server.hashed_node_ID, DNS_server.ip_address + ':' + DNS_server.port_number) or \
		DNS_server.check_in_range_excluded_excluded(DNS_server.predecessor[0], DNS_server.hashed_node_ID, data_dict['ID']):
		
		DNS_server.predecessor = (data_dict['ID'], data_dict['IP_port'])
	
	return successful_response

@app.route('/query', methods=['GET', 'POST'])
def url_query():

	query_value = eval(request.data.decode("utf-8"))['val']

	if type(query_value) != int :
		hashed_query = uf.get_hash(query_value, DNS_server.m)

	else:
		hashed_query = query_value

	return {'val' :DNS_server.answer_query(hashed_query)}


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

		data = {'ip':ip_address, 'port':port}
		response = requests.get(url_prefix+peer_ip_address+':'+peer_port+'/node_join', json=data)

		DNS_server.join(tuple(response.json()['val']))

	while True:
		time.sleep(refresh_time_seconds)

		DNS_server.stabilize()
		DNS_server.fix_fingers()
		DNS_server.check_predecessor()
		
		print("ip port",DNS_server.ip_address+':'+DNS_server.port_number)
		print("suc pred", DNS_server.successor, DNS_server.predecessor)
		print("node ID",DNS_server.hashed_node_ID)


		

		


