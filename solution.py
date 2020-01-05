import requests
import bs4
import json
from threading import Thread


def extracting_information(tab,out):

    list_of_links = []  # this is a list for all the links in a single department
    [list_of_links.append(i.get('href')) for i in soup.select('div {} .clickable-row a'.format(tab))]

    for dep_link in list_of_links:
        request = requests.get(dep_link)
        soup2 = bs4.BeautifulSoup(request.text, 'lxml')

        description_of_job = {'title': '', 'location': '', 'description': [], 'qualification': [], 'posted by': ''}

        description_of_job['title'] = soup2.find_all(class_='job-title')[0].text
        description_of_job['location'] = soup2.find_all('span', class_='job-detail')[0].text
        [description_of_job['description'].append(de.text) for de in soup2.select('#st-jobDescription .wysiwyg ul li')]
        [description_of_job['qualification'].append(qu.text) for qu in soup2.select('#st-qualifications .wysiwyg ul li')]
        try:
            description_of_job['posted by'] = soup2.select('.details h3')[0].text
        except IndexError:
            description_of_job['posted by'] = 'NULL'

        output[out].append(description_of_job)


req = requests.get('https://www.cermati.com/karir')
soup = bs4.BeautifulSoup(req.text, 'lxml')

output = {}
output1 = []    # creating the list for the departments for looping purpose
dep = soup.find_all('h4', class_='tab-title')   # selecting the departments code and adding into the output dictionary
for i in dep:               # selecting only the text from that code
    output[i.text] = []
    output1.append(i.text)

tabs = []   # this is a list of id's of departments from html code
[tabs.append(i.get('href')) for i in soup.select('div .col-xs-2 a')]

li = []

for i in range(len(tabs)):
    li.append(Thread(target=extracting_information, args=(tabs[i], output1[i],)))   # creating a thread for each department
    li[i].start()   # starting the thread simultaneously

for i in range(len(li)):
    li[i].join()    # making the main thread to wait for all the other threads we had started

print(output)
with open('solution.json', 'w') as creating_file:
    json.dump(output, creating_file)
