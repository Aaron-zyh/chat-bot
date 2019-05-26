from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
import nltk

from lib.search import Search

class Action_description(Action):
    def name(self):
      # type: () -> Text
      # return "action_chatbot"
      return "action_description"

    def run(self, dispatcher, tracker, domain):
      
      
      lemma = nltk.wordnet.WordNetLemmatizer()
      Operations = []

      # for debugging
      print("action_name:",self.name())
      latest_message = ("description//latest_message:",tracker.latest_message)
      print(latest_message)
      
      print(tracker.current_state)

      # get what you need from slots
      course = tracker.get_slot("course")
      knowledge = tracker.get_slot("knowledges")
      # get what you need from user_input if not exist in slot
      # if slot exists in the latest msg, it will be autofilled in slotList. 
      # returnType: tracker.get_latest_entity_values() -> Object<generator> : next( ) or list( )
      course = list(tracker.get_latest_entity_values("course")) if not course else course
      knowledge = list(tracker.get_latest_entity_values("knowledge")) if not knowledge else knowledge
      
      # preprocess input data from users
      if course:
        course = str(course).lower()
      if knowledge:
        knowledge = [lemma.lemmatize(str.lower(key)) for key in knowledge]

      # If all required info has been stored in slot_set -> respond to question
      # otherwise -> send message for requesting what missed.
      if not (course and knowledge):
        # sending msg
        message = "Can you provide the course code of that knowledge?(e.g compXXXX)" if not course else "About what(description)?"
        dispatcher.utter_message(message) 
        # setting slot
        if course:
          Operations.append(SlotSet('course', course))
        if knowledge:
          Operations.append(SlotSet('knowledges', knowledge))
        
      if course and knowledge:
        #search infomation in db
        search = Search()

        if course in search.db_list:
          # search by keywords extracted by NLU
          data = search._search_by_key(db_name=course,key=knowledge)
          # if data matched is not exist, return message 'Nothing matched'
          # then reset solt
          if not len(data):
            dispatcher.utter_message("Nothing matched :(")
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
          # matched data found -> excuting searching function
          #                    -> compute idf
          #                    -> ranking outcome
          #                    -> return outcome
          else:
            sim, index = search.tf_idf(knowledge,data)
            title = None
            time = None
            num_key = 1
            for i in index:
              if ((not title) or title != data[i][2])and((not time) or time != data[i][0] ):
                ans_from = f'I got you something in {data[i][0]} about {data[i][2]}:'
                title = data[i][2]
                time = data[i][0]
                dispatcher.utter_message(str(num_key))
                dispatcher.utter_message(ans_from)
                num_key +=1
              dispatcher.utter_message(data[i][1])
              print(i,data[i])
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
        
        if course not in search.db_list:
          dispatcher.utter_message("Sorry.. I can't find course ")
          dispatcher.utter_message("Is that what you want? (Yes/No)")
          Operations.append(SlotSet('course', None))
      
      return Operations

