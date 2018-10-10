import requests
from bs4 import BeautifulSoup
import csv


def info():
    page = requests.get("https://www.engineering.unsw.edu.au/study-with-us/current-students/academic-information/electives/pg-electives")
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find_all("tbody")[0]
    rows = table.find_all("tr")[2:]

    timetables = []
    course_codes = []
    course_names = []
    adk = []

    for row in rows:
        # skip table title row
        if row.find("a"):
            # example of a row: [code, timetable, name, adk, comment]
            columns = row.find_all("td")
            # get course code
            if len(columns[0].get_text()) > 8:
                course_codes.append(columns[0].get_text()[:-1])
            else:
                course_codes.append(columns[0].get_text())
            # get course name
            course_names.append(columns[2].get_text())
            # get timetable link
            if columns[1].find("a"):
                timetables.append(columns[1].find("a")['href'])
            else:
                timetables.append(None)
            # check if the course is ADK
            if columns[3].get_text() == 'X':
                adk.append(True)
            else:
                adk.append(False)

    return timetables, course_codes, course_names, adk


def course_timetable():
    timetable = dict()
    url = 'https://raw.githubusercontent.com/bennyoppa/Chat-Bot/adbahl/multi_location_data/Course_Time.csv?token=AXsox5jSDShxYt30X1gBTsRnm1bJy4rQks5bxo6hwA%3D%3D'
    response = requests.get(url)
    with open('course_timetable.csv', 'wb') as output_file:
        output_file.write(response.content)

    first_line = True
    with open('course_timetable.csv') as raw_file:
        file = csv.reader(raw_file, delimiter=',')
        for row in file:
            if first_line:
                first_line = False
            else:
                if row:
                    timetable[row[0]] = row[1]

    return timetable
