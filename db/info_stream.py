from bs4 import BeautifulSoup
import requests


def list_of_electives():
    url = 'https://www.engineering.unsw.edu.au/computer-science-engineering/courses-programs/postgraduate-coursework/specialisations'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    start = soup.find('div', class_='paragraph').find_next('div', class_='paragraph').find('table')

    result = []

    while start:
        temp = []
        columns = start.find_all('td')
        for i in range(len(columns)):
            if i % 2 == 0:
                temp.append(columns[i].get_text()[0:8])
        start = start.find_next('table')
        result.append(temp)

    return result
