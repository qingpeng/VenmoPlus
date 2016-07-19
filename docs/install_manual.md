
If you want to install the tools manually
======

##Redis

```shell
$ wget http://download.redis.io/releases/redis-3.2.1.tar.gz
$ tar xzf redis-3.2.1.tar.gz
$ cd redis-3.2.1
$ make
```

##Elasticsearch

Install Kibana


https://www.elastic.co/downloads/kibana


##Flask


/home/ec2-user/VenmoPlus/src/backend/Flask

```
sudo pip install Flask
sudo pip install flask-restful
sudo pip install flask_cors
sudo pip install redis
sudo pip install elasticsearch
python runbackend.py
```
##Angular-JS

angular-seed
Use this as template..

https://github.com/angular/angular-seed

git clone https://github.com/angular/angular-seed.git

`npm install`

require node.js

You may want to copy/move those npm/node to your /usr/bin/

ln -fs app ...

##Kafka

download kafka

http://kafka.apache.org/downloads.html

```
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic venmo_test
sudo pip install kafka
python VenmoPlus/src/streaming/kafka_producer_venmo_api.py localhost venmo_test 0 15 &
```

##Spark
Download and extract spark 

http://spark.apache.org/downloads.html


spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.1 VenmoPlus/src/streaming/streaming_consumer_venmo.py &



  

