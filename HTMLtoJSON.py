from bs4 import BeautifulSoup
import json
from os import listdir,path
from os.path import isfile, join,basename
import requests



def parseHTML():
    htmlfilesdirectory = 'corpusRawHTML'
    outputdirectory = 'output'
    # open file
    for file in listdir(htmlfilesdirectory):
        if isfile(join(htmlfilesdirectory, file)) and file.endswith('.html'):
            file = open(join(htmlfilesdirectory, file))
            print('parse file: ' + file.name)

            htmlfile = BeautifulSoup(file, 'html.parser')
            output = {}
            htmlarticle = htmlfile.article
            output['title'] = getTitel(htmlarticle)
            output['metaData']= getMetadata(htmlfile)
            output['abstract'] = getAbstract(htmlarticle)

            name = path.splitext(basename(file.name))[0]
            file = open(join(outputdirectory, name + '.json'), 'w')
            json.dump(output, file)
            file.close()

def readJsonFiles():
    outputdirectory = 'output'
    for file in listdir(outputdirectory):
        # read json
        print('read file: ' + file)
        name = path.splitext(basename(file))[0]
        file = open(join(outputdirectory, name + '.json'), 'r')
        jsonfile = json.load(file)
        print(jsonfile["title"])



def getTitel(htmlArticle):
    title=htmlArticle.find("h1").text
    if title:
        return title
    else:
        return 'no title found'

def getallReferences(htmlArticle):
    pass

def getKeywords(htmlfile):
    print("keywords")
    '''for div in htmlArticle.findAll('strong'):
            if div.text and div.text == "Keywords:":
                text=div.text
                keywordsArray = div.parent.text.replace(text,"").strip()
                break
    return keywordsArray.split(";")'''
    keywords=htmlfile.find("meta", {"name": "keywords"})['content']
    print(keywords)
    return keywords

def getYear(htmlfile):
    print('year')
    year=htmlfile.find("meta", {"name": "citation_year"})['content']
    print(year)
    return int(year)

def getAbstract(htmlArticle):
    print("Abstract")
    for div in htmlArticle.findAll('div'):
        if div.find('h3'):
            container=div.find('h3')
            if container.text and container.text=="Abstract":
                #print("Abstract found!!")
                break
    abstract=div.find('p').find('p')

    print(len(abstract.findAll('br')))
    if abstract.find('strong'):
        list=[]
        #list.append({'titel': 'no Titel', 'text': abstract.next_sibling})
        for section in abstract.findAll('strong'):
            #print(section)
            #print(section.next_sibling)
            list.append({'titel': section.text,'text':section.next_sibling})
    elif abstract.find('br'):
        list = []
        #print(abstract.text.splitlines())
        for section in abstract.text.splitlines():
            #print(section)
            list.append({'title':'no Titel','text':section})
    else:
        list = {'title': 'no Titel', 'text': abstract.text}
    print(list)
    return list

def getMetadata(htmlfile):
    output={}
    output['keywords']=getKeywords(htmlfile)
    output['yearOfArticle']=getYear(htmlfile)
    return output

def getAuthors(htmlArticle):
    pass



def getSelection(htmlArticle):
    getInnerSection(htmlArticle)
    SelectionImages(htmlArticle)
    SelectionTables(htmlArticle)
    SelectionFormeln(htmlArticle)

    getSelectionTitle(htmlArticle)
    getSelectionText(htmlArticle)
    getNumSelectionReferences(htmlArticle)
    pass

def getSelectionTitle(htmlSelection):
    pass

def getSelectionText(htmlSelection):
    pass


def getNumSelectionReferences(htmlArticle):
    pass

def SelectionImages(htmlArticle):
    pass

def SelectionTables(htmlArticle):
    pass

def SelectionFormeln(htmlArticle):
    pass

def getInnerSection(htmlArticle):
    #search if inner section --> getSelection(htmlArticle)
    pass

#parseHTML()
#readJsonFiles()