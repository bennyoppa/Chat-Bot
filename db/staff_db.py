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

    def __init__(self, _id, full_name='N/A', email='N/A', phone='N/A', office='N/A', staff_type='N/A', courses=[], *args, **kwargs):
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
    url = 'https://raw.githubusercontent.com/bennyoppa/Chat-Bot/master/multi_location_data/Contact_Details_Staff_Type.csv?token=AXsox4yMmg64M63cK84cbgu-0xVP5oJjks5brKIuwA%3D%3D'
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
                    staff = Staff(name.upper(), row[0], row[1], row[2], row[3], row[4])
                    staff.save()
                    print(row[0])
