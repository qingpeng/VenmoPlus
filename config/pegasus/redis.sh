#!/bin/bash

PEG_ROOT=$PEGASUS_HOME
#VENMOPLUS_HOME=$VENMOPLUS_HOME
CLUSTER_NAME=redis-qingpeng

peg up ${VENMOPLUS_HOME}/config/pegasus/redis_master.yml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} redis


