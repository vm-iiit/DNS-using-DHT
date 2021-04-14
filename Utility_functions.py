import hashlib

def get_hash(input_string, m):

	hashed_string = hashlib.sha256(input_string.encode())

	return (int(hashed_string, 16) % m)