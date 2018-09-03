#Staff_Course.py: This files collect the Staff and thier course details (Creating KnowledgeBase).
#Created By : Arvind Bahl
#Course: Comp9900
#Project: ChatBot
#Group: Humble Learners.
#Date: 30 Aug 2018
#*******************************************************************************************

# Imports the required libraries
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

# First stage website
page_url = "https://webcms3.cse.unsw.edu.au/search"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# Name the file and put headers
out_filename = "Staff_Course.csv"
headers = "Course Staff, Course Code,Semester,Course Name  \n"
f = open(out_filename, "w")
f.write(headers)

# Variable assignment
container_s = page_soup.findAll("div", {"class": "table-responsive"})
containers = container_s[0]
table=containers.find('tbody')
rows = table.find_all('tr')
data = ''

# Looping and crawling websites to gather information and write to the file.
for row in rows:
    cols = row.find_all('td')
    cd = cols[4].findAll('a')
    
    #data = data + cols[0].text+ ' , '
    #data = data + cols[1].text+ ' , '
    #data = data + cols[2].text.replace(',', '')+ ' , '
    #data = data + cols[3].text.replace('\n', '').strip()+ ' , '
    #data = data + cols[4].findAll('a').text.replace('\n', ' ')+ ' , '

    '''
    if (len(cols[3].findAll('td') ==0):
        data = data + " " + ' , '
    else:
        data = data + cols[3].string+ ' , ' 
    data = data + cols[3].str + ' , '
        '''
 
    temp_data=''
    for i in  range(len(cd)):
        temp_data = cd[i].text+ ',' + cols[0].text+ ' , ' + data + cols[1].text+ ' , ' + cols[2].text.replace(',', '') + "\n"
        f.write(temp_data)
        temp_data=""
        
    #data = data + temp_data + '\n'

    #f.write(data)
    #data =''
    #cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele]) 

f.close()

