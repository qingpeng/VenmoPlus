#!/bin/bash

PEG_ROOT=$PEGASUS_HOME

CLUSTER_NAME=kafka-qingpeng

peg up ${VENMOPLUS_HOME}/config/pegasus/kafka_master.yml &
peg up ${VENMOPLUS_HOME}/config/pegasus/kafka_workers.yml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} hadoop
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka

