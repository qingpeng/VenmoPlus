from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pyspark.sql import SQLContext
from pyspark.sql.types import *


import json
import redis
from elasticsearch import Elasticsearch

def process_RDD(RDD,r0,r1,es):

    lines = RDD.collect()
    for line in lines:
        process_line(line,r0,r1,es)
    #RDD.foreach(process_line)

def process_line(line,r0,r1,es):
    line = line.rstrip()
    fields = json.loads(line)
    es.index(index='venmo_test', doc_type='payment', body=fields)
    try:
        target_id = fields['transactions'][0]['target']['id']
        actor_id = fields['actor']['id']
        message = fields['message']
        target_name = fields['transactions'][0]['target']['name']
        actor_name = fields['actor']['name']
        time = fields['updated_time']
        payment_id = fields['payment_id']

        r0.sadd(target_id,actor_id)
        r0.sadd(actor_id,target_id)
        r1.setnx(target_id,target_name)
        r1.setnx(actor_id,actor_name)
    except:
        pass



#        transaction = sqlContext.createDataFrame([(payment_id,actor_id,message,target_id,tim
#e,actor_degree,target_degree),], ["payment_id","actor_id","message","target_id","time","acto
#r_degree","target_degree"])
#        user =  sqlContext.createDataFrame([(target_id,target_name),(actor_id,actor_name),],
# ["id","name"])
#        user.show()
#        transaction.write.format("org.apache.spark.sql.cassandra").mode('append').options(ta
#ble="transaction_degree", keyspace="venmo_streaming").save()
#        user.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="us
#er", keyspace="venmo_streaming").save()
#

if __name__ == "__main__":

    sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
    sqlContext = SQLContext(sc)

    ssc = StreamingContext(sc, 2)
    brokers = "52.40.167.57:9092"
    topic = "venmo_test"

    r0 = redis.StrictRedis(host='52.11.57.125', port=6379, db=0)
    r1 = redis.StrictRedis(host='52.11.57.125', port=6379, db=1)
    es = Elasticsearch([{'host': '52.34.193.106', 'port': 9200}])

  #  degree_DF = sqlContext.read.format("org.apache.spark.sql.cassandra").options(table="degr
#ee", keyspace="venmo_streaming").load()
#    degree_DF.cache()
    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
    lines = kvs.map(lambda x: x[1])
#    count2=lines.count()
#    lines.pprint()
    lines.foreachRDD(process_RDD,r0,r1,es)

    #count2.pprint()

    ssc.start()
    ssc.awaitTermination()
