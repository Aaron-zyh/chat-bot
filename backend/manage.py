#! /usr/bin/env python3

from flask import Flask,request,jsonify, make_response
import json
import nltk
import re

## rasa core related
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig

stop_words = set({'ourselves', 'hers', 'between', 'yourself', 'again',
                  'there', 'once', 'during', 'out', 
                  'with', 'they', 'own', 'an', 'be', 'for', 'do', 'its',
                  'yours', 'such', 'into', 'of', 'itself', 
                  'off', 's', 'am', 'as', 'from', 'him',
                  'each', 'the', 'themselves', 'below',  
                  'these', 'your', 'his', 'through', 'don', 'me', 'were',
                  'her', 'more', 'himself', 'down', 'should', 'our',
                  'their', 'above', 'both', 'up', 'to', 'ours', 'had',
                  'she', 'all',  'at', 'any', 'before', 'them',
                  'same', 'been', 'have', 'will', 'on', 'does',
                  'yourselves', 'then', 'because',  'over',
                   'so', 'did', 'now', 'under', 'he', 
                  'herself', 'has', 'just', 'too', 'only', 'myself',
                  'those', 'after', 'few', 't', 'being',
                  'if', 'theirs', 'my', 'against', 'a', 'by', 'doing',
                   'further', 'was', 'here', 'than', "", "/*", "*/" })


app = Flask(__name__)
#loading the rasa core before first request
@app.before_first_request
def load_rasa_agent():
      ## path should be changed
    interpreter = RasaNLUInterpreter("./rasa/models/nlu/default/chatbot")
    action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
    app.rasa_agent = Agent.load("./rasa/models/dialogue",
        interpreter=interpreter,action_endpoint=action_endpoint)
    
    # lemma used to preprocess the input
    app.lemma = nltk.wordnet.WordNetLemmatizer()


#route address at api/test/
@app.route('/test/', methods=['POST'])
def test_post():

    postData = request.form
    data = request.form.get("data")
    print('POST DATA：',postData,data) # print POST DATA received
    data = eval(data)
    response = ''
    # preprocessed data before put into rasa
    lemma = app.lemma
    data = re.sub('\s\s*',' ',data)
    list_data = data.split(' ')
    

    list_data = [lemma.lemmatize(str.lower(w)) for w in list_data]
    new_list_data = []
    for w in list_data:
        if w not in stop_words:
            new_list_data.append(w)
    data = (' ').join(new_list_data)

    # handle by rasa
    ret = app.rasa_agent.handle_text(data)
    for msg in ret:
        print(msg)
    
    # combine the response from rasa into one message
    for msg in ret:
        response += msg['text']
        response += '\n'

    #print (response)

    
    #jsonify response and send back
    rst = make_response(jsonify(response))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    
    return rst,201

## application is running at "localhost:7001" defaultly
if __name__ == '__main__':
    # manualy trigger load_rasa_agent()
    app.try_trigger_before_first_request_functions()
    app.run(debug=True,host = 'localhost',port = 7001)



