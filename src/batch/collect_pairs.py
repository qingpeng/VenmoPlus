#!/usr/bin/env python
import argparse
import os



parser = argparse.ArgumentParser(description='A script to extract all pairs from TMP di
rectory')
parser.add_argument('-d', '--directory', help ='TMP directory',required=True)
parser.add_argument('-o', '--outfile', help ='output file', required=True)

args = parser.parse_args()



def parse_pairs(dir, output):
    """parse pairs from tmp directory"""
    fh_output = open(output, 'w')

    for dir2 in os.listdir(dir):
        print dir2
        if dir2 !="_temporary":
            for file in os.listdir(os.path.join(dir,dir2)):
                file_name = os.path.join(dir,dir2,file)
                print file_name
                f = open(file_name, 'r')
                for line in f:
                    fh_output.write(line)
    fh_output.close()


parse_pairs(args.directory, args.outfile)
