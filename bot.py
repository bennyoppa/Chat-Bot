from nlp.rasa import RasaNLP



nlp = RasaNLP('./rasa-config.json', './rasa-data.json', './rasa-model')

nlp.train()


print(nlp.find_reply('Who is the tutor of COMP9417?'))
res = nlp.parse('Who is the LiC of COMP9417?')
print(res)
