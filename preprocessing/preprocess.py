#### This script is to convert q-a file into rasa format.

import json
import os
import re
from copy import deepcopy

### The stop words is to remove useless words in training
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
                  'yourselves', 'then', 'that', 'because',  'over',
                  'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
                  'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
                  'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being',
                  'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it',
                   'further', 'was', 'here', 'than', 'in', "", "/*", "*/" })

### read json file
def read_json(read_file):
	with open(read_file, 'r') as load_f:

		load_list = json.load(load_f)
	return load_list

### write json file
def write_json(write_file, new_dict):
	with open(write_file,'w') as write_f:
		json.dump(new_dict, write_f, indent = 1)

### create rasa style json format
def create_rasa_format(topic, key_words, rasa_dict, format_each):
	inner_list = rasa_dict["rasa_nlu_data"]["common_examples"]
	
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

				if "comp" in j:
					format_each_keywords["entity"] = "course"
				elif "week" in j:
					format_each_keywords["entity"] = "time"
				elif "example" in j:
					format_each_keywords["entity"] = "example"
				elif "solution" in j:
					format_each_keywords["entity"] = "solution"
				elif "exercise" in j:
					format_each_keywords["entity"] = "exercise"
				else:
					format_each_keywords["entity"] = "knowledge"

				format_each["entities"].append(format_each_keywords)
				format_each = deepcopy(format_each)
			if 'week' not in sentence:
				if 'week ' in i:
					format_each_keywords["value"] = i
					format_each_keywords["entity"] = "time"
					format_each_keywords["start"] = 100
					format_each_keywords["end"] = 106
					format_each["entities"].append(format_each_keywords)
					format_each = deepcopy(format_each)

	inner_list.append(format_each)

	return rasa_dict

def create_rasa_format_inform(topic, key_words, rasa_dict, format_each):
	inner_list = rasa_dict["rasa_nlu_data"]["common_examples"]
	
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

				if "comp" in j:
					format_each_keywords["entity"] = "course"
				elif "week" in j:
					format_each_keywords["entity"] = "time"

				else:
					format_each_keywords["entity"] = "knowledge"

				format_each["entities"].append(format_each_keywords)
				format_each = deepcopy(format_each)


	inner_list.append(format_each)

	return rasa_dict

#### read q-a json file and write in rasa style json file
path1 = 'optimize_data'
path_list1=os.listdir(path1)

new_json = []

for i in range(len(path_list1)):
	path = path1 + '/' + path_list1[i]
	path_list = os.listdir(path)
	print(path_list)
	for j in range(0, len(path_list)):
		path_json_file = path + '/' + path_list[j]
		print(path_json_file)
		load_list = read_json(path_json_file)

		rasa_dict = {"rasa_nlu_data": {"common_examples": []}}
		for k in range(len(load_list)):
			topic = load_list[k]['question']
			

			key_words = load_list[k]['key_words']
			intent_rasa = load_list[k]['intent']
			
			format_each = {"text": topic, "intent": intent_rasa, "entities": []}
			if intent_rasa != 'inform':
				a = create_rasa_format(topic, key_words, rasa_dict, format_each)
			else:
				a = create_rasa_format_inform(topic, key_words, rasa_dict, format_each)

		new_json = a["rasa_nlu_data"]["common_examples"] + new_json	



write_file = 'preprocessed_data/preprocessed.json'
rasa_dict_pro = {"rasa_nlu_data": {"common_examples": []}}
rasa_dict_pro["rasa_nlu_data"]["common_examples"] = new_json
write_json(write_file, rasa_dict_pro)


		

