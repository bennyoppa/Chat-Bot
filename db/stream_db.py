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
    areas = ListField(EmbeddedDocumentField(Elective))

    def __init__(self, _id, name, areas=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = _id
        self.name = name
        self.areas = areas


def add_elective(number, electives):
    new = Elective(number, electives)
    return new


def create_streams():
    stream_id_list, courses_list, numbers_list, stream_name_dict = list_of_info()
    i = 0
    for stream_id in stream_id_list:
        _id = stream_id
        name = stream_name_dict[stream_id]
        areas = []
        if stream_id == 'COMPAS' or stream_id == 'COMPBS':
            length = 2
        elif stream_id == 'COMPSS':
            length = 3
        else:
            length = 1

        for _ in range(length):
            new_area = add_elective(numbers_list[i], courses_list[i])
            areas.append(new_area)
            i += 1

        stream = Stream(_id, name, areas)
        connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
        stream.save()
        print(_id, name)
