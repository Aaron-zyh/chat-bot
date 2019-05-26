### This file is to train nlu model and run & test the model

from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

def train_nlu(data, configs, model_dir):
	training_data = load_data(data)
	trainer = Trainer(config.load(configs))
	trainer.train(training_data)
	model_directory = trainer.persist(model_dir, fixed_model_name = 'chatbot')
	
def run_nlu():
	interpreter = Interpreter.load('./models/nlu/default/chatbot')
	print(interpreter.parse(u"what is exercise about query cost"))
	
if __name__ == '__main__':
	train_nlu('data/preprocessed.json', 'config_spacy.json', './models/nlu')
	run_nlu()