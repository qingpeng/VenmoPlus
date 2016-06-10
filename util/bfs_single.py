#from __future__ import print_function

import sys

from graphframes import *
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from pyspark.sql import SQLContext
from pyspark.sql.types import *


import json

if __name__ == "__main__":


    sc = SparkContext(appName="PythonStreamingDirectKafkaWordCount")
    sqlContext = SQLContext(sc)


    file_graph1_obj =open( "/home/ubuntu/Graph/venmo_1370291832.json",'r')
    file_graph2_obj =open( "/home/ubuntu/Graph/venmo_1376956980.json",'r')

    v_list = []
    e_list = []

    for line in file_graph1_obj:
        line = line.rstrip()
        fields = json.loads(line)
        target_id = fields['transactions'][0]['target']['id']
        actor_id = fields['actor']['id']
        message = '0'
        v_list.append((target_id,'0'))
        v_list.append((actor_id,'0'))
        e_list.append((target_id,actor_id,message))
        e_list.append((actor_id,target_id,message))
    
    v = sqlContext.createDataFrame(v_list,["id", "name"])
    e = sqlContext.createDataFrame(e_list,["src", "dst", "message"])
    g = GraphFrame(v, e)

    for line in file_graph2_obj:
        line = line.rstrip()
        fields = json.loads(line)
        target_id = fields['transactions'][0]['target']['id']
        actor_id = fields['actor']['id']
        message = fields['message']
        time = fields['updated_time']
        BFS = g.bfs("id ="+target_id,"id ="+actor_id,maxPathLength=3)
        if BFS.count() > 0:
            distance = (len(BFS.columns) - 1)/2
        else:
            distance = 0
        print target_id, actor_id, message, time, distance

    
