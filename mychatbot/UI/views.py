from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,HttpResponse
import json

# Create your views here.
def homepage(request):
    return render(request, 'ChatUI.html')

def Chatbot_sub(req):
     result='Sup!!!'
     if req.method == 'POST':
          print(req.body)
          data = json.loads(req.body)
          print(data)
          return HttpResponse(json.dumps(result), content_type='application/json')
     return render(req, 'error.html')