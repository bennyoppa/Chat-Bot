#Course Time.py: This files collect the Course Staff details (Creating KnowledgeBase).
#Created By : Arvind Bahl
#Course: Comp9900
#Project: ChatBot
#Group: Humble Learners.
#Date: 10 Sept 2018
#*******************************************************************************************

# Imports the required libraries
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv

# First stage website
page_url = "http://timetable.unsw.edu.au/2018/COMPKENS.html"
uClient = uReq(page_url)
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# Saved Contact file
out_filename = "Course_Time.csv"
#headers = "Course Code, Time  \n"
f = open(out_filename, "w")
#f.write(headers)

data_dict1 ={}

# Variable assignment
container_s = page_soup.find("td", {"class": "classSearchFormBody"}).find_all("td", {"class": "formBody"})
containers = container_s[3]
cont = containers.find_all("a", href = True)


containers1 = container_s[4]
cont1 = containers1.find_all("a", href = True)


for i in range(len(cont)):
    if (i%2==0):
        data_dict1[cont[i].text] =""
        #print(cont[i].text)
    
for j in range(len(cont1)):
    if (j%2==0):
        data_dict1[cont1[j].text] = ""
        #print(cont1[i].text)
        
#table=containers.find('tbody')
#rows = table.find_all('tr')
#data = ''
#data_dict1 ={}

# Looping and crawling websites to gather information and write to the file.
#for row in rows:
    #cols = row.find_all('td')
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
    #cd = cols[0].findAll('a')
    #data_dict1[cd[0].text] =""
 
    #temp_data=''
    #for i in  range(len(cd)):
        #temp_data = temp_data + cd[i].text+ '; '        
    #data = data + temp_data + '\n'

#print(len(data_dict1))
fin_data ={}
for key in data_dict1:

    try:
        page_url1 = "http://timetable.unsw.edu.au/2018/" + key + ".html"
        uClient1 = uReq(page_url1)
        page_soup1 = soup(uClient1.read(), "html.parser")
        uClient1.close()
            #container_s1 = page_soup1.findAll("td", {"class": "classSearchFormBody"})
        container_s1 = page_soup1.find("td", {"class": "classSearchFormBody"}).find_all("td", {"class": "formBody"})
        further =container_s1[1].find_all("td", {"class":"formBody"})

        for i in range(len(further)):
            further1= further[i].find_all("td", {"class":"data"})
            #print(key, i)
            for j in range(len(further1)):   
                if(further1[j].text=="Lecture" and further1[j+3].text.startswith("WEB") == False):
                    if further1[j+6].text != "In Person":
                        fin_data[key] = further1[j+6].text
    except:
        pass
                                  
    #containers1 = container_s1[1]
    #table1=containers1.find('tbody')



with open(out_filename, 'w') as csv_file:
    #csv_file.write(headers)
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "Time"])
    for key, value in fin_data.items():
        if value != "":
            writer.writerow([key, value])    

#with open(out_filename, 'w') as csv_file:

#f.write(data)
#data =''
    #cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele]) 

f.close()

