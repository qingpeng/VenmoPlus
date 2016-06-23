#!/bin/bash

PEG_ROOT=$PEGASUS_HOME

CLUSTER_NAME=kafka-qingpeng

peg up ${PEG_ROOT}/examples/kafka/master.yml &
peg up ${PEG_ROOT}/examples/kafka/workers.yml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka
