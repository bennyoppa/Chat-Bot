from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
#q = 'Who is the pre_requisite of COMP9417?'

import sys
sys.path.append('../../../')

from nlp.rasa import RasaNLP
from db.retrieve_info import get_info
import json

# get reply
def reply(parsed_query):
    '''
    takes RasaNLP parsed query as input
    outputs the answer string for user
    '''

    answers = ['Let me check.',
               'Here is what I found:'
               ]

    notfound = 'Sorry, can\'t find what you want'

    stream = ['number', 'electives']
    if parsed_query[0] is True:
        # need_reply,[]
        _, [deter, table, keyword, att] = parsed_query

        try:
            info_list = get_info(table, keyword, att)
        except:
            return notfound

        print('returned data:',keyword, 'att: ', att)

        if not any(info_list):
            return notfound

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
                answer += key.upper() + ':\n\tPlease choose '
                for i in range(len(info)):
                    if i > 0:
                        answer += '\n\tAnd '
                    answer += str(info[i][stream[0]]) + ' subjects from below: \n\t\t' \
                              + ' \n\t\t'.join(info[i][stream[1]])
                answer += ' \n'
        print(answer[:-1])
        return answer[:-1]

    return parsed_query

# Create your views here.
def homepage(request):
    return render(request, 'mainpage.html')

def Chatbot_iframe(request):
    return render(request, 'ChatUI.html')

def mytips(req):
    return render(req,'test3.html')

nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')
nlp.train()

def Chatbot_sub(req):
     if req.method == 'POST':
          print(req.body)
          data = json.loads(req.body)
          print(data)
          #res = nlp.find_reply(data['content'])
          #need_reply, [deter, table, [keyword], att] = res
          #answer = get_course_info(table, (keyword).upper(), att)
          #reply = ''
          #for q in answer:
          #     reply += answer[q] + '\n'
          answer = reply(nlp.find_reply(data['content']))
          print('view: ', nlp.subject)

          return HttpResponse(json.dumps(answer), content_type='application/json')
     return render(req, 'error.html')