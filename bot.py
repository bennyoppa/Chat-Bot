from nlp.rasa import RasaNLP
from db.retrieve_info import get_course_info


def reply(parsed_query):
    '''
    takes RasaNLP parsed query as input
    outputs the answer string for user
    '''
    need_reply, [deter, table, [keyword], att] = parsed_query
    if need_reply:
        answer = ''
        info = get_course_info(table, (keyword).upper(), att)
        if not deter:
            # non determinnistic answer
            for i in info:
                answer += info[i] + '\n'
        else:
            # determinnistic answer
            d = True
            if not info:
                '''
                change db to return False later instead of 'not found'
                '''
                # no record found
                answer = 'No.'
            else:
                for i in info:
                    d = d and info[i]
                    answer += i + ': ' + str(info[i]) + '\n'
                if d:
                    answer = 'Yes, ' + answer
                else:
                    answer = 'No, ' + answer

    return answer

q = 'What is the pre_requisite of COMP9417?'
q1 = 'Is COMP9417 an adk course?'


#  train the nlp model
nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')
nlp.train()


print(reply(nlp.find_reply(q)))

### parse query
##parsed_query = nlp.find_reply(q)
##need_reply, [deter, table, [keyword], att] = parsed_query
##
##
### get the answer
##answer = get_course_info(table, (keyword).upper(), att)
##print(answer)
