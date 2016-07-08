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
