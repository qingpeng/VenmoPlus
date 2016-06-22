ubuntu@ip-172-31-1-198:~$ vi redis_proc_for_id.py

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