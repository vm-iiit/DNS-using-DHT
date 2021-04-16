import Utility_functions as uf


class Node:

	def __init__(self, ip_address, port_number, m, predecessor = None, successor = None):

		self.ip_address = ip_address
		self.port_number = port_number

		self.hashed_node_ID = uf.get_hash(ip_address + port_number, m)

		self.node_finger_table = finger_table(self.hashed_node_ID, m, ip_address)
		self.predecessor = predecessor
		self.successor = successor
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

		for index in range(len(self.node_finger_table)-1, -1, -1):

			if check_in_range_excluded_included(self.hashed_node_ID, hashed_value, self.node_finger_table[index][2]):
				return self.node_finger_table[index][3]

		return self.ip_address


	def find_successor(self, hashed_value):

		if check_in_range_excluded_included(self.hashed_node_ID, self.successor, hashed_value):
			return self.successor

		else:
			n_bar = self.closest_preceeding_node(hashed_value)
			return n_bar.find_successor(hashed_value)

	def join(self, new_node_IP):
		pass


		


class finger_table:

	def __init__(self, hashed_node_ID, m, IP_address):

		self.table = []
		for i in range(m):
			
			start = (hashed_node_ID + 2**i) % (2**m)
			key_range = (start, (hashed_node_ID + 2**(i+1)) % (2**m))
			next_node = hashed_node_ID
			
			self.table.append((start, key_range, next_node, IP_address))