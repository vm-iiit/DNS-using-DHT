import Utility_functions as uf
from flask import request
import requests

url_prefix = "http://"

class Node:

	def __init__(self, ip_address, port_number, m, predecessor = None, successor = None):

		self.ip_address = ip_address
		self.port_number = port_number

		self.hashed_node_ID = uf.get_hash(ip_address + port_number, m)

		self.node_finger_table = finger_table(self.hashed_node_ID, m, ip_address)
		# self.predecessor = (self.hashed_node_ID, self.ip_address + ':' + self.port_number)
		self.predecessor = None
		self.successor = (self.hashed_node_ID, self.ip_address + ':' + self.port_number)
		self.url_ip_map = dict()
		self.m = m



	def check_in_range_excluded_included(self, lower_val, upper_val, check_val):

		if (lower_val < check_val and check_val <= upper_val) or \
			(upper_val < lower_val and lower_val < check_val) or \
			(check_val <= upper_val and upper_val < lower_val):
			return True
		else:
			False

	def check_in_range_excluded_excluded(self, lower_val, upper_val, check_val):

		if (lower_val < check_val and check_val < upper_val) or \
			(upper_val < lower_val and lower_val < check_val) or \
			(check_val < upper_val and upper_val < lower_val):
			return True
		else:
			False

	def return_my_ip(self):
		return self.ip_address+":"+self.port_number

	def closest_preceeding_node(self, hashed_value):

		for index in range(self.m-1, -1, -1):

			if self.check_in_range_excluded_included(self.hashed_node_ID, hashed_value, self.node_finger_table.table[index][2]):
				return (self.node_finger_table.table[index][2], self.node_finger_table.table[index][3]) 

		return self.successor


	def find_successor(self, hashed_value):
		#print("**********************************")
		if self.check_in_range_excluded_included(self.hashed_node_ID, self.successor[0], hashed_value):
			#print("if", self.successor)
			return self.successor

		else:
			n_bar = self.closest_preceeding_node(hashed_value)

			if n_bar == (self.hashed_node_ID, self.ip_address + ':' + self.port_number):
				#print("same node")
				return self.successor
			#print("else nbar",n_bar)
			data = {'ID' : self.hashed_node_ID}
			#print("calling node",self.ip_address, self.port_number)
			response = requests.get(url_prefix + n_bar[1]+'/find_successor', json = data)
			successor = request.data.decode("utf-8")
			##print("got suc",successor)
			return successor

	def join(self, successor):
		self.predecessor = None
		self.successor = successor


	def stabilize(self):


		response = requests.get(url_prefix + self.successor[1]+'/get_predecessor')
		##print("stabilize resp",response)
		successors_predecessor = response.json()['val']


		if 	successors_predecessor is not None and	\
			self.check_in_range_excluded_excluded(self.hashed_node_ID, self.successor[0], successors_predecessor[0]):
			self.successor = successors_predecessor

		if successors_predecessor is not None and	\
			self.successor == (self.hashed_node_ID, self.ip_address + ':' + self.port_number):
			print("^^^^^^^^^^^^^^^^^^^^^")
			self.successor = successors_predecessor

		print("notify",self.successor)
		data = {'IP_port': self.ip_address + ':' + self.port_number, 'ID':self.hashed_node_ID}
		response = requests.post(url_prefix + self.successor[1]+'/notify', json=data)


	def check_predecessor(self):

		try:
			response = requests.get(url_prefix + self.predecessor[1]+'/check_heartbeat')
		except:
			self.predecessor = None



class finger_table:

	def __init__(self, hashed_node_ID, m, IP_address):

		self.table = []
		for i in range(m):
			
			start = (hashed_node_ID + 2**i) % (2**m)
			key_range = (start, (hashed_node_ID + 2**(i+1)) % (2**m))
			next_node = hashed_node_ID
			
			self.table.append((start, key_range, next_node, IP_address))