#Launch the system based on Pegasus
(under construction...)

##Streaming process

1. run kafka producer to retrieve new venmo transactions from venmo API

run on kafka instance #2
```
% peg ssh kafka-qingpeng 2

git clone https://github.com/qingpeng/VenmoPlus.git
sudo pip install kafka-python
screen -S kafka
python VenmoPlus/src/streaming/kafka_producer_venmo_api.py 52.40.167.57 venmo_test 0 15
```
Now the new venmo transactions are sending to Kafka servers for Spark Streaming to consume.

2. run Spark Streaming to retrieve new venmo transactions from Kafka servers and store the records into 
Redis and Elasticsearch DB

run on spark instance #1
```
% peg ssh spark-qingpeng 1
screen -S spark
spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.1 VenmoPlus/src/streaming/streaming_consumer_venmo.py
```