class Action_solution(Action):

    def name(self):
      # type: () -> Text
      return "action_solution"
    def run(self, dispatcher, tracker, domain):
      lemma = nltk.wordnet.WordNetLemmatizer()
      Operations = []

      # for debugging
      print("action_name:",self.name())
      latest_message = ("solution//latest_message:",tracker.latest_message)
      print(latest_message)
      
      print(tracker.current_state)

      # get what you need from slots
      course = tracker.get_slot("course")
      knowledge = tracker.get_slot("knowledges")
      # get what you need from user_input if not exist in slot
      # if slot exists in the latest msg, it will be autofilled in slotList. 
      # returnType: tracker.get_latest_entity_values() -> Object<generator> : next( ) or list( )
      course = list(tracker.get_latest_entity_values("course")) if not course else course
      knowledge = list(tracker.get_latest_entity_values("knowledge")) if not knowledge else knowledge
      
      # preprocess
      if course:
        course = str(course).lower()
      if knowledge:
        knowledge = [lemma.lemmatize(str.lower(key)) for key in knowledge]

      # If all required info has been stored in slot_set -> respond to question
      # otherwise -> send message for requesting what missed.
      if not (course and knowledge):
        # sending msg
        message = "Can you provide the course code of that knowledge?(e.g compXXXX)" if not course else "About what(solution)?"
        dispatcher.utter_message(message) 
        # setting slot
        if course:
          Operations.append(SlotSet('course', course))
        if knowledge:
          Operations.append(SlotSet('knowledges', knowledge))
        
      if course and knowledge:
        #search infomation in db
        search = Search()
        # searching courses 
        if course in search.db_list:
          # search by keywords
          data = search._search_by_key(db_name=course,key=knowledge)
          if not len(data):
            dispatcher.utter_message("Nothing matched :(")
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
          else:
            # matched data found -> excuting searching function
            #                    -> compute idf
            #                    -> ranking outcome
            #                    -> return outcome
            sim, index = search.tf_idf(knowledge,data)
            title = None
            time = None
            num_key = 1

            for i in index:
              if ((not title) or title != data[i][2])and((not time) or time != data[i][0] ):
                ans_from = f'I got you something in {data[i][0]} about {data[i][2]}:'
                title = data[i][2]
                time = data[i][0]
                dispatcher.utter_message(str(num_key))
                dispatcher.utter_message(ans_from)
                num_key +=1
              dispatcher.utter_message(data[i][1])
            
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
        
        if course not in search.db_list:
          dispatcher.utter_message("Sorry.. I can't find course ")
          dispatcher.utter_message("Is that what you want? (Yes/No)")
          Operations.append(SlotSet('course', None))
      return Operations

class Action_exercise(Action):

    def name(self):
      # type: () -> Text
      return "action_exercise"

    def run(self, dispatcher, tracker, domain):
      
      lemma = nltk.wordnet.WordNetLemmatizer()
      Operations = []
      # get what you need from slots
      course    = tracker.get_slot("course")
      knowledge = tracker.get_slot("knowledges")
      time      = tracker.get_slot("time")

      # for debugging
      print("action_name:",self.name())
      latest_message = ("exercise//latest_message:",tracker.latest_message)
      print(latest_message)
      # get what you need from user_input if not exist in slot
      # if slot exists in the latest msg, it will be autofilled in slotList. 
      # returnType: tracker.get_latest_entity_values() -> Object<generator> : next( ) or list( )
      course = list(tracker.get_latest_entity_values("course")) if not course else course
      knowledge = list(tracker.get_latest_entity_values("knowledge")) if not knowledge else knowledge
      time = list(tracker.get_latest_entity_values("time")) if not time else time
      
      # preprocess
      if course:
        course = str(course).lower()
      if knowledge:
        knowledge = [lemma.lemmatize(str.lower(key)) for key in knowledge]
        if 'exercise' in knowledge:
          knowledge.remove("exercise")
      if time:
        time = str(time).lower()
        time = time.replace(' ','0')
        time=time.strip('[').strip(']')
      print('time: ', time)
      print('knowledge: ', knowledge)
      # If all required info has been stored in slot_set -> respond to question
      # otherwise -> send message for requesting what missed.
      if not (course and (knowledge or time)):
        # sending msg
        message = "Can you provide the course code of that knowledge?(e.g compXXXX)" if not course else "About what or time of lecture(e.g week 2)?"
        dispatcher.utter_message(message) 

        # setting slot
        if course:
          Operations.append(SlotSet('course', course))
        if knowledge:
          Operations.append(SlotSet('knowledges', knowledge))
        
      if course and (knowledge or time):
        #retrieval info in DB
        search = Search()

        if course in search.db_list:
          # search method need imporvement for this: searhing exercises by knowledge or by time.

          print("time:",time)
          if knowledge:
            # search by keywords(compulsory) and time(optional)
            data = search._search_by_key(db_name=course,key=knowledge,intent='exercise',time=time)
          else:
            # search by time(compulsory) if no keywords provided
            data = search._search_by_time(db_name=course,intent='exercise',time=time)
          
          # matched data found -> excuting searching function
          #                    -> compute idf
          #                    -> ranking outcome
          #                    -> return outcome
          if not len(data):
            dispatcher.utter_message("Nothing matched :(")
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
          else:
            sim, index = search.tf_idf(knowledge,data)
            if not knowledge:
              ans_from = f'Here is all the exercises in {time}:'
              dispatcher.utter_message(ans_from)
            time = None
            title = None
            num_key = 1
            for i in index:
              if  ((not title) or title != data[i][2]) and ((not time) or time != data[i][1]):
                ans_from = f'I got you exercises in {data[i][0]} about {data[i][2]}:'
                title = data[i][2]
                time = data[i][1]
                dispatcher.utter_message(str(num_key))
                dispatcher.utter_message(ans_from)
                num_key +=1
              dispatcher.utter_message(data[i][1])
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
        
        if course not in search.db_list:
          dispatcher.utter_message("Sorry.. I can't find course ")
          dispatcher.utter_message("Is that what you want? (Yes/No)")
          Operations.append(SlotSet('course', None))    
      return Operations

