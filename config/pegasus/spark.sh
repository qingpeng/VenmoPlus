#!/bin/bash

PEG_ROOT=$PEGASUS_HOME

CLUSTER_NAME=spark-qingpeng

peg up ${VENMOPLUS_HOME}/config/pegasus/spark_master.yml &
peg up ${VENMOPLUS_HOME}/config/pegasus/spark_workers.yml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} hadoop
peg install ${CLUSTER_NAME} spark
