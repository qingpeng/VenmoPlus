#Some useful tips

## elasticsearch

###You can close/open an index with commands like this:

```shell
curl -XPOST 'localhost:9200/venmo2018/_close'
curl -XPOST 'localhost:9200/venmo2018/_open'
```
###some scripts to load data into elasticsearch in bulk

`python  ~/VenmoPlus/src/batch/load_into_es.py -d venmo2016/`

###Be careful of these record in json
You may have problem while trying to load json into elasticsearch

For some transactions, the receiver is "a phone number" or "an email" without user_id or user_name.



## redis

###get where dump file is located

`redis-cli config get dir`

### load data into redis in bulk

firstly generate command file then load into using pipe

```
python VenmoPlus/src/batch/redis_proc_for_id2.py -d /mnt/s3/venmo-json/ -o full_venmo_id_command.txt &
cat full_venmo_id_command.txt |redis-cli -h ec2-52-11-57-125.us-west-2.compute.amazonaws.com -n 1 --pipe
```
