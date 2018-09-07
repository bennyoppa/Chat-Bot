from db.info_stream import *
from mongoengine import *


class Elective(EmbeddedDocument):
    number = IntField(required=False)
    electives = ListField(required=False)

    def __init__(self, number, electives, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.number = number
        self.electives = electives


class Stream(Document):
    _id = StringField(required=True, primary_key=True)
    name = StringField(required=False)
    areas = ListField(EmbeddedDocument(Elective))

    def __init__(self, _id, name='N/A', areas=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = _id
        self.name = name
        self.areas = areas


def add_elective(number, electives):
    new = Elective(number, electives)
    return new


def create_stream_db():
    id_list, courses_list, numbers_list = list_of_info()

    for stream_id in id_list:
        pass
