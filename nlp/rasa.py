import random
import logging
from db.retrieve_info import get_info

##pip install rasa_nlu scipy scikit-learn sklearn-crfsuite numpy spacy
##python -m spacy download en


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
    
    INTENT_GREET1 = 'greet1'
    GREET_MSGS1 = ['Hello.', 'Hi.', 'Hey.', 'Hihi.']

    INTENT_GREET2 = 'greet2'
    GREET_MSGS2 = [
        'Fine, thank you, how may I help you.',
        'Pretty good, thank you for asking, how may I help you.'
        ]

##    INTENT_SELF = 'self'
    SELF_MSG = ['My name is UNSW CSE Chat-Bot, I can answer CSE enrolment related questions.']

    INTENT_UNRELATED = 'unrelated'
    UNRELATED_MSG = ['Sorry, I can only answer questions related to CSE courses, streams and staff.']

##    INTENT_FUNC = 'function'
##    FUNC_MSG = ['I can provide course recommendation and information retrieval of CSE courses, streams and staff.']

    INTENT_CHALLENGE = 'challenge'
    CHALLENGE_MSG = ['I\'m able to assist you with CSE-related questions.']

    ENTITY_SELF = 'self'

    # intent: table names, table to search 

    # entity: keywords
    ENTITY_DET = 'd'
    ENTITY_NDET = 'nd'
    ENTITY_KEY = 'key'
    ENTITY_ATT = 'att'

    def __init__(self, config_file, data_file, model_dir, INTENTS = ['course', 'staff', 'stream']):
        # record the current subject for follow questions
        self.subject = None

        self.INTENTS = INTENTS
        
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

    def _reply(self, msg):
        res = self.parse(msg)
        logging.info('rasa parse res: {}'.format(res))

        if not 'intent' in res or res['intent'] is None:
            # later we can do something with unparsed messages, probably train bot
            self.unparsed_messages.append(msg)
            return random.choice(self.COULD_NOT_PARSE_MSGS)

        if res['intent']['name'] == self.INTENT_GREET1:
            return random.choice(self.GREET_MSGS1)

        if res['intent']['name'] == self.INTENT_GREET2:
            return random.choice(self.GREET_MSGS2)
        
##        if res['intent']['name'] == self.INTENT_SELF:
##            return random.choice(self.SELF_MSG)
        
        if res['intent']['name'] == self.INTENT_UNRELATED:
##            if not any(res['entities']):
##                return random.choice(self.UNRELATED_MSG)

            if self.ENTITY_SELF in [e['entity'] for e in res['entities']]:
                return random.choice(self.SELF_MSG)
            
            return random.choice(self.UNRELATED_MSG)
        
##        if res['intent']['name'] == self.INTENT_FUNC:
##            return random.choice(self.FUNC_MSG)
        
        if res['intent']['name'] == self.INTENT_CHALLENGE:
            return random.choice(self.CHALLENGE_MSG)




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

            if len(key):
                self.subject = key

            # need_reply,[]
            return deterministic, res['intent']['name'], self.subject, att










        self.unparsed_messages.append(msg)
        return random.choice(self.COULD_NOT_PARSE_MSGS)


    def reply(self, msg):
        
        '''
        takes RasaNLP parsed query as input
        outputs the answer string for user
        '''

        parsed_query = self._reply(msg)
        # used to construct answers to queries related to stream questions
        stream = ['number', 'electives']

        if type(parsed_query) is tuple:
            # need_reply,[]
            deter, table, keyword, att = parsed_query



            try:
                info_list = get_info(table, keyword, att)
            except:
                # parsed into undesired format
                self.unparsed_messages.append(msg)
                return random.choice(self.COULD_NOT_PARSE_MSGS)

            if not any(info_list):
                # no record in DB
                self.unparsed_messages.append(msg)
                return random.choice(self.COULD_NOT_PARSE_MSGS)
            
            answer = ''

            for index in range(len(keyword)):
                key = keyword[index]
                info = info_list[index]

                if table == 'course':
                    
                    if not deter:
                        answer += key.upper() + ':\n'
                        for i in info:
                            answer += '\t' + i + ': ' + info[i] + '\n'

                    else:
                        answer += key
                        for i in info:
                            if info[i]:
                                answer += ' is ' + i + ','
                            else:
                                answer += ' is not' + i + ','

                        answer = answer[:-1] + '.' + '\n'

                    
                elif table == 'stream':
                    answer += key.upper() + ':\n\tPlease choose'
                    for i in range(len(info)):
                        if i > 0:
                            answer += '\n\tAnd'
                        answer += ' ' + str(info[i][stream[0]]) + ' subjects from below:\n\t\t' \
                                  + '\n\t\t'.join(info[i][stream[1]])
                    answer += '\n'

            return answer[:-1]
        
        return parsed_query


    # saves unparsed messages into a file
    def snapshot_unparsed_messages(self, filename):
        with open(filename, 'a') as f:
            for msg in self.unparsed_messages:
                f.write('{}\n'.format(msg))




