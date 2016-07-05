# ingest real time transaction from Venmo API and send them to Kafka
# 
import random
import sys
import six
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer
import time
import os
import requests
import json

class Producer(object):

    def __init__(self, addr):
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)
        self.sess = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.sess.mount('http://', adapter)
        self.sess.mount('https://', adapter)

    def produce_msgs(self, topic, source_symbol, last_record_set):
        self.record_set = set()
        count = 0
	try:
		for item in self.r["data"]:
		    self.record_set.add(item["payment_id"])
		    count += 1
		    if not item["payment_id"] in last_record_set:
			message_info = "{}\n".format(json.dumps(item))
			self.producer.send_messages(topic, source_symbol, message_info)
	#                print message_info
	#                print count
	except:
		k = 1
		    
    
    def get_venmo(self,limit=300,page="https://venmo.com/api/v5/public?"):
	try:
                self.r = self.sess.get(page + "&limit={}".format(limit)).json()
	except:
		self.r = ""
        
        

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    topic = str(args[2])
    partition_key = str(args[3])
    wait = int(args[4])
    last_record_set = set()
    while True:
        start_time = int(time.time())

        prod = Producer(ip_addr)
        prod.get_venmo()
	if prod.r == "":# if error while connecting to Venmo API
		continue
        prod.produce_msgs(topic, partition_key, last_record_set) 
        last_record_set = prod.record_set
        end_time = int(time.time())
        if end_time - start_time > wait:
            pass
        else:
            time.sleep(wait - (end_time-start_time))

