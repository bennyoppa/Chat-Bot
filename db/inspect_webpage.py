from bs4 import BeautifulSoup
import requests
from db.info_lists import info


page = requests.get('http://www.handbook.unsw.edu.au/postgraduate/courses/2019/COMP9318')
soup = BeautifulSoup(page.content, "html.parser")
if soup.find(text='Conditions for Enrolment'):
    pre_req = soup.find_all('h3')[1].find_next().find('div').get_text()[15:]
    pre_req = pre_req.replace('\n', '')
    print(pre_req)