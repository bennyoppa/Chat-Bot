from bs4 import BeautifulSoup
import requests

url = 'http://timetable.unsw.edu.au/2018/COMP9021.html'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
print(soup)
