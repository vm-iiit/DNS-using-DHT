import Utility_functions as uf

class Node:

	def __init__(self, ip_address, port_number, m, predecessor = None, successor = None):

		self.ip_address = ip_address
		self.port_number = port_number

		self.hashed_node_ID = uf.get_hash(ip_address + port_number, m)

		self.node_finger_table = finger_table(hashed_node_ID, m)
		self.predecessor = predecessor
		self.successor = successor
		self.url_ip_map = dict()
		


class finger_table:

	def __init__(self, hashed_node_ID, m):

		self.table = []
		for i in range(m):
			
			start = (hashed_node_ID + 2**i) % m
			key_range = (start, (hashed_node_ID + 2**(i+1)) % m)
			next_node = hashed_node_ID
			
			self.table.append((start, key_range, next_node))

