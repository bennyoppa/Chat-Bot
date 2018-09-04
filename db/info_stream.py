from bs4 import BeautifulSoup
import requests


def list_of_info():
    courses_list = []
    numbers_list = [1, 3, 1, 3, 2, 2, 2, 3, 3, 3, 3]
    stream_name_list = []

    url = 'https://www.engineering.unsw.edu.au/computer-science-engineering/courses-programs/postgraduate-coursework/specialisations'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    start_of_table = soup.find('div', class_='paragraph').find_next('div', class_='paragraph').find('table')
    while start_of_table:
        temp = []
        columns = start_of_table.find_all('td')
        for i in range(len(columns)):
            if i % 2 == 0:
                temp.append(columns[i].get_text()[0:8])
        start_of_table = start_of_table.find_next('table')
        courses_list.append(temp)

    start_of_paragraph = soup.find('div', class_='paragraph').find_next('div', class_='paragraph')
    while start_of_paragraph:
        stream_name = start_of_paragraph.find('h3').get_text()
        if stream_name != 'COMPCS':
            stream_name_list.append(stream_name)
        start_of_paragraph = start_of_paragraph.find_next('div', class_='paragraph')

    return stream_name_list, courses_list, numbers_list
