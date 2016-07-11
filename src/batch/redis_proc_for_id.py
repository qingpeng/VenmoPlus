# script to prepare for command list to load the pair of user_id:user_name  into redis db

def dump_json(dir_name,file_out):
    file_out_obj = open(file_out, 'w')

    ids = {}
    for dir2 in os.listdir(dir_name):
        print dir2
        if dir2 !="_temporary":
            for file in os.listdir(os.path.join(dir_name,dir2)):
                file_name = os.path.join(dir_name,dir2,file)
                print file_name
                file_obj = open(file_name, 'r')
                for line in file_obj:
                        #print line
                        try:
                                line = line.rstrip()
          #                      print line
                                fields = json.loads(line)
          #                      print fields
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
    file_out_obj.close()

def get_redis(command):
    block = ""
    block = block + "*" + str(len(command)) + "\r\n"
    for cmd in command:
        block = block + "$" + str(len(cmd)) + "\r\n"
        block = block + cmd + "\r\n"
    return block


import argparse
import os
import json
parser = argparse.ArgumentParser(description='A script to generate COMMAND to dump all json files into redis')
parser.add_argument('-d', '--directory', help ='directory',required=True)
parser.add_argument('-o', '--output', help ='output file',required=True)


args = parser.parse_args()

dump_json(args.directory,args.output)

