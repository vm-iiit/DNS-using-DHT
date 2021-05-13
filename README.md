# Domain name service using Distributed hash table 

This  is a python implementation of DNS service using [chord](https://pdos.csail.mit.edu/papers/ton:chord/paper-ton.pdf) distributed hash table architecture.

### Features

- Store and retreive URL : ip address mappings as key value pairs; however key value pairs could be anything.
- Customized dynamic load balancer which can account for node additions and departure/failure.
- Scalable ring size
- O(log n) worst case lookup complexity.

### Usage

-  First start the load balancer by running `python load_balancer.py`. By default it runs on port number 9090 which can be changed through `dns_port` variable.
-  Now run `python initiate_DNS_server.py 127.0.0.1:5050 i` where port number is random and `i` flag stands for initialization.
-  For adding subsequent nodes, run `python initiate_DNS_server.py 127.0.0.1:5050 a` where `a` stands for node addition.
-  For DNS queries, send GET request to the url `http://127.0.0.1:9090/query` and send json in the body, like `{"val" :"www.whatsaap.com"}`

- Space delimited key-value pairs are loaded from `data.txt`.
- The ring size is taken as the next higher exponent of 2 from `max_nodes = value` present in `config.txt`. For example if `value` is `100`, the ring size will be `128`.

