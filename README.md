# VenmoPlus.com
### Explore your Venmo network! 
#### an insight data engineering program project


demo video: https://www.youtube.com/watch?v=a_qULTlw1e4

demo slides: http://www.slideshare.net/qingpeng/venmoplus

#### Features

(here, "friends" mean people who have done transanctions with the user.)
* fuzzy searching of user name, with friend list to help identify users with same name
* list recent transactions for a specific user
* **label the relationship between the payer and receiver**, which can be used as a signal for fraud detection. The longest relationship that can be identify is 3rd degree connection, as LinkedIn does. This is not a trivial task!
* friend recommendation, list the friends of your friends who share some friends with you but not your friends yet
* search transactions in your history and the transactions related to your friends with specific items
* list friends of the user and the number of their friends (degree)

#### Repo Structure

**`./src/`** all the important files are here

**`./src/batch/`** scripts to load historic transactions data from S3 into Redis and Elasticsearch DB

- `redis_proc_for_edge.py`: load edge information to Redis, key: user_id value: set with friend list 

- `redis_proc_for_id.py`: load node information to Redis, key: user_id value: user_name

- `load_into_es.py`: load records to elasticsearch

- `helper.scala`: helper code for loading data from S3 to databases distributedly 

- `load_to_es.scala`: load json files from S3 to elasticsearch using connector

**`./src/streaming `** scripts working with Spark Streaming to impliment streaming/real time pipeline, from Venmo API to Redis and Elasticsearch

- `kafka_producer_venmo_api.py`: get realtime transactions from venmo API and send to kafka

- `streaming_consumer_venmo.py`: script working with Spark Streaming to consume messages from kafka and store the records into Elasticsearch and Redis

**`./src/backend`** scripts working with Flask to build APIs

- `./Flask/runbackend.py`: script to launch flask server for API

- `./Flask/backend/__init__.py`: script to build API

- `./Flask/backend/helper.py`: script to implement functions for building API


**`./src/frontend`** stuffs working with AngularJS to build web interface

- `./app/app.js`: AngularJS script to implement frontend function

- `./app/index.html`: default page template

- `./app/pages/main.html`: homepage

- `./app/pages/user.html`: user page

**`./docs/`** instructions about setup, launch the website


#### Pipeline

![alt text](https://raw.githubusercontent.com/qingpeng/VenmoPlus/master/docs/pipeline.png "Pipeline")

#### System

![alt text](https://raw.githubusercontent.com/qingpeng/VenmoPlus/master/docs/system.png "System")


#### Design and Optimizations

##### Replace BFS with Bidirectional Search  

Shortest distance -> intersection of sets (friend lists)

1st degree friends of A ∩ 1st degree friends of B == [] ?

O(N^2) -> O(2*N)

2nd degree friends of A ∩ 1st degree friends of B == []?

 O(N^3) -> O(N + N^2)
 
##### Real time distance query

Query distance between vertices in a historic moment in a constantly changing graph (because we don’t pre-calculate the distance….)
A recent transaction for a user is history and has changed the graph

Query distance of the two users at that moment. (not considering that specific transaction)

Remove the influence of that specific transaction temporarily and restore later
Test if that transaction is the first between the pair of users.

##### Query and Search optimizations

1. Remove aggregation for better performance… (trade-off)
2. Friend recommender: Using Counter to get only 5 users with the most common friends
3. Search message in friend circle
4. Combine query of Elasticsearch and Redis


