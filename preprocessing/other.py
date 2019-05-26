### this file is to reply thanks, deny intents in json file

import json
import os

path_input_file = 'other.json'
with open(path_input_file, 'r') as loadf:
	load_list = json.load(loadf)
G = []
for i in range(0, 120):
	G = G + load_list
def write_json(write_file, new_dict):
	with open(write_file,'w') as write_f:
		json.dump(new_dict, write_f, indent = 1)
write_json('other_new.json', G)
