
from bs4 import BeautifulSoup
import requests
import json

from urllib3 import Retry

pages_crawled = []
base_link = 'https://github.com/topics/nodejs'

def crawler(url):
    try:
        page = requests.get(url)
        print("{} successfully with {}".format(url, page.status_code))
        if(page.status_code>400):
            print("{} failed with {}".format(url, page.status_code))
            return False
    except Exception as e:
        print("error occured at {}!".format(url))
        print(e)
        print("\n\n\n \t\t\t* * * * * * \n\n\n")
        return False
    soup = BeautifulSoup(page.text, 'html.parser')
    articles = soup.find_all('div', {'class': 'd-flex flex-justify-between my-3'})
    for article in articles:
        href = article.find('div', {'class': 'd-flex flex-auto'}).find('h3').findAll('a')[1]['href']
        if href not in pages_crawled:
            pages_crawled.append(href)
    return True 

crawler(base_link)
counter = 2
next = True
while(next):
    next = crawler(base_link+"?page={}".format(counter))
    counter+=1                                      

f = open("react_result.json", "a")
f.write(json.dumps(pages_crawled))
f.close()
print(pages_crawled)
print(len(pages_crawled))
