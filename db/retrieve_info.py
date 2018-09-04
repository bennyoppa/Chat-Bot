from mongoengine import *
from db import course_db
from db import stream_db
import json


def create_course_db():
    course_db.add_courses()
    return "Course database created."


def create_stream_db():
    stream_db.create_streams()
    return "Stream database created."


def get_course_info(table, keyword, query):
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    if table == 'course':
        target = course_db.Course.objects
    elif table == 'stream':
        target = course_db.Course.objects
    elif table == 'staff':
        target = course_db.Course.objects
    else:
        return "Wrong table name."

    for doc in target:
        if doc._id == keyword:
            if len(query) == 0:
                result = json.loads(doc.to_json())
            else:
                result = {}
                info = json.loads(doc.to_json())
                for key in query:
                    if key not in query:
                        return "Wrong desired output."
                    result[key] = info[key]
            return result
    return "Not found."
