#!/bin/bash

PEG_ROOT=$PEGASUS_HOME

CLUSTER_NAME=spark2-qingpeng

peg up ${PEG_ROOT}/examples/spark/master.yml &
peg up ${PEG_ROOT}/examples/spark/workers.yml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} hadoop
peg install ${CLUSTER_NAME} spark
