ubuntu@ip-172-31-1-198:~$ more redis_proc_for_id.py
#!/usr/bin/env python
import sys
import argparse
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk,bulk,parallel_bulk

parser = argparse.ArgumentParser(description='A script to dump id and name to redis db')
parser.add_argument('-d', '--directory', help ='TMP directory',required=True)
parser.add_argument('-o', '--output', help ='output file for load into redis',required=True)



args = parser.parse_args()


import json


def get_redis(cmds):
	line = ""
	line = line + "*" + str(len(cmds)) + "\r\n"
	for cmd in cmds:
		line = line + "$" + str(len(cmd)) + "\r\n" + cmd + "\r\n"
	return line


def process_file(file_name):
	file_obj = open(file_name, 'r')
	for line in file_obj:
		try:
			line = line.rstrip()
			fields = json.loads(line)
			#rint line
			target_id = fields['transactions'][0]['target']['id']
			target_name = fields['transactions'][0]['target']['name']
			actor_id = fields['actor']['id']
			actor_name = fields['actor']['name']
			ids[actor_id] = actor_name
			ids[target_id] = target_name
		except:
			i = 1
	for each_id in ids.keys():

		command1 = ['SET', each_id,ids[each_id]]
		file_out_obj.write(get_redis(command1))



def dump_json(dir):
    ids = {}
    for dir2 in os.listdir(dir):
        print dir2
        if dir2 !="_temporary":
            for file in os.listdir(os.path.join(dir,dir2)):
                file_name = os.path.join(dir,dir2,file)
                print file_name
		file_obj = open(file_name, 'r')
		for line in file_obj:
			try:
				line = line.rstrip()
				fields = json.loads(line)
				#rint line
				target_id = fields['transactions'][0]['target']['id']
				target_name = fields['transactions'][0]['target']['name']
				actor_id = fields['actor']['id']
				actor_name = fields['actor']['name']
				ids[str(actor_id)] = actor_name
				ids[str(target_id)] = target_name
			except:
				i = 1
                file_obj.close()
    for each_id in ids.keys():

	command1 = ['SET', each_id,ids[each_id]]
	#print command1
	try:
		file_out_obj.write(get_redis(command1))
	except:
		s=1



file_out_obj = open(args.output, 'w')
dump_json(args.directory)

file_out_obj.close()