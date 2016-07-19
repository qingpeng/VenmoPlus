
From EC2 Image instance
=======

1  Elasticsearch

`screen -S elastic`
`./elasticsearch-2.3.4/bin/elasticsearch`
CtrA -D

2  Redis

`screen -S redis`
`./redis-3.2.1/src/redis-server`

3  flask

`screen -S flask`
`python VenmoPlus/src/backend/Flask/runbackend.py`

4  angularJS

modify app.js to reflect current API server url

`screen -S anglular`

`cd angular-seed/`
`sudo npm start`

5  kafka

`screen -S kafka`
`cd kafka_2.11-0.10.0.0`
`bin/zookeeper-server-start.sh config/zookeeper.properties &`
`bin/kafka-server-start.sh config/server.properties &`

launch kafka producer to fetch realtime data from Venmo API

`cd`
`python VenmoPlus/src/streaming/kafka_producer_venmo_api.py localhost venmo_test 0 15 &`

6  spark

`screen -S spark`
`spark-1.6.1-bin-hadoop2.6/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.1 VenmoPlus/src/streaming/streaming_consumer_venmo.py`

