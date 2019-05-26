from sklearn import feature_extraction
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer  
from pymongo import MongoClient
import configparser
import os 

class Search:
    # connecting mongoDB
    def __init__(self):
        print(os.getcwd())
        config = configparser.ConfigParser()
        config.read("./mongo_config.ini")
        mongo_url = config['MONGO']['mongo_url']
        port = config['MONGO']['port']
        self.client = MongoClient(mongo_url,int(port))
        self.db_list = self.client.list_database_names()

    # build query and send request to mongo
    def _search_by_key(self,db_name,key,intent= None,time = None):
        print("This is search by key")
        res = []
        db = self.client[db_name]
        collit = db.list_collection_names()
        filt = {"$or":[]}
        print("intent:",intent)
        print("time:",time)
        print("time_type:",type(time))
        # remove possible ' ' in key
        for i in range(len(key)): 
	        key[i] = key[i].replace(' ','')

        print('key:',key)
        for word in key:
            filt["$or"].append({"key_words": {"$regex":word,"$options":"i"}})
        if intent:
            new_filt = {"$and":[filt,{"intent_tag":intent}]}
            filt = new_filt
        print('filt',filt)
        for collection in collit:
            if time:
                if collection not in time:
                    continue
            print('Potential_collection_name:',collection)
            datas = db[collection].find(filt)
            for data in datas:
                res.append([collection,data['content'],data['key_words']])
        #print('res',res)
        return res
    
    # search by time if key_words value is not provided
    def _search_by_time(self,db_name,time,intent=None):
        print("This is search by time")
        res = []
        db = self.client[db_name]
        collit = db.list_collection_names()
        print("intent:",intent)
        print("time:",time)
        print("time_type:",type(time))
        filt = {"intent_tag":intent}
        print(filt)
        for collection in collit:
            if time:
                if collection not in time:
                    continue
            print('Potential_collection_name:',collection)
            datas = db[collection].find(filt)
            for data in datas:
                res.append([collection,data['content'],data['key_words']])
        return res

    # calculate the jaccard similarity
    def jaccard_sim(self,arr1,arr2):
        assert(len(arr1) == len(arr2))
        i = 0
        j = 0
        intersection = 0
        union = 0
        while i < len(arr1):
            if arr1[i] != 0 or arr2[j] != 0:
                union += 1
                if arr1[i] != 0 and arr2[j] != 0:
                    intersection += 1
            i += 1
            j += 1
        return float(intersection)/float(union)
    
    # return the top ranking 
    def tf_idf(self,knowledge,data):
        corpus = []
        corpus.append(' '.join(list(knowledge)))
        for d in data:
            corpus.append(' '.join(d[-1]))
        
        vectorizer = CountVectorizer() 

        X = vectorizer.fit_transform(corpus)

       
        word = vectorizer.get_feature_names()  
       

        counts =  X.toarray()

        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(X)
        #print(tfidf)
        #print(tfidf.toarray())

        tf_idf = tfidf.toarray()
        sim = []
        for i in range(1,len(tf_idf)):
            sim.append(self.jaccard_sim(tf_idf[0],tf_idf[i]))
        #print("sim:",sim)
        if sim:
            max_sim = max(sim)
            index = []
            for i in range(0,len(sim)):
                if sim[i] == max_sim:
                    index.append(i)
            return (max_sim,index)
        else:
            return(0,False)
