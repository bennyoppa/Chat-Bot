#Course Staff.py: This files collect the Course Staff details (Creating KnowledgeBase).
#Created By : Arvind Bahl
#Course: Comp9900
#Project: ChatBot
#Group: Humble Learners.
#Date: 30 Aug 2018
#*******************************************************************************************

# Imports the required libraries
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv

# First stage website
page_url = "https://webcms3.cse.unsw.edu.au/search"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# Saved Contact file
out_filename = "Per_Semester_Course_Staff.csv"
headers = "Course Staff, Course Code, Semesters,   \n"
f = open(out_filename, "w")
f.write(headers)

# Variable assignment
container_s = page_soup.findAll("div", {"class": "table-responsive"})
containers = container_s[0]
table=containers.find('tbody')
rows = table.find_all('tr')
data = ''
data_dict = {}
# Looping and crawling websites to gather information and write to the file.
for row in rows:
    cols = row.find_all('td')
    data = data + cols[0].text+ ' , '
    data = data + cols[1].text+ ' , '
	
    cd = cols[4].findAll('a')
    temp_data=''
    for i in  range(len(cd)):
        temp_data = cd[i].text + " , " + cols[0].text
        if (temp_data in data_dict):
            data_dict[temp_data] = data_dict[temp_data] + " ; " + cols[1].text
        else:
            data_dict[temp_data] = cols[1].text
        temp_data=''
	
	#Write to the file.
with open(out_filename, 'w') as csv_file:
    #csv_file.write(headers)
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "Course Code", "Semesters"])
    writer.writerow(["", "", ""])
    writer.writerow(["", "", ""])
    writer.writerow(["", "", ""])
    for key, value in data_dict.items():
        key1 = key.split(",")
        value1 = key1[1] + "," + value
        writer.writerow([key1[0], key1[1], value])

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
    #cd = cols[4].findAll('a')
 
    #temp_data=''
    #for i in  range(len(cd)):
        #temp_data = temp_data + cd[i].text+ '; '
        
    #data = data + temp_data + '\n'

    #f.write(data)
    #data =''
    #cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele]) 

#f.close()

