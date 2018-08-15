import requests
from bs4 import BeautifulSoup


def info():
    page = requests.get("https://www.engineering.unsw.edu.au/study-with-us/current-students/academic-information/electives/pg-electives")
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find_all("tbody")[0]
    rows = table.find_all("tr")[2:]

    handbooks = []
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
            course_codes.append(columns[0].get_text()[:-1])
            # get course name
            course_names.append(columns[2].get_text())
            # get handbook link
            handbooks.append(columns[0].find("a")['href'])
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

    return handbooks, timetables, course_codes, course_names, adk
