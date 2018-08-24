from nlp.rasa import RasaNLP
from db.retrieve_info import get_course_info


q = 'Who is the pre_requisite of COMP9417?'


#  train the nlp model
nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')
nlp.train()


# parse query
res = nlp.find_reply(q)
need_reply, [deter, table, [keyword], att] = res


# get the answer
answer = get_course_info(table, (keyword).upper(), att)

