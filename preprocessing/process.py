### This script is to combine "week" and string of week number

import json
import os
import re
from copy import deepcopy

### read json file
def read_json(read_file):
	with open(read_file, 'r') as load_f:

		load_list = json.load(load_f)
	return load_list

### write json file
def write_json(write_file, new_dict):
	with open(write_file,'w') as write_f:
		json.dump(new_dict, write_f, indent = 1)


path = os.listdir('Archive')
print(path)


os.mkdir('qa_data/qa_inform_new')
os.mkdir('qa_data/data_exl_new')
os.mkdir('qa_data/data_ques_new')
os.mkdir('qa_data/data_sol_new')
os.mkdir('qa_data/data_exes_new')

### loop every file and combine 'week', string of number
for l in path:

	path_input_dir = 'qa_data' + '/' + l

	path_input_dir_list = os.listdir(path_input_dir)
	
	for i in range(len(path_input_dir_list)):
		path_json_file = path_input_dir + '/' + path_input_dir_list[i]

		load_list = read_json(path_json_file)

		for j in range(len(load_list)):
			key_words = load_list[j]['key_words']
			questions = load_list[j]['question']
			
			if 'week' in questions:
				for k in range(len(key_words)-1):
					if key_words[k] == 'week':
						if key_words[k+1].isdigit() == True:
							new_key = key_words[k] + ' ' + key_words[k+1]
							key_words.append(new_key)
								
							key_words.pop(k+1)
							key_words.pop(k)

		write_file = l + '_new' + '/' + path_input_dir_list[i]
		write_json(write_file, load_list)

	