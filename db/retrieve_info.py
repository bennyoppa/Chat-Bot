from mongoengine import *
from db import course_db
from db import stream_db
from db import staff_db
import json


def create_course_db():
    course_db.add_courses()
    return "Course database created."


def create_stream_db():
    stream_db.create_streams()
    return "Stream database created."


def create_staff_db():
    staff_db.create_staff()
    return "Staff database created."


def get_info(table, keywords, query):
    keywords = [x.upper() for x in keywords]
    query = [x.lower() for x in query]
    if table == 'course':
        return get_course_info(keywords, query)
    elif table == 'stream':
        return get_stream_info(keywords, query)
    elif table == 'staff':
        return get_staff_info(keywords, query)
    return None


def get_course_info(keywords, query):
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    table = course_db.Course.objects
    final_result = []

    for keyword in keywords:
        result = {}
        for doc in table:
            if doc._id == keyword:
                if len(query) == 0:
                    result = json.loads(doc.to_json())
                else:
                    info = json.loads(doc.to_json())
                    for key in query:
                        result[key] = info[key]
        final_result.append(result)
    return final_result


def get_stream_info(keywords, original_query):
    found = False
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    table = stream_db.Stream.objects
    final_result = []
    original_query = [x.upper() for x in original_query]

    for keyword in keywords:
        result = []
        query = [x for x in original_query]
        for doc in table:
            if doc._id == keyword:
                found = True
                if len(query) == 0:
                    result = json.loads(doc.to_json())['areas']
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

                    for k in range(len(areas)):
                        if areas[k]['number'] > 0:
                            result.append(areas[k])
        if result:
            final_result.append(result)
        else:
            if found:
                final_result.append([True])
            else:
                final_result.append(result)
    return final_result


def get_staff_info(keywords, query):
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    table = staff_db.Staff.objects
    final_result = []

    for keyword in keywords:
        result = {}
        keyword = staff_db.change_name_format(keyword)
        for doc in table:
            if doc._id == keyword:
                if len(query) == 0:
                    result = json.loads(doc.to_json())
                else:
                    info = json.loads(doc.to_json())
                    for key in query:
                        result[key] = info[key]
        final_result.append(result)
    return final_result
