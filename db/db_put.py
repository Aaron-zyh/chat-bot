# Easily put json file into mongodb
# By Yuanhai Zhang
from pymongo import MongoClient
import os
import json
client = MongoClient('ec2-3-104-117-103.ap-southeast-2.compute.amazonaws.com', 27017)

# one coure one database
# set the name of database be the name of course e.g.: comp9315
db_name = 'comp9315'

# if db not exist, will automatically create it 
db = client[db_name]
# existing db list
db_list = client.list_database_names()

data_dir = '/home/aaron/chat-bot/capstone-project-teaml/data_preprocess_tool/data_preprocessing_modular/data_preprocessed'
file_list = os.listdir(data_dir)
for i in range(0,len(file_list)):
    collection_name = '' + file_list[i].rstrip('.json')
    # print(collection_name)
    
    path = os.path.join(data_dir,file_list[i])

    if os.path.isfile(path) and ('.json' in str(file_list[i])) :
        #print(file_list[i],path)
        collit = db.list_collection_names()
        print(collit)
        if collection_name not in collit:
            db.create_collection(collection_name)
        collection = db[collection_name]
        with open(path) as template:
            template_dct = json.load(template)
            #print (template_dct)
            result = collection.insert_many(template_dct)
        print("SUccess &s",result)



