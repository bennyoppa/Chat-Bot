from mongoengine import *
import csv
import requests
import re


class Staff(Document):
    _id = StringField(required=True, primary_key=True)
    full_name = StringField(required=False)
    email = StringField(required=False)
    phone = StringField(required=False)
    office = StringField(required=False)
    staff_type = StringField(required=False)
    courses = ListField(required=False)

    def __init__(self, _id, full_name='N/A', email='N/A', phone='N/A', office='N/A', staff_type='N/A', courses=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = _id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.office = office
        self.staff_type = staff_type
        self.courses = courses


def change_name_format(raw_name):
    split_name = re.split(' ', raw_name)
    if len(split_name) == 1:
        final_name = split_name[0]
    else:
        final_name = split_name[0][0] + ' ' + split_name[-1]
    return final_name


def create_staff():
    staff_courses = dict()
    url = 'https://raw.githubusercontent.com/bennyoppa/Chat-Bot/master/multi_location_data/Per_Semester_Course_Staff.csv?token=AXsox1Y0mlfQeosPltQEtkA9jC539l5Dks5busynwA%3D%3D'
    response = requests.get(url)
    with open('staff_course_semester.csv', 'wb') as output_file:
        output_file.write(response.content)

    first_line = True
    with open('staff_course_semester.csv') as raw_file:
        file = csv.reader(raw_file, delimiter=',')
        for row in file:
            if first_line:
                first_line = False
            else:
                if row:
                    row[0] = change_name_format(row[0][:-1]).upper()
                    row[1] = row[1][1:]
                    if row[0] in staff_courses:
                        staff_courses[row[0]].append(row[1])
                    else:
                        staff_courses[row[0]] = [row[1]]

    url = 'https://raw.githubusercontent.com/bennyoppa/Chat-Bot/master/multi_location_data/Contact_Details_Staff_Type.csv?token=AXsox1MQHF20fwOWybMHGA-kcnq7yHBGks5buuGIwA%3D%3D'
    response = requests.get(url)
    with open('staff_details.csv', 'wb') as output_file:
        output_file.write(response.content)

    first_line = True
    with open('staff_details.csv') as raw_file:
        file = csv.reader(raw_file, delimiter=',')
        for row in file:
            if first_line:
                first_line = False
            else:
                if row:
                    if row[4] == 'Staff':
                        row[4] = 'lecturer'
                    else:
                        row[4] = 'tutor'
                    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
                    name = change_name_format(row[0])
                    staff = Staff(name.upper(), row[0], row[1], row[2], row[3], row[4], staff_courses[name.upper()])
                    staff.save()
                    print(row[0])
