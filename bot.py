from nlp.rasa import RasaNLP



nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')

nlp.train()


print(nlp.find_reply('Who is the tutor of COMP9417?'))
res = nlp.parse('what is the course name of COMP9417?')
print(res)
