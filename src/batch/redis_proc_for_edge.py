# script to prepare for command list to load the edge information into redis db, set for each user id with friends inside

def dump_files(dir_name,file_out):
    file_out_obj = open(file_out, 'w')
    for filename in os.listdir(dir_name):
        if filename[0] != ".":

            file_name = os.path.join(dir_name,filename)
            print file_name
            file_obj = open(file_name, 'r')
            for line in file_obj:
                line = line.rstrip()
                subline = line[1:-1]
                #print subline
                fields = subline.split(",")
                command = ["SADD",fields[0],fields[1]]
                block = get_redis(command)
                file_out_obj.write(block)
                command = ["SADD", fields[1], fields[0]]
                block = get_redis(command)
                file_out_obj.write(block)
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
parser = argparse.ArgumentParser(description='A script to generate COMMAND to dump all edge info into redis')
parser.add_argument('-d', '--directory', help ='directory',required=True)
parser.add_argument('-o', '--output', help ='output file',required=True)


args = parser.parse_args()

dump_files(args.directory,args.output)

