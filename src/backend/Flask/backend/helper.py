# helper script to work with __init__.py to build API for frontend to call
#

import redis 
from elasticsearch import Elasticsearch 
from elasticsearch.helpers import streaming_bulk,bulk,parallel_bulk


# redis DB with edge info
r0 = redis.StrictRedis(host="localhost", port=6379, db=0)

# redis DB with userID: user name
r1 = redis.StrictRedis(host="localhost", port=6379, db=1)

es = Elasticsearch(
        ['localhost:9200'],
   sniff_on_start=False,
   sniff_on_connection_fail=False,
   #sniffer_timeout=60
   )
#es_index = ["venmo_test","venmo2018"]
es_index = "venmo_test" 
es_type = "payment"
#es_type = ["payment","transaction"]
redis_server = "localhost"


def get_friend(vertex):
    return r0.smembers(vertex)

def get_name(user_id):
    name = {}
    name['id'] = user_id
    name['name'] = r1.get(user_id)
    return name

def get_friend_list(user_id):
    friend_list = []
    for friend in r0.smembers(user_id):
        friend_dict = {}
        friend_dict['id'] = friend
        friend_dict['name'] = r1.get(friend)
        friend_dict['degree'] = get_degree(friend)
        friend_list.append(friend_dict)
    return friend_list



def get_degree(vertex):
    return len(r0.smembers(vertex))
    
def get_2nd_friend(vertex):
    second_degree = set()
    friends = get_friend(vertex)
    for s in friends:
        second_degree = second_degree.union(r0.smembers(s))
    return second_degree-friends
    
def get_distance(r,a,b,updated_time): # if updated_time ='n/a', if there is one record in ES, assume it is not 
    # so there are transactions before this one, so distance is 1
    if test_new_connection(a,b,updated_time) == False:
        return 1
 #   if a in r.smembers(b) or b in r.smembers(a):
 #       return 1
    else:
        r.srem(a,b)
        r.srem(b,a)
        
        if r.smembers(a).isdisjoint(r.smembers(b)) !=True:
            r.sadd(a,b)
            r.sadd(b,a)
            return 2
        else:

            second_degree = set()
            for s in r.smembers(a):
                second_degree = second_degree.union(r.smembers(s))
            #print second_degree print r.smembers(b) print second_degree & r.smembers(b)
            if second_degree.isdisjoint(r.smembers(b)):
                r.sadd(a,b)
                r.sadd(b,a)
                return 0
            else:
                r.sadd(a,b)
                r.sadd(b,a)
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
    if friend_list == []:
	friend_list = [{'user_id':'N/A','shared_friend_count':'N/A','name':'N/A'}]

    return friend_list
 



def test_new_connection(a,b,updated_time): # test if this is the first connection between the two users.
    query ={
    "size":1,
            "query" : {

                     "bool" : {
                       "should":[{
                         "bool":{
                       "must" : [
                          { "term" : {"actor.id" : a}},
                          { "term" : {"transactions.target.id" : b}},
                          {"range": {"updated_time":{"lt":updated_time}}}
                       ]
                       }},
                       {"bool":{
                   
                       "must" : [
                          { "term" : {"actor.id" : b}},
                          { "term" : {"transactions.target.id" : a}},
                          {"range": {"updated_time":{"lt":updated_time}}}
                       ]
                       }
                       }]
                  }
               }
           
    }
    res = es.search(index=es_index,doc_type=es_type, body=query)
    #print a,b,updated_time,res['hits']['total']
    if res['hits']['total'] == 0:
        # no transactions before this one
        return True

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
    res = es.search(index=es_index,doc_type=es_type, body=query)
    transactions = []
    for hit in res['hits']['hits']:
	transaction_dict = {}

        payment_id = hit['_source']['payment_id']
        time = hit['_source']['updated_time']
        message = hit['_source']['message']
        actor_id = hit['_source']['actor']['id']
        actor_name = hit['_source']['actor']['name']
        target_id = hit['_source']['transactions'][0]['target']['id']
        target_name = hit['_source']['transactions'][0]['target']['name']
        distance = get_distance(r0,actor_id,target_id,time) # add time stamp
	transaction_dict['actor_name'] = actor_name
	transaction_dict['actor_id'] = actor_id
	transaction_dict['target_name'] = target_name
	transaction_dict['target_id'] = target_id
        if distance == 0:
            distance = ">3rd (Know this guy???)"
        elif distance == 1:
            distance = "1st"
        elif distance == 2:
            distance = "2nd"
        elif distance == 3:
            distance = "3rd"
	transaction_dict['distance'] = distance
	transaction_dict['time'] = time
	transaction_dict['message'] = message
	transactions.append(transaction_dict)
    if transactions == []:
	transactions = [{'actor_name':'N/A','actor_id':'N/A','target_name':'N/A','target_id':'N/A','distance':'N/A','time':'N/A','message':'N/A'}]
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
            "must": { "match" : {"message" : message}}
              
              }
      },
      "sort": { "created_time": { "order": "desc" }
              }
        }
    res = es.search(index=es_index,doc_type=es_type, body=query)
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
    if transactions == []:
        transactions = [{'message':'N/A','time':'N/A','actor_name':'N/A','target_name':'N/A'}]
 
    return transactions



