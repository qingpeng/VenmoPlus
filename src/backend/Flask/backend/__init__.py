from flask import Flask
from flask_restful import reqparse, Resource, Api
import flask_cors
from flask_cors import CORS
#from flask.ext.cors import CORS
import requests
from . import config
import json
from . import helper
from helper import *

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()

class User(Resource):
	def get(self):
		print ("Call for GET /user")
		parser.add_argument('q')
		query_string = parser.parse_args()
	#	url = config.es_base_url['venmo']+'/_user'
		name = query_string['q']
		names = list_user(name)
		return names		

class Friend(Resource):
	def get(self):
		print ("Call for GET /friend")
		parser.add_argument('q')
		query_string = parser.parse_args()
	#	url = config.es_base_url['venmo']+'/_user'
		user_id = query_string['q']
		friends_list = friend_recommend(r0,r1,user_id) 
		return friends_list		

class Message(Resource):
	def get(self):
		print ("Call for GET /message")
		parser.add_argument('q')
		parser.add_argument('m')
		query_string = parser.parse_args()
	#	url = config.es_base_url['venmo']+'/_user'
		user_id = query_string['q']
		message = query_string['m']
		transactions = search_message_in_circle(message,user_id,2)
		return transactions		



class Search(Resource):
    def get(self):
	print ("Call for GET /search")
	parser.add_argument('q')
	query_string = parser.parse_args()
	url = config.es_base_url['venmo']+'/_search'
	query = {
	    "size":50, 
	       "query" : {
		  "constant_score" : { 
		     "filter" : {
			"bool" : {
			  "should" : [
			     { "term" : {"actor.id" : query_string['q']}}, 
			     { "term" : {"transactions.target.id" : query_string['q']}} 
			  ]
			  }
		       }
		     }
		  },
		  "sort": { "created_time": { "order": "desc" }}
	}
	resp = requests.post(url, data=json.dumps(query))
	data = resp.json()
	transactions = []
	for hit in data['hits']['hits']:
	
		payment_id = hit['_source']['payment_id']
		time = hit['_source']['updated_time']
		message = hit['_source']['message']
		actor_id = hit['_source']['actor']['id']
		actor_name = hit['_source']['actor']['name']
		target_id = hit['_source']['transactions'][0]['target']['id']
		target_name = hit['_source']['transactions'][0]['target']['name']
		transaction = hit['_source']
		transaction['distance'] =  get_distance(r0,actor_id,target_id,time) # add time stamp
		transaction['actor_name'] = actor_name
		transaction['target_name'] = target_name
	
 		transactions.append(transaction)	
	#	transactions.append([payment_id, time,message,actor_id,actor_name,target_id,target_name,distance])
	return transactions
		  

api.add_resource(Search, config.api_base_url+'/search')
api.add_resource(User, config.api_base_url+'/user')
api.add_resource(Friend, config.api_base_url+'/friend')
api.add_resource(Message, config.api_base_url+'/message')




