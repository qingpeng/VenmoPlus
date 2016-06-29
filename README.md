# VenmoPlus.com
### Explore your Venmo network! 
####an insight data engineering program project

http://www.venmoplus.com


./src/

./src/batch/ 

scripts to load historic transactions data from S3 into Redis and Elasticsearch DB

./src/streaming 

scripts working with Spark Streaming to impliment streaming/real time pipeline, from Venmo API to Redis and Elasticsearch

./src/backend 

scripts working with Flask to build APIs

./src/frontend 

scripts working with AngularJS to build web interface

./docs/    

instructions about setup, launch the website
  
demo video: https://www.youtube.com/watch?v=a_qULTlw1e4

demo slides: http://www.slideshare.net/qingpeng/qingpeng-zhang-week5

pipeline:

![alt text](https://raw.githubusercontent.com/qingpeng/VenmoPlus/master/docs/pipeline.png "Pipeline")

system:

![alt text](https://raw.githubusercontent.com/qingpeng/VenmoPlus/master/docs/system.png "System")


###Design and Optimizations

####Algorithm 1
Shortest distance -> intersection of sets (friend lists)

1st degree friends of A ∩ 1st degree friends of B == [] ?

2nd degree friends of A ∩ 1st degree friends of B == []?

####Algorithm 2
Query distance between vertices in a historic moment in a constantly changing graph (because we don’t pre-calculate the distance….)
A recent transaction for a user is history and has changed the graph

Query distance of the two users at that moment. (not considering that specific transaction)

Remove the influence of that specific transaction temporarily and restore later
Test if that transaction is the first between the pair of users.

###Query and Search optimizations

1. Remove aggregation for better performance… (trade-off)
2. Friend recommender: 
- Using Counter to get only 5 users with the most common friends
3. Search message in friend circle
4. Combine query of Elasticsearch and Redis


