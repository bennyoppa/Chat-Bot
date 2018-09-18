from mongoengine import *


class Staff(Document):
    _id = StringField(required=True, primary_key=True)
    email = StringField(required=False)
    phone = StringField(required=False)
    office = StringField(required=False)
    staff_type = StringField(required=False)
    courses = ListField(required=False)

    def __init__(self, _id, email='N/A', phone='N/A', office='N/A', staff_type='N/A', courses=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = _id
        self.email = email
        self.phone = phone
        self.office = office
        self.staff_type = staff_type
        self.courses = courses


def create_staff():
    pass