#!/bin/bash

PEG_ROOT=$PEGASUS_HOME

CLUSTER_NAME=es-qingpeng

peg up ${VENMOPLUS_HOME}/config/pegasus/es_master.yml &
peg up ${VENMOPLUS_HOME}/config/pegasus/es_workers.yml &

wait

peg fetch ${CLUSTER_NAME}

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} elasticsearch
