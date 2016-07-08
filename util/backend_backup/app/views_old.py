#changes are highlighted in blue

from flask import jsonify
#jsonify creates a json representation of the response

from app import app
from cassandra.cluster import Cluster
#importing Cassandra modules from the driver we just installed

# setting up connections to cassandra
cluster = Cluster(['ec2-52-40-166-123.us-west-2.compute.amazonaws.com'])
#change the bolded text to your seed node public dns (no < or > symbols but keep quotations. Be careful to copy quotations as it might copy it as a special character and throw an error. Just delete the quotations and type them in and it should be fine.
session = cluster.connect('venmo_streaming')

@app.route('/')
@app.route('/index')
def index():
  return "Hello, World!"

@app.route('/api/<key>')
def pick(key):
       stmt = "SELECT * FROM transaction_degree WHERE message=%s ALLOW FILTERING"
       response = session.execute(stmt, parameters=[key])
       print response
       response_list = []
       for val in response:
            response_list.append(val)
       jsonresponse = [{"payment_id": x.payment_id, "message": x.message, "actor_id":x.actor_id,"target_id":x.target_id,"time":x.time} for x in response_list]
       return jsonify(transaction=jsonresponse)
