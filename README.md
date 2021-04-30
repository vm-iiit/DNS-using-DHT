# DNS using DHT 

## How to run load balancer

python3 loadbalancer.py    # By default it is running on port no. 9090

## How to run chord nodes

python3 initiate_server.py 127.0.0.1:8956 i  # port numbers are arbitary

python3 initiate_server.py 127.0.0.1:6023 a 

python3 initiate_server.py 127.0.0.1:5824 a

## How to request from client
There are two options either use curl  or postman

using postman call the load balancer which is running on port 9090

url  127.0.0.1:9090  
body {'val': 'www.google.com'} 


## list of all the mapped url and ip is present in data.txt file
