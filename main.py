import requests
from bs4 import BeautifulSoup
from info_lists import info


handbooks, timetables, course_codes, course_names, adk = info()
number_courses = len(course_codes)

for i in range(number_courses):
    page = requests.get(handbooks[i])
    soup = BeautifulSoup(page.content, "html.parser")
    pre_requisite = None
    description = None
    if page.status_code == 200:
        summary = soup.find(class_="summary").get_text()
        pre_requisite = summary.split('\n')
        description = soup.find("h2").findNext("div").get_text()

    print(course_codes[i])
    print(course_names[i])
    print("ADK: {:}".format(adk[i]))
    if pre_requisite and len(pre_requisite) == 11:
        print(pre_requisite[7][:-38])
    else:
        print(None)
    if description:
        print(description)
    else:
        print(None)
    print()
