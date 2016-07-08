import random
import sys
import six
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer

class Producer(object):

    def __init__(self, addr):
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, source_symbol, file_to_use):
        file_obj = open(file_to_use, 'r')
        msg_cnt = 0
        while True:
            message_info = file_obj.next()
            print message_info
            self.producer.send_messages('venmo2', source_symbol, message_info)
            msg_cnt += 1

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    file_to_use = str(args[3])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key, file_to_use) 

