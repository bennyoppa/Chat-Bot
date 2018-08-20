import requests
from bs4 import BeautifulSoup
from info_lists import info
from mongoengine import *


class Course(Document):
    code = StringField(required=True)
    name = StringField(required=False)
    adk = BooleanField(required=False)
    pre_requisite = StringField(required=False)
    description = StringField(required=False)

    def __init__(self, code, name, adk, pre_requisite, description, *args, **values):
        super().__init__(*args, **values)
        self.code = code
        self.name = name
        self.adk = adk
        self.pre_requisite = pre_requisite
        self.description = description


def add_courses():
    handbooks, timetables, course_codes, course_names, adk = info()
    number_courses = len(course_codes)

    for i in range(number_courses):
        page = requests.get(handbooks[i])
        soup = BeautifulSoup(page.content, "html.parser")
        pre_requisite = None
        description = ""
        pre_req = ""
        if page.status_code == 200:
            summary = soup.find(class_="summary").get_text()
            pre_requisite = summary.split('\n')
            description = soup.find("h2").findNext("div").get_text()

        if pre_requisite:
            if len(pre_requisite) == 11:
                pre_req = pre_requisite[7][:-38]

        print(course_codes[i])
        connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
        course = Course(course_codes[i], course_names[i], adk[i], pre_req, description)
        course.save()


def delete_all_courses():
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    for course in Course.objects:
        course.delete()
    print("All courses deleted.")
