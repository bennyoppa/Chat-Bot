from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
#q = 'Who is the pre_requisite of COMP9417?'

import sys
sys.path.append('../../../')

from nlp.rasa import RasaNLP
from db.retrieve_info import get_course_info
import json

# get reply
def reply(parsed_query):
    '''
    takes RasaNLP parsed query as input
    outputs the answer string for user
    '''
    print(parsed_query)
    need_reply, \
    [deter,
     table,
     [keyword],
     att] = parsed_query
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

# Create your views here.
def homepage(request):
    return render(request, 'mainpage.html')

def Chatbot_iframe(request):
    return  render(request, 'ChatUI.html')

def Chatbot_sub(req):

     nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')
     nlp.train()

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
          return HttpResponse(json.dumps(reply(nlp.find_reply(data['content']))), content_type='application/json')
     return render(req, 'error.html')