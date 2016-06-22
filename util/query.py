import redis
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk,bulk,parallel_bulk


# redis DB with edge info
r0 = redis.StrictRedis(host="ec2-52-39-225-153.us-west-2.compute.amazonaws.com", port=6379, db=0)

# redis DB with userID: user name
r1 = redis.StrictRedis(host="ec2-52-39-225-153.us-west-2.compute.amazonaws.com", port=6379, db=1)


es = Elasticsearch(
   ['http://172.31.1.205:9200', 'http://172.31.1.200:9200','http://172.31.1.201:9200'],
   sniff_on_start=True,
   sniff_on_connection_fail=True,
   sniffer_timeout=60
   )
   

def user_list(name):

    
    body_target = 
{
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


    body_actor = 
{
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
    ids = res_target['aggregations']['buckets'].extend(res_actor['aggregations']['buckets'])
    id_dict = {}
    for id in ids:
        if id["key"] in id_dict:
            id_dict[id['key']] +=  id['doc_count']]
        else:
            id_dict[id['key']] =  id['doc_count']]
    sorted_id  = sorted(id_dict.items(), key=operator.itemgetter(1),reverse=True)
    return sorted_id
    

def get_name_for_id(id): # to expand to actor and target or separate redis DB
    search_actor = 
{"size":1,
  "query": {
         "match": { "actor.id" : id }
  }
} 
    res = es.search(index="venmo",doc_type="transaction", body=search_actor)
    return 


def get_recent_transactions(id):
    query = 
{"size":50, 
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
    return res['hits']['hits']
    
def get_distance(a,b):

    if a in r.smembers(b) or b in r.smembers(a):
        return 1
    elif r.smembers(a).isdisjoint(r.smembers(b)) !=True:
        return 2
    else:
         
        second_degree = set()
        for s in r.smembers(a):
            second_degree = second_degree.union(r.smembers(s))
        print second_degree
        print r.smembers(b)
        print second_degree & r.smembers(b)
        if second_degree.isdisjoint(r.smembers(b)):
            return 0
        else:
            return 3
            
def get_friend(id):
    return r.smembers(id)

def get_degree(id):
    return len(r.smembers(id))
    
    
def get_2nd_friend(id):
    second_degree = set()
    for s in r.smembers(a):
        second_degree.union(r.smembers(s))
    return second_degree
    

from collections import Counter

def friend_recommend(a):
    
    second_degree = []
    for s in r.smembers(a):
        second_degree.extend(list(r.smembers(s)))
    recommend_list = []
    for item in Counter(second_degree).most_common():
        if item[0] not in r.smembers(a):
            recommend_list.append(item)
    return recommend_list

def search_message_in_circle(message,id):
    friend_list = list(get_friend(id).union(get_2nd_friend(id)))
    
    query = 
    {"size":50, 
   "query" : {

            "bool" : {
              "should" : [
                 { "terms" : {"actor.id" : friend_list}}, 
                 { "terms" : {"transactions.target.id" : friend_list}}], "minimum_should_match": 1,
            "must":  { "match" : {"message" : message}} 
              
              }
      },
      "sort": { "created_time": { "order": "desc" }}
    res = es.search(index="venmo",doc_type="transaction", body=query)
    return res['hits']['hits']
}

def search_friend_in_circle(id):
    
    
    


