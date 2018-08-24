from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse


import sys
sys.path.append('../../../')

from nlp.rasa import RasaNLP
from db.retrieve_info import get_course_info
import json

# Create your views here.
def homepage(request):
    return render(request, 'ChatUI.html')

def Chatbot_sub(req):
     result='Sup!!!'

     nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')
     nlp.train()

     if req.method == 'POST':
          print(req.body)
          data = json.loads(req.body)
          print(data)
          res = nlp.find_reply(data['content'])
          need_reply, [deter, table, [keyword], att] = res
          answer = get_course_info(table, (keyword).upper(), att)
          reply = ''
          for q in answer:
               reply += answer[q] + '\n'
          return HttpResponse(json.dumps(reply), content_type='application/json')
     return render(req, 'error.html')