class Action_example(Action):

    def name(self):
      # type: () -> Text
      return "action_example"
    def run(self, dispatcher, tracker, domain):
      
      lemma = nltk.wordnet.WordNetLemmatizer()
      Operations = []
      # get what you need from slots
      course    = tracker.get_slot("course")
      knowledge = tracker.get_slot("knowledges")
      time      = tracker.get_slot("time")

      # for debugging
      print("action_name:",self.name())
      latest_message = ("example//latest_message:",tracker.latest_message)
      print(latest_message)
      # get what you need from user_input if not exist in slot
      # if slot exists in the latest msg, it will be autofilled in slotList. 
      # returnType: tracker.get_latest_entity_values() -> Object<generator> : next( ) or list( )
      course = list(tracker.get_latest_entity_values("course")) if not course else course
      knowledge = list(tracker.get_latest_entity_values("knowledge")) if not knowledge else knowledge
      time = list(tracker.get_latest_entity_values("time")) if not time else time
      
      # preprocess
      if course:
        course = str(course).lower()
      if knowledge:
        knowledge = [lemma.lemmatize(str.lower(key)) for key in knowledge]
        if 'exercise' in knowledge:
          knowledge.remove("exercise")
      if time:
        time = str(time).lower()
        time = time.replace(' ','0')
        time=time.strip('[').strip(']')
      print('time: ', time)
      print('knowledge: ', knowledge)
      # If all required info has been stored in slot_set -> respond to question
      # otherwise -> send message for requesting what missed.
      if not (course and (knowledge or time)):
        # sending msg
        message = "Can you provide the course code of that knowledge?(e.g compXXXX)" if not course else "About what or time of lecture(e.g week 2)?"
        dispatcher.utter_message(message) 

        # setting slot
        if course:
          Operations.append(SlotSet('course', course))
        if knowledge:
          Operations.append(SlotSet('knowledges', knowledge))
        
      if course and (knowledge or time):
        #retrieval info in DB
        search = Search()

        if course in search.db_list:
          # search method need imporvement for this: searhing exercises by knowledge or by time.

          print("time:",time)
          if knowledge:
            data = search._search_by_key(db_name=course,key=knowledge,intent='example',time=time)
          else:
            data = search._search_by_time(db_name=course,intent='example',time=time)

          if not len(data):
            dispatcher.utter_message("Nothing matched :(")
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
          else:
            sim, index = search.tf_idf(knowledge,data)
            if not knowledge:
              ans_from = f'Here is all the examples in {time}:'
              dispatcher.utter_message(ans_from)
            title = None
            time = None            
            num_key = 1
            for i in index:
              if ((not title) or title != data[i][2]) and ((not time ) or time != data[i][1]):
                ans_from = f'I got you examples in {data[i][0]} about {data[i][2]}:'
                title = data[i][2]
                time = data[i][1]
                dispatcher.utter_message(str(num_key))
                dispatcher.utter_message(ans_from)
                num_key +=1
              dispatcher.utter_message(data[i][1])
            dispatcher.utter_message("Is that what you want? (Yes/No)")
            Operations.append(SlotSet('knowledges', None))
            Operations.append(SlotSet('time', None))
        
        if course not in search.db_list:
          dispatcher.utter_message("Sorry.. I can't find course ")
          dispatcher.utter_message("Is that what you want? (Yes/No)")
          Operations.append(SlotSet('course', None))    
      return Operations