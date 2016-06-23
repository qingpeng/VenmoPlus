from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
import requests
from . import config
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()

class Search(Resource):
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
		  

api.add_resource(Search, config.api_base_url+'/search')

