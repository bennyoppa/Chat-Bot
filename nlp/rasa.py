import random
import logging
import wikipedia

##pip install rasa_nlu scipy scikit-learn sklearn-crfsuite numpy spacy wikipedia

from rasa_nlu.converters import load_data
##pip install rasa-nlu==0.11.5

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer, Metadata, Interpreter
from rasa_nlu.components import ComponentBuilder





class RasaNLP(object):
    COULD_NOT_PARSE_MSGS = [
        'Sorry, I don\'t know it',
        'Next time I will know, but not now',
        'Sorry, can\'t get what do you mean',
        'Try something else'
    ]
    GREET_MSGS = ['Hola!', 'Privet!', 'Xin chào!']
    INTENT_GREET = 'greet'

    # intent: table names, table to search 
    INTENTS = ['course', 'staff']

    # entity: keywords
    ENTITY_DET = 'd'
    ENTITY_NDET = 'nd'
    ENTITY_KEY = 'key'
    ENTITY_ATT = 'att'

    def __init__(self, config_file, data_file, model_dir):
        # record the current subject for follow questions
        self.subject = None

        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

        # store unparsed messages, so later we can train bot
        self.unparsed_messages = []

        self.data_file = data_file
        self.model_dir = model_dir
        self.rasa_config = RasaNLUConfig(config_file)

    def train(self):
        training_data = load_data(self.data_file)
        trainer = Trainer(self.rasa_config)
        trainer.train(training_data)

        self.interpreter = Interpreter.load(trainer.persist(self.model_dir), self.rasa_config)

        logging.info('rasa trained successfully')

    def parse(self, msg):
        return self.interpreter.parse(msg)

    def find_reply(self, msg):
        res = self.parse(msg)
        logging.info('rasa parse res: {}'.format(res))

        if not 'intent' in res or res['intent'] is None:
            # later we can do something with unparsed messages, probably train bot
            self.unparsed_messages.append(msg)
            return random.choice(self.COULD_NOT_PARSE_MSGS)

        if res['intent']['name'] == self.INTENT_GREET:
            return random.choice(self.GREET_MSGS)




        # same approach for all questions
        if res['intent']['name'] in self.INTENTS and len(res['entities']) > 0:


            deterministic = False
            # to locate entry
            key = []
            # to retrieve info
            att = []

            
            for e in res['entities']:
                if e['entity'] == self.ENTITY_DET:
                    deterministic = True
                elif e['entity'] == self.ENTITY_ATT:
                    att += [e['value']]
                elif e['entity'] == self.ENTITY_KEY:
                    key += [e['value']]

            return True, [deterministic, res['intent']['name'], key, att]










        self.unparsed_messages.append(msg)
        return random.choice(self.COULD_NOT_PARSE_MSGS)


    # {table name: key word}, desired att
    def get_short_answer(self, table_key, att):
        print('table name and desired key word:', table_key, '\ndesired attribute:', att)

    # saves unparsed messages into a file
    def snapshot_unparsed_messages(self, filename):
        with open(filename, 'a') as f:
            for msg in self.unparsed_messages:
                f.write('{}\n'.format(msg))




##r = RasaNLP('../rasa-config.json', '../rasa-data.json', '../rasa-model')
##
##r.train()
##
##print(r.find_reply('Who is the tutor of COMP9417?'))
##res = r.parse('Who is the LiC of COMP9417?')
##print(res)
