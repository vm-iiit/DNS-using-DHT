import hashlib

def get_hash(input_string, m):
	print("called")
	hashed_string = hashlib.sha256(input_string.encode()).hexdigest()
	return (int(hashed_string, 16) % (2**m))