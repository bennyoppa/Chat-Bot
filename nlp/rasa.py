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
    COULD_NOT_PARSE_MSGS = ['Sorry, I don\'t understand your question, can you please ask in another way?',
                            'Sorry, I don\'t understand your query, can you please try it in a different way?',
                            
                            ]

    NO_RECORD = ['Sorry, I could not find what you are looking for',
                 'Sorry, there is no record found in my database for your question',
                 ]
    
    INTENT_GREET1 = 'greet1'
    GREET_MSGS1 = ['Hello.', 'Hi.', 'Hey.', 'Hihi.']

    INTENT_GREET2 = 'greet2'
    GREET_MSGS2 = [
        'Fine, thank you, how may I help you.',
        'Pretty good, thank you for asking, how may I help you.'
        ]

    INTENT_GREET3 = 'greet3'
    GREET_MSGS3 = [
        'You are welcome.',
        'No worries at all',
        ]

##    INTENT_SELF = 'self'
    SELF_MSG = ['My name is Uri. I am an intelligent chatting robot and can answer CSE enrolment related questions.']

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

    # combined querys, two tables to search
    COMBINED_INTENT = 'combined'
    # table to search first
    ENTITY_KEY1 = 'key1'
    # second table to search
    ENTITY_KEY2 = 'key2'

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
            self.uned_messages.append(msg)
            return random.choice(self.COULD_NOT_PARSE_MSGS)

        if res['intent']['name'] == self.INTENT_GREET1:
            return random.choice(self.GREET_MSGS1)

        if res['intent']['name'] == self.INTENT_GREET2:
            return random.choice(self.GREET_MSGS2)

        if res['intent']['name'] == self.INTENT_GREET3:
            return random.choice(self.GREET_MSGS3)
        
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


        if res['intent']['name'] in self.COMBINED_INTENT:
            deterministic = False
            # to locate entry
            key1 = []
            key2 = []
            # to retrieve info
            att = []

            for e in res['entities']:
                if e['entity'] == self.ENTITY_DET:
                    deterministic = True
                elif e['entity'] == self.ENTITY_ATT:
                    att += [e['value']]
                elif e['entity'] == self.ENTITY_KEY1:
                    key1 += [e['value']]
                elif e['entity'] == self.ENTITY_KEY2:
                    key2 += [e['value']]

            return deterministic, 'staff', get_info('course', key1, key2), att



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
        _answers = ['Sure, this is what I found:\n',
                    'OK, I found this:\n',
                    'Not a problem.\n',
                    'No problem at all.\n',
                    'Sure, I can do this.\n',
                    '',
                    '',
                    '',
                    ]



        parsed_query = self._reply(msg)
        # used to construct answers to queries related to stream questions
        stream = ['number', 'electives']

        if type(parsed_query) is tuple:
            # need_reply,[]
            deter, table, keyword, att = parsed_query


            # replace 'contact' in att for staff table
            try:
                idx = att.index('contact')
                att[idx:idx+1] = ('email', 'phone')
            except:
                pass



            try:
                info_list = get_info(table, keyword, att)
            except:
                # parsed into undesired format
                self.unparsed_messages.append(msg)
                return random.choice(self.COULD_NOT_PARSE_MSGS)

            if not any(info_list):
                # no record in DB
                self.unparsed_messages.append(msg)
                return random.choice(self.NO_RECORD)
            
##            answer = random.choice(_answers)
            answer = '\n'

            for index in range(len(keyword)):
                key = keyword[index]
                info = info_list[index]

                if not any(info):
                    if not deter:
                        answer += key + ': \n\tNo record found\n'
                    else:
                        answer += key + ': No record found\n'
                    continue

                if table == 'course':
                    
                    if not deter:
                        answer += key.upper() + ':\n'
                        for i in info:
                            answer += '\t' + i + ': ' + str(info[i]) + '\n'

                    else:
                        answer += key
                        for i in info:
                            if info[i]:
                                answer += ' is ' + i + ','
                            else:
                                answer += ' is not ' + i + ','

                        answer = answer[:-1] + '.' + '\n'

                    
                elif table == 'stream':
                    answer += key.upper()

                    if True in info:
                        # meet the requirement
                        answer += ': you are eligible to declare this stream, congratulations!\n'
                        continue
                    else:
                        answer += ':\n\tPlease choose'

                        
                    for i in range(len(info)):
                        if i > 0:
                            answer += '\n\tAnd'
                        answer += ' ' + str(info[i][stream[0]]) + ' subjects from below:\n\t\t' \
                                  + '\n\t\t'.join(info[i][stream[1]])
                    answer += '\n'

                elif table == 'staff':
                    answer += key + ':\n'
                    for i in info:
                        if info[i] == 'N/A':
                            answer += '\t' + i + ': No record' + '\n'
                        else:
                            if isinstance(info[i], list):
                                answer += '\t' + i + ': ' + ' and '.join(info[i]) + '\n'
                            else:
                                answer += '\t' + i + ': ' + info[i] + '\n'


            return answer[:-1]
        
        return parsed_query


    # saves unparsed messages into a file
    def snapshot_unparsed_messages(self, filename):
        with open(filename, 'a') as f:
            for msg in self.unparsed_messages:
                f.write('{}\n'.format(msg))




