parser = argparse.ArgumentParser(description='A script to dump all json files into elastic search db')
parser.add_argument('-d', '--directory', help ='TMP directory',required=True)

args = parser.parse_args()


es = Elasticsearch(
   ['http://172.31.1.205:9200', 'http://172.31.1.200:9200','http://172.31.1.201:9200'],
   sniff_on_start=True,
   sniff_on_connection_fail=True,
   sniffer_timeout=60
   )

def dump_json(dir):
    s = {}
    for dir2 in os.listdir(dir):
        print dir2
        if dir2 !="_temporary":
            for file in os.listdir(os.path.join(dir,dir2)):
                file_name = os.path.join(dir,dir2,file)
                print file_name
                f = open(file_name, 'r')
                for line in f:
                    line = str(line.rstrip())
                   # print s.format(line)
                    s = {'_op_type':'create','_type':'transaction','_source':line}
                    yield(s)
                  #  print line
#dump_json(args.directory)
success, _ = parallel_bulk(es,dump_json(args.directory),index='venmo',thread_count=4,raise_on_error=False)
print('Performed %d actions' % success)
#count = 0
#for item in dump_json(args.directory):
#    print count
#    print item
#    count += 1
