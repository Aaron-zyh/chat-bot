import json
import os
import re
from copy import deepcopy

stop_words = set({'ourselves', 'hers', 'between', 'yourself', 'again',
                  'there', 'about', 'once', 'during', 'out', 'very', 'having',
                  'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its',
                  'yours', 'such', 'into', 'of', 'most', 'itself', 'other',
                  'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
                  'each', 'the', 'themselves', 'below', 'are', 'we',
                  'these', 'your', 'his', 'through', 'don', 'me', 'were',
                  'her', 'more', 'himself', 'this', 'down', 'should', 'our',
                  'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had',
                  'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them',
                  'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
                  'yourselves', 'then', 'that', 'because', 'what', 'over',
                  'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
                  'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
                  'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being',
                  'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it',
                  'how', 'further', 'was', 'here', 'than', 'in', "", "/*", "*/" })

def read_json(read_file):
	with open('data/data_ques/'+read_file, 'r') as load_f:
		load_list = json.load(load_f)
	return load_list

def write_json(write_file, new_dict):
	with open(write_file,'w') as write_f:
		
		json.dump(new_dict, write_f, indent = 1)

def create_rasa_format(topic, key_words, rasa_dict):

	inner_list = rasa_dict["rasa_nlu_data"]["common_examples"]
	
	format_each = {"text": topic, "intent": "description", "entities": []}

	start = 0
	end = 0
	format_each_keywords = {"start": start, "end": end, "value": "", "entity": ""}
	for i in key_words:
		if i not in stop_words:
			sentence = str(topic)
			
			for m in re.finditer(i, sentence):
				start = m.start()
				end = start+len(i)
				
				format_each_keywords["start"] = start
				format_each_keywords["end"] = end
				format_each_keywords["value"] = i
				j = str(i)
				if "COMP" in j:
					format_each_keywords["entity"] = "course"
				else:
					format_each_keywords["entity"] = "knowledge"

				format_each["entities"].append(format_each_keywords)
				format_each = deepcopy(format_each)

	inner_list.append(format_each)

	return rasa_dict
			




path = 'data/data_ques'
path_list=os.listdir(path)
write_file = 'preprocessing_data/preprocessed.json'

new_json = []
for n_file in range(0, len(path_list)):

	read_file = path_list[n_file]

	#write_file = 'preprocessing_data/' + read_file
	
	load_list = read_json(read_file)

	rasa_dict = {"rasa_nlu_data": {"common_examples": []}}

	for i in range(len(load_list)):

		topic = load_list[i]["question"]
		key_words = load_list[i]["key_words"]

		a = create_rasa_format(topic, key_words, rasa_dict)

	new_json = a["rasa_nlu_data"]["common_examples"] + new_json
		
rasa_dict_pro = {"rasa_nlu_data": {"common_examples": []}}
rasa_dict_pro["rasa_nlu_data"]["common_examples"] = new_json
write_json(write_file, rasa_dict_pro)
	
	
	
