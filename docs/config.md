
Add following to your ~/.bash_profile.

export VENMOPLUS_HOME=<path-to-this-venmoplus-directory>
export PATH=$VENMOPLUS_HOME:$PATH

$ source ~/.bash_profile

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

peg fetch $ec-cluster
peg ssh $ec-cluster 1

install 

cd Downloads/
wget https://download.elastic.co/kibana/kibana/kibana-4.5.1-linux-x64.tar.gz
tar xzvf kibana-4.5.1-linux-x64.tar.gz
cd kibana-4.5.1-linux-x64/
./bin/kibana plugin --install elastic/sense
./bin/kibana

DNS:5601/




