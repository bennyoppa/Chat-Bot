from mongoengine import *
from flask import *
import course_db
import re
import json

app = Flask(__name__)


@app.route('/create/courses', methods=['GET'])
def create_course_db():
    course_db.add_courses()
    return "Course database created.", 200


@app.route('/delete/courses', methods=['DELETE'])
def delete_course_db():
    course_db.delete_all_courses()
    return "Course database deleted.", 200


@app.route('/courses/<code>', methods=['GET'])
def get_course_info(code):
    connect(host='mongodb://benny:comp9900@ds125912.mlab.com:25912/comp9900')
    raw_query = request.query_string.decode()
    query = re.split('\+', raw_query)

    for course in course_db.Course.objects:
        if course.code == code:
            if len(raw_query) == 0:
                result = json.loads(course.to_json())
            else:
                result = {}
                info = json.loads(course.to_json())
                for key in query:
                    if key not in course:
                        return "Wrong query.", 404
                    result[key] = info[key]
            return jsonify(result), 200
    return code + " not found.", 404


if __name__ == '__main__':
    app.run()
