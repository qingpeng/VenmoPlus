#If you want to transfer Redis and Elasticsearch DB from one server to another

## about redis

Use SAVE command or BGSAVE

http://zdk.blinkenshell.org/redis-backup-and-restore/

a good read about Redis data persistence

http://redis.io/topics/persistence

## about elasticsearch

This is really good and convenient tool to migrate index from one ES server to another

https://www.npmjs.com/package/elasticdump

You have to install node.js and npm firstly

```
./elasticdump --input=http://52.34.193.106:9200/venmo_test --output=http://localhost:9200/venmo_test  --type=analyzer
./elasticdump --input=http://52.34.193.106:9200/venmo_test --output=http://localhost:9200/venmo_test  --type=mapping
./elasticdump --input=http://52.34.193.106:9200/venmo_test --output=http://localhost:9200/venmo_test  --type=data --limit 10000 
./elasticdump --input=http://52.34.193.106:9200/venmo2018 --output=http://localhost:9200/venmo2018  --type=analyzer
./elasticdump --input=http://52.34.193.106:9200/venmo2018 --output=http://localhost:9200/venmo2018  --type=mapping
./elasticdump --input=http://52.34.193.106:9200/venmo2018 --output=http://localhost:9200/venmo2018  --type=data --limit=10000
```

