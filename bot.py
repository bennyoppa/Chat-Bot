from nlp.rasa import RasaNLP
#from SpeechRecognition.SpeechRecognition import BotSR

from db.retrieve_info import get_info

# stream, no record and eligible are the same.
#                       return True

qs = "I've completed COMP6714 and comp9313 and COMP9321, what other subjects do I have to study to declare COMPDS stream and COMPAS?"



qq = "show me the name of comp4121"


qq0 = 'is it adk'
qq1 = 'what is the name of it'




import warnings
warnings.filterwarnings('ignore')

#!/usr/bin/env python -W ignore::DeprecationWarning


##def reply(parsed_query):
##    '''
##    takes RasaNLP parsed query as input
##    outputs the answer string for user
##    '''
##
##    answers = ['Let me check.',
##               'Here is what I found:'
##               ]
##
##    notfound = 'Sorry, can\'t find what you want'
##
##    stream = ['number', 'electives']
##
##    if parsed_query[0] is True:
##        # need_reply,[]
##        _, [deter, table, keyword, att] = parsed_query
##
##        info_list = get_info(table, keyword, att)
##
##        if not any(info_list):
##            return notfound
##        
##        answer = ''
##
##        for index in range(len(keyword)):
##            key = keyword[index]
##            info = info_list[index]
##
##            if table == 'course':
##                
##                if not deter:
##                    answer += key.upper() + ':\n'
##                    for i in info:
##                        answer += '\t' + i + ': ' + info[i] + '\n'
##
##                else:
##                    answer += key
##                    for i in info:
##                        if info[i]:
##                            answer += ' is ' + i + ','
##                        else:
##                            answer += ' is not' + i + ','
##
##                    answer = answer[:-1] + '.' + '\n'
##
##                
##            elif table == 'stream':
##                answer += key.upper() + ':\n\tPlease choose'
##                for i in range(len(info)):
##                    if i > 0:
##                        answer += '\n\tAnd'
##                    answer += ' ' + str(info[i][stream[0]]) + ' subjects from below:\n\t\t' \
##                              + '\n\t\t'.join(info[i][stream[1]])
##                answer += '\n'
##
##        return answer[:-1]
##    
##    return parsed_query




        
##        if need_reply:
##            answer = ''
##            info = get_info(table, keyword, att)
##            print('printing: ', info)
##            if not deter:
##                # non determinnistic answer
##                for dic in info:
##                    for key in dic:
##                        answer += dic[key] + '\n'
##            else:
##                # determinnistic answer
##                d = True
##                if not info:
##                    '''
##                    change db to return False later instead of 'not found'
##                    '''
##                    # no record found
##                    answer = 'No.'
##                else:
##                    for i in info:
##                        d = d and info[i]
##                        answer += i + ': ' + str(info[i]) + '\n'
##                    if d:
##                        answer = 'Yes, ' + answer
##                    else:
##                        answer = 'No, ' + answer
##
##        return answer

q01 = 'What is the pre_requisite of COMP9417?'


q02 = 'What is the pre_requisite and name of COMP9517 and comp9418?'
q03 = "What are the prerequisite and lic of COMP3121 and comp4121?"
q04 = 'do you know Tatjana Zrimec'

##????????
##q11 = 'Is COMP9417 an adk course?'

q="show me the lic of comp9021"
qq="how to contact lic of comp9020"

q11 = 'Is COMP9418 an adk course?'
q12 = 'What is the prerequisite of it?'

q21 = 'Are COMP9417 and comp9801 adk courses?'
q22 = "What is the prerequisite of coMp9024 and comp9444?"
q23 = "What are the prerequisite and name of coMp9024 and comp9021?"


q3 = 'I\'ve done comp9021 and comp9024, am i eligible for COMPas stream?'
q41 = "What subjects do I have to complete to declare COMPAS stream?"
q42 = "What subjects do I have to complete to declare COMPAS and COMPDS stream?"

q51 = "what is the phone/email of eric martin?"

q61 = "who is the lic of comp9021?"
q62 = "where is the office of eric martin?"
q63 = "what courses does eric martin teach?"

q71="tell/show/give/me/ what's/the contact number of eric martin "
q72="do you know lic of comp9021?"
q73="do you know where is the office of eric martin"
q74="do you know Eric Martin/name of comp9444/comp9900"
q75="tell me something about comp9323/Alan Blair"
q76= "how to contact the lic of comp9020?"

q77 = 'whos lic comp9020'
q78 = 'how to contact him'

#  train the nlp model
nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')
nlp.train()

botsr = BotSR()


##print(reply(nlp.find_reply(q4)))


##print(   reply(nlp.reply(q41))    )
##print(   reply(nlp.reply(q42))    )

print(nlp._reply(q))
print(nlp._reply(qq))



def test():
    while 1:
        print('Your question:')
        q = input()
        if q == 'q':
            break
        print(nlp.reply(q))

    nlp.snapshot_unparsed_messages('unparsed.txt')

def test2():
    while 1:
        print('Tell me your question:')
        q = botsr.recognise()
        if q is False:
            print('Sorry, I didn\'t hear what you just said')
        else:
            print(nlp.reply(q))


    nlp.snapshot_unparsed_messages('unparsed.txt')



##test2()


### parse query
##parsed_query = nlp.find_reply(q)
##need_reply, [deter, table, [keyword], att] = parsed_query
##
##
### get the answer
##answer = get_course_info(table, (keyword).upper(), att)
##print(answer)



##a=[{'adk': False, 'name': 'Principles of Programming'}, {'adk': False, 'name': 'Data Structures and Algorithms'}]
##b=[[{'number': 1, 'electives': ['COMP9414', 'COMP9814']}, {'number': 2, 'electives': ['COMP4411', 'COMP4418', 'COMP9318', 'COMP9418', 'COMP9444', 'COMP9517']}], [{'number': 3, 'electives': ['COMP6714', 'COMP9313', 'COMP9315', 'COMP9318', 'COMP9319', 'COMP9321']}]]
