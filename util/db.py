
count = 0
for line in file_graph_obj:
    line = line.rstrip()
    fields = json.loads(line)
    target_id = fields['transactions'][0]['target']['id']
    actor_id = fields['actor']['id']
    message = fields['message']
    target_name = fields['transactions'][0]['target']['name']
    actor_name = fields['actor']['name']
    time = fields['updated_time']
    payment_id = fields['payment_id']
    
    transaction = sqlContext.createDataFrame([(payment_id,actor_id,message,target_id,time),], ["payment_id","actor_id","message","target_id","time"])
    user =  sqlContext.createDataFrame([(target_id,target_name),(actor_id,actor_name),], ["id","name"])
    transaction.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="transactions", keyspace="venmo_streaming").save()
    user.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="user", keyspace="venmo_streaming").save()
    
    count += 1
    if count >100:
        break
