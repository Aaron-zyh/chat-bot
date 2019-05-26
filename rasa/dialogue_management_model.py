# libraries imported
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import rasa_core
from rasa_core.agent import Agent
from rasa_core.policies.fallback import FallbackPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig
from rasa_core.run import serve_application
from rasa_core import config


# training model
def train_dialogue(domain_file = 'chat_domain.yml',
					model_path = './models/dialogue',
					training_data_file = './data/stories.md'):
	print(training_data_file)

	#fall back policy initialized
	fallback = FallbackPolicy(fallback_action_name="action_default_fallback",
                          core_threshold=0.3,
                          nlu_threshold=0.3)
					
	agent = Agent(domain_file, policies = [MemoizationPolicy(), KerasPolicy(max_history=3, epochs=600, batch_size=50),fallback])
	# import training data
	data = agent.load_data(training_data_file)
	# generating diagram of story	
	agent.visualize("data/stories.md",
                output_file="graph.html", max_history=3)
	# start training
	agent.train(data)
				
	agent.persist(model_path)
	return agent

# function of running agent
def run_chatbot(serve_forever=True):
	interpreter = RasaNLUInterpreter('./models/nlu/default/chatbot')

	action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
	agent = Agent.load('./models/dialogue', interpreter=interpreter, action_endpoint=action_endpoint)
	rasa_core.run.serve_application(agent ,channel='cmdline')
		
	return agent

if __name__ == '__main__':
	train_dialogue()
	run_chatbot()