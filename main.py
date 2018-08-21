from mongoengine import *
import course_db
import re
import json


def create_course_db():
    course_db.add_courses()
    return "Course database created."


def delete_course_db():
    course_db.delete_all_courses()
    return "Course database deleted."


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


if __name__ == '__main__':
    while True:
        print("---instruction---")
        print("c - Create database")
        print("d - Delete database")
        print("s - Search")
        print("q - Quit\n")
        action = input("Select an action: ")
        if action == 's':
            table_name = input("Enter a table name: ")
            match_keyword = input("Enter a search keyword: ")
            output = input("Enter desired search result: ")
            if len(output) == 0:
                output = []
            else:
                output = re.split(' ', output)
            print(get_course_info(table_name, match_keyword, output))
            print()
        elif action == 'q':
            break
        elif action == 'c':
            create_course_db()
            print()
        elif action == 'd':
            delete_course_db()
            print()
        else:
            continue
