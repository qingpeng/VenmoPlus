# To build API, working with helper.py
#

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

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


parser = reqparse.RequestParser()

# API for list relavant user names and list of their friends
class User(Resource):
	def get(self):
		print ("Call for GET /user")
		parser.add_argument('q')
		query_string = parser.parse_args()
	#	url = config.es_base_url['venmo']+'/_user'
		name = query_string['q']
		names = list_user(name)
		return names		

# API for friend recommender
class Friend(Resource):
	def get(self):
		print ("Call for GET /friend")
		parser.add_argument('q')
		query_string = parser.parse_args()
	#	url = config.es_base_url['venmo']+'/_user'
		user_id = query_string['q']
		friends_list = friend_recommend(r0,r1,user_id) 
		return friends_list		

# API for searching transactions in friend circle
class Message(Resource):
	def get(self):
		print ("Call for GET /message")
		parser.add_argument('q')
		parser.add_argument('m')
		query_string = parser.parse_args()
	#	url = config.es_base_url['venmo']+'/_user'
		user_id = query_string['q']
		message = query_string['m']
		transactions = search_message_in_circle(message,user_id,1)
		return transactions		

# API for getting name for a user ID
class Name(Resource):
    def get(self):
        print ("Call for GET /name")
        parser.add_argument('q')
        query_string = parser.parse_args()
        user_id = query_string['q']
        name = get_name(user_id)
        return name

# API for getting the list of friends for a user
class List(Resource):
    def get(self):
        print ("Call for GET /list")
        parser.add_argument('q')
        query_string = parser.parse_args()
        user_id = query_string['q']
        friend_list = get_friend_list(user_id)
        return friend_list



# API for getting the recent transactions
class Search(Resource):
    def get(self):
	print ("Call for GET /search")
	parser.add_argument('q')
	query_string = parser.parse_args()
        user_id = query_string['q']
        transactions = get_recent_transactions(user_id)
        return transactions
		  

api.add_resource(Search, config.api_base_url+'/search')
api.add_resource(User, config.api_base_url+'/user')
api.add_resource(Friend, config.api_base_url+'/friend')
api.add_resource(Message, config.api_base_url+'/message')
api.add_resource(List, config.api_base_url+'/list')
api.add_resource(Name, config.api_base_url+'/name')


