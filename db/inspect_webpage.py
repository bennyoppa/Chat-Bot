from bs4 import BeautifulSoup
import requests
from db.info_lists import info


handbooks, timetables, course_codes, course_names, adk = info()


url = 'http://www.handbook.unsw.edu.au/postgraduate/courses/2019/COMP9900'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
print(soup)
