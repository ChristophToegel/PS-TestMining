from bs4 import BeautifulSoup
import requests
import os

def getJournalsFromCategoriesPage(categoryurl,categoryName):
    #print(categoryurl)
    r = requests.get(categoryurl)
    journalpage = BeautifulSoup(r.text, 'html.parser')
    #print(r.text)
    for journal in journalpage.findAll('td', attrs={'valign': 'middle'}):
        #print(journal)
        journallink=journal.find('a')
        if journallink:
            print('Journaltitel:'+journallink['title'])
            #print(journallink['href'])
            getArchiveList(journallink['href'],categoryName)

def getArchiveList(journallink,categoryName):
    #print('link')
    r = requests.get(journallink)
    journalpage = BeautifulSoup(r.text, 'html.parser')
    for listitem in journalpage.findAll('li',{"class": "nav-item"}):
        link=listitem.find('a')
        if link.text=="Archive":
            getPaperlist(link['href'],categoryName)
            #print('archivelink found:'+link['href'])

def getPaperlist(journalarchive,categoryName):
    r = requests.get(journalarchive)
    journalarchive = BeautifulSoup(r.text, 'html.parser')
    for year in journalarchive.findAll('h6',{"class": "card-header p-2"}):
        card=year.find('strong')
        if card.text=="2018":
            for paperlistlink in year.parent.find('nav').findAll('a'):
                print('Paperlist'+paperlistlink['href'])
                savePaper(paperlistlink['href'],categoryName)

def savePaper(paperlistlink,categoryName):
    r = requests.get(paperlistlink)
    paperlist = BeautifulSoup(r.text, 'html.parser')
    for paperEntry in paperlist.findAll('div',{'class':"row"}):
        for link in paperEntry.findAll('a'):
            if link.text=="Peer-reviewed Full Article":
                global counter
                print('Article link found:'+link['href'])
                r = requests.get(link['href'])
                #paperlink split by /
                if not os.path.exists('crawlerHTMLTest/'+categoryName):
                    os.makedirs('crawlerHTMLTest/'+categoryName)
                name=link['href'].split('/')[len(link['href'].split('/'))-1]
                #paperfehlerausbessern
                file=open('crawlerHTMLTest/'+categoryName+'/'+name, 'w')
                file.write(r.text)
                file.close()
                counter+=1


def runCrawler():
    r = requests.get('https://www.omicsonline.org')
    htmlfile = BeautifulSoup(r.text, 'html.parser')
    for titel in htmlfile.findAll('h3'):
        if titel.text == "Journals by Subject":
            for category in titel.parent.parent.findAll('a'):
                print('category: '+category['title'])
                getJournalsFromCategoriesPage(category['href'],category['title'])

counter=0
runCrawler()
