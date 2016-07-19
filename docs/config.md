# Using Pegasus to employ a large cluster with multiple EC2 instances for each part of the pipeline

You can also install all the pipeline in one EC2 instance for testing. You may want a instance like M4.large with 8G memory.

Below is about using Pegasus for launching the cluster. You can refer to other document in this directory for manual installation.

Add following to your ~/.bash_profile.

```shell
export VENMOPLUS_HOME=<path-to-this-venmoplus-directory>
export PATH=$VENMOPLUS_HOME:$PATH
source ~/.bash_profile
```

in ./config/pegasus/ directory
run install.sh to launch AWS EC2 instances and install necessary packages.

2 m4.large for kafka
2 m4.xlarge for elasticsearch
1 m4.xlarge for redis
2 m4.large for spark
1  for server


bash install.sh



Elastic Search
====

connect to elasticsearch instance

```
peg fetch $ec-cluster
peg ssh $ec-cluster 1
```
install kibana and sense for better exploring elasticsearch db

```
cd Downloads/
wget https://download.elastic.co/kibana/kibana/kibana-4.5.1-linux-x64.tar.gz
tar xzvf kibana-4.5.1-linux-x64.tar.gz
cd kibana-4.5.1-linux-x64/
./bin/kibana plugin --install elastic/sense
./bin/kibana
```
DNS:5601/



Kafka Setup
======
connect to kafka instance

```
peg fetch $kafka-cluster
peg ssh $kafka-cluster 1
```
create topic for testing

```
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 2 --topic my-topic
```
check topic list

```
/usr/local/kafka/bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic my-topic
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 2 --topic venmo_test
```
install redis elasticsearch support for spark
=====
```
peg ssh spark-qingpeng 2
sudo pip install redis
sudo pip install elasticsearch

peg ssh spark-qingpeng 1
sudo pip install redis
sudo pip install elasticsearch
```
