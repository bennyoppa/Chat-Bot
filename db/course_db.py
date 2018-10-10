import requests
from bs4 import BeautifulSoup
from db.info_lists import info, course_timetable
from mongoengine import *


class Course(Document):
    _id = StringField(required=True, primary_key=True)
    name = StringField(required=False)
    adk = BooleanField(required=False)
    pre_requisite = StringField(required=False)
    description = StringField(required=False)
    lic = StringField(required=False)
    timetable = StringField(required=False)

    def __init__(self, _id, name, adk, pre_requisite='N/A', description='N/A', lic='N/A', timetable='N/A', *args, **values):
        super().__init__(*args, **values)
        self._id = _id
        self.name = name
        self.adk = adk
        self.pre_requisite = pre_requisite
        self.description = description
        self.lic = lic
        self.timetable = timetable


def add_courses():
    timetables = course_timetable()
    timetables_link, course_codes, course_names, adk = info()
    number_courses = len(course_codes)

    for i in range(number_courses):
        print(course_codes[i])
        pre_req = 'N/A'
        description = 'N/A'
        lic = 'N/A'

        page = requests.get('http://www.handbook.unsw.edu.au/postgraduate/courses/2019/' + course_codes[i])
        soup = BeautifulSoup(page.content, "html.parser")
        if soup.find(text='Conditions for Enrolment'):
            pre_req = soup.find_all('h3')[1].find_next().find('div').get_text()[15:]
            pre_req = pre_req.replace('\n', '')

        if soup.find('div', class_="a-card-text m-toggle-text has-focus"):
            description = soup.find('div', class_="a-card-text m-toggle-text has-focus").get_text()
            description = description.replace('\n', '')

        url = timetables_link[i]
        if url:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            if soup.find(text='T1'):
                lic = soup.find(text='T1').find_next().get_text()
            elif soup.find(text='T2'):
                lic = soup.find(text='T2').find_next().get_text()

        if course_codes[i] in timetables:
            timetable = timetables[course_codes[i]]
        else:
            timetable = 'N/A'

        connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
        course = Course(course_codes[i], course_names[i], adk[i], pre_req, description, lic, timetable)
        course.save()
