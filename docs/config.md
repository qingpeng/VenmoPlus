
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
