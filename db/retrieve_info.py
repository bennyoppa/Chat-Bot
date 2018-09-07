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


def get_info(table, keyword, query):
    if table == 'course':
        return get_course_info(keyword, query)
    elif table == 'stream':
        return get_stream_info(keyword, query)
    elif table == 'staff':
        pass
    return None


def get_course_info(keyword, query):
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    table = course_db.Course.objects

    for doc in table:
        if doc._id == keyword:
            if len(query) == 0:
                result = json.loads(doc.to_json())
            else:
                result = {}
                info = json.loads(doc.to_json())
                for key in query:
                    if key not in query:
                        return None
                    result[key] = info[key]
            return result
    return None


def get_stream_info(keyword, query):
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    table = stream_db.Stream.objects

    for doc in table:
        if doc._id == keyword:
            if len(query) == 0:
                return json.loads(doc.to_json())['areas']
            else:
                areas = json.loads(doc.to_json())['areas']
                while query:
                    course = query.pop(0)
                    for i in range(len(areas)):
                        area = areas[i]['electives']
                        for j in range(len(area)):
                            if course == area[j]:
                                areas[i]['electives'].pop(j)
                                areas[i]['number'] = areas[i]['number'] - 1
                                break
                result = []
                for k in range(len(areas)):
                    if areas[k]['number'] != 0:
                        result.append(areas[k])
                return result