import operator 
def list_user(name):
    print name

    
    body_target = {
  "size":10,
  "query": {
         "match": { "transactions.target.name" : name }
  }
#  "aggs" :{
#    "number": {
#      "terms":{
#        "field":"transactions.target.id", "size": 0
#      }
#    }
#  }
}


    body_actor = {
   "size":10,
   "query": {
         "match": { "actor.name" : name }
  }
 # "aggs" :{
 #   "number": {
 #     "terms":{
 #       "field":"actor.id", "size": 0
 #     }
 #   }
 # }
} 
    res_target = es.search(index=es_index,doc_type=es_type, body=body_target)
    #print res_target
    res_actor = es.search(index=es_index,doc_type=es_type, body=body_actor)
    #print res_target print "===============\n\n" print res_actor print 
    #res_target['aggregations']['number']['buckets'] print res_actor['aggregations']['number']['buckets']
#    ids = res_target['aggregations']['number']['buckets']+res_actor['aggregations']['number']['buckets']
    #print ids
#    id_dict = {} for id in ids:
#        if id["key"] in id_dict:
#            id_dict[id['key']] += id['doc_count'] else: id_dict[id['key']] = id['doc_count']
    #print id_dict
   # sorted_id = sorted(id_dict.items(), key=operator.itemgetter(1),reverse=True) r1 = 
   # redis.StrictRedis(host=redis_server, port=6379, db=1)
    hits_target = res_target["hits"]["hits"]
    hits_actor = res_actor["hits"]["hits"]

    final_list = []
    #print len(hits_target) print range(len(hits_target)) print res_target print hits_target
   # if len(hits_target) > len(hits_actor):
   #     size = len(hits_target)
   # else:
   #     size = len(hits_actor)
    for i in range(10):
   #     print i
        try:
            item = hits_target[i]["_source"]["transactions"][0]["target"]["id"]
            #print item
            if not item in final_list:
                final_list.append(item)
        except IndexError:
            pass
        #print "here"
        try:
            item = hits_actor[i]["_source"]["actor"]["id"]
            if not item in final_list:
                final_list.append(item)
        except IndexError:
            pass

   # print final_list
    if final_list == []:
        name_list = [{'user_id':'N/A','name':'N/A','transactions_number':'N/A','friend':'N/A'}]
        return name_list
    if len(final_list)>1:
        if r1.get(final_list[1]).lower() == name.lower():
            s = final_list.pop(0)
            final_list.insert(1,s)

    name_list = []
    for user_id in final_list:
        name_dict = {}
        name_dict['user_id'] = user_id
        name_dict['name'] = r1.get(user_id)
        friends_list = r0.smembers(user_id)
        friends_name_list = [r1.get(x) for x in friends_list]
        try:
            friend_str = ', '.join(friends_name_list)[0:100]
        except:
            friend_str = ""
        name_dict['transactions_number'] = "N/A" #id_dict[user_id]
        name_dict['friend'] = friend_str
        name_list.append(name_dict)

    return name_list
