import redis
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk,bulk,parallel_bulk


# redis DB with edge info
r0 = redis.StrictRedis(host="ec2-52-39-225-153.us-west-2.compute.amazonaws.com", port=6379, db=0)

# redis DB with userID: user name
r1 = redis.StrictRedis(host="ec2-52-39-225-153.us-west-2.compute.amazonaws.com", port=6379, db=1)

es = Elasticsearch(
   ['52.41.91.188:9200', '52.41.104.252:9200','52.26.39.161:9200'],
   sniff_on_start=False,
   sniff_on_connection_fail=False,
   #sniffer_timeout=60
   )

def get_friend(vertex):
    return r0.smembers(vertex)

def get_degree(vertex):
    return len(r0.smembers(vertex))
    
def get_2nd_friend(vertex):
    second_degree = set()
    friends = get_friend(vertex)
    for s in friends:
        second_degree = second_degree.union(r0.smembers(s))
    return second_degree-friends
    
def get_distance(r,a,b,updated_time): # if updated_time ='n/a', if there is one record in ES, assume it is not current, 
    # so the record is old, no new conenction, distance  = 1
    if test_new_connection(a,b,updated_time) == False:
        return 1
 #   if a in r.smembers(b) or b in r.smembers(a):
 #       return 1
    else:
        r.srem(a,b)
        
        if r.smembers(a).isdisjoint(r.smembers(b)) !=True:
            r.sadd(a,b)
            return 2
        else:

            second_degree = set()
            for s in r.smembers(a):
                second_degree = second_degree.union(r.smembers(s))
            #print second_degree
            #print r.smembers(b)
            #print second_degree & r.smembers(b)
            if second_degree.isdisjoint(r.smembers(b)):
                r.sadd(a,b)
                return 0
            else:
                r.sadd(a,b)
                return 3
        
        

from collections import Counter
def friend_recommend(r0,r1,a):
    
    second_degree = []
    friends = get_friend(a)
    for s in friends:
        #print r.smembers(s)
        second_degree.extend(list(r0.smembers(s)))
    recommend_list = []
    newcounter = Counter(second_degree)
    del newcounter[a]
    for i in friends:
        del newcounter[i]
    friend_list = []
    friends = newcounter.most_common(5)

    for friend in friends:
        friend_dict = {}
        friend_dict['user_id'] = friend[0]
        friend_dict['shared_friend_count'] = friend[1]
        friend_dict['name'] = r1.get(friend[0])
        friend_list.append(friend_dict)
    return friend_list
 



def test_new_connection(a,b,updated_time): # test if this is the first connection between the two users.
    query ={ 
    "size":2, 
       "query" : {

                "bool" : {
                  "must" : [
                     { "term" : {"actor.id" : a}}, 
                     { "term" : {"transactions.target.id" : b}} 
                  ]

             }
          }
    }
    res = es.search(index="venmo",doc_type="transaction", body=query)
    if res['hits']['total'] == 0: 
    # current record has not been indexed by ES and no previous record
        return True
    elif res['hits']['total'] == 1 :
        if res['hits']['hits'][0]['_source']['updated_time'] == updated_time:
              # only current record in ES 
            return True
        
        else:
            # older 1 record in ES
            return False
      

    else:
         # more than 1 records in ES
        return False

import json

def get_recent_transactions(id): # for specific user, also with distance between the pair of users.
    query ={ 
    "size":50, 
       "query" : {
          "constant_score" : { 
             "filter" : {
                "bool" : {
                  "should" : [
                     { "term" : {"actor.id" : id}}, 
                     { "term" : {"transactions.target.id" : id}} 
                  ]
                  }
               }
             }
          },
          "sort": { "created_time": { "order": "desc" }}
    }
    res = es.search(index="venmo",doc_type="transaction", body=query)
    transactions = []
    for hit in res['hits']['hits']:
        payment_id = hit['_source']['payment_id']
        time = hit['_source']['updated_time']
        message = hit['_source']['message']
        actor_id = hit['_source']['actor']['id']
        actor_name = hit['_source']['actor']['name']
        target_id = hit['_source']['transactions'][0]['target']['id']
        target_name = hit['_source']['transactions'][0]['target']['name']
        distance = get_distance(r0,actor_id,target_id,time) # add time stamp
        transactions.append([payment_id, time,message,actor_id,actor_name,target_id,target_name,distance])
    return transactions
    

def search_message_in_circle(message,id,degree):
    if degree ==2:
        friend_list = list(get_friend(id).union(get_2nd_friend(id)))
    elif degree == 1:
        friend_list = list(get_friend(id))
    #print friend_list
    query = {
        "size":50, 
    "query" : {

            "bool" : {
              "should" : [
                 { "terms" : {"actor.id" : friend_list}}, 
                 { "terms" : {"transactions.target.id" : friend_list}}], "minimum_should_match": 1,
            "must":  { "match" : {"message" : message}} 
              
              }
      },
      "sort": { "created_time": { "order": "desc" }
              }
        }
    res = es.search(index="venmo",doc_type="transaction", body=query)
    transactions = []
    for hit in res['hits']['hits']:
	transactions_dict = {}
        payment_id = hit['_source']['payment_id']
        time = hit['_source']['updated_time']
        message = hit['_source']['message']
        actor_id = hit['_source']['actor']['id']
        actor_name = hit['_source']['actor']['name']
        target_id = hit['_source']['transactions'][0]['target']['id']
        target_name = hit['_source']['transactions'][0]['target']['name']
        #transactions.append([payment_id, time,message,actor_id,actor_name,target_id,target_name,distance])
	transactions_dict['payment_id'] = payment_id
	transactions_dict['actor_id'] = actor_id
	transactions_dict['actor_name' ] = actor_name
	transactions_dict['target_id']= target_id
	transactions_dict['target_name'] = target_name
	transactions_dict['time'] = time
	transactions_dict['message'] = message
	transactions.append(transactions_dict)

 
    return transactions



import operator
def list_user(name):

    
    body_target = {
  "query": {
         "match": { "transactions.target.name" : name }
  },
  "aggs" :{
    "number": {
      "terms":{
        "field":"transactions.target.id"
      }
    }
  }
}


    body_actor = {
  "query": {
         "match": { "actor.name" : name }
  },
  "aggs" :{
    "number": {
      "terms":{
        "field":"actor.id"
      }
    }
  }
} 
    res_target = es.search(index="venmo",doc_type="transaction", body=body_target)
    res_actor = es.search(index="venmo",doc_type="transaction", body=body_actor)
    #print res_target
    #print "===============\n\n"
    #print res_actor
    #print res_target['aggregations']['number']['buckets']
    #print res_actor['aggregations']['number']['buckets']
    ids = res_target['aggregations']['number']['buckets']+res_actor['aggregations']['number']['buckets']
    #print ids
    id_dict = {}
    for id in ids:
        if id["key"] in id_dict:
            id_dict[id['key']] +=  id['doc_count']
        else:
            id_dict[id['key']] =  id['doc_count']
    #print id_dict
    sorted_id  = sorted(id_dict.items(), key=operator.itemgetter(1),reverse=True)
    r1 = redis.StrictRedis(host="ec2-52-39-225-153.us-west-2.compute.amazonaws.com", port=6379, db=1)


    sorted_name = [(x,r1.get(x),y,) for x,y in sorted_id]
    name_list = []
    for name in sorted_name:
        name_dict = {}
        name_dict['user_id'] = name[0]
        name_dict['name'] = name[1]
        name_dict['transactions_number'] = name[2]
        name_list.append(name_dict)
    return name_list
