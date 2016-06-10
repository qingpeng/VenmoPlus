from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pyspark.sql import SQLContext
from pyspark.sql.types import *


import json

def process_RDD(RDD):
    lines = RDD.collect()
    for line in lines:
        process_line(line)
    #RDD.foreach(process_line)

def process_line(line):
    line = line.rstrip()
    fields = json.loads(line)
    try:
        target_id = fields['transactions'][0]['target']['id']
        actor_id = fields['actor']['id']
        message = fields['message']
        target_name = fields['transactions'][0]['target']['name']
        actor_name = fields['actor']['name']
        time = fields['updated_time']
        payment_id = fields['payment_id']
#    payment_id.pprint() 
        transaction = sqlContext.createDataFrame([(payment_id,actor_id,message,target_id,time),], ["payment_id","actor_id","message","target_id","time"])
        user =  sqlContext.createDataFrame([(target_id,target_name),(actor_id,actor_name),], ["id","name"])
        user.show()
        transaction.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="transactions", keyspace="venmo_streaming").save()
        user.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="user", keyspace="venmo_streaming").save()
    except:
        pass
#

if __name__ == "__main__":


    sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
    sqlContext = SQLContext(sc)


#    file_graph_obj = open("/home/ubuntu/Graph/venmo_1370291832.json",'r')

#    for line in file_graph_obj.readlines(20):
#        process_line(line)

#    exit()


    ssc = StreamingContext(sc, 2)
    brokers = "ec2-52-40-166-123.us-west-2.compute.amazonaws.com:9092"
    topic = "venmo2"

    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: x[1])
#    count2=lines.count()
#    lines.pprint()
    lines.foreachRDD(process_RDD)

    #count2.pprint()

    ssc.start()
    ssc.awaitTermination()